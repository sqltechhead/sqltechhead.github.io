---
title: Query Execution Internals
date: 2020-02-16 19:00:00 +0000
categories: [SQL, Internals, Performance]
---
## Introduction
Every time a query is run there are preset steps that have to occur for SQL to turn a T-SQL query into an execution plan and provide results. For a brand new query SQL uses 4 main internal steps:

- Query Parser
- Algebrizer
- Optimizer
- Query Execution
These set of steps are known as Query Compilation. Each step carries out different actions to create the plan.

## Query Parser
When T-SQL query is executed the first internal step it will reach is the query parser. This steps main function is to ensure that the T-SQL is written correctly, there are no syntax errors. You may recognise the below button in SSMS. This utilises the Query Parser Internal step:

![QueryInternals](/assets/images/QueryExecutionInternals.png){: .dark .w-75 .normal }

The output is a parse tree. Which is essentially a test that a set of steps can be created for the query. If you have mis-spelt a WHERE clause then a set of steps will not be able to be created so the parser returns and error.

Create the test database and table below:

```sql
CREATE DATABASE QueryInternals
 
GO
 
USE [QueryInternals]
GO
CREATE TABLE TestTable (ID INT,ColumnName VARCHAR(50))
```

Now if you were to run the below query. The Query Parser would fail and stop the query process

```sql
SELECT * 
FRM dbo.TestTable
```

Whereas if you were to correct the query and run the below, the query process would succeed on the Query Parser and move onto the Algebrizer:

```sql
SELECT * 
FROM dbo.TestTable
```

## Algebrizer
Next step if the parsing has succeeded is the algebrizer. This step will bind the query, what this means that once it knows that the query is structured correctly, it needs to make sure all the objects that are being requested are available and correct. It also pulls back object definitions if it finds the objects in the database such as data type information. As an example, using your test database and table. If the below SQL was run then the query would pass the Query Parser, but fail on he Algebrizer:

```sql
SELECT * 
FROM dbo.NonExistent_TestTable
```

We haven’t created this table so it doesn’t exist, so when the Algebrizer tries to bind it, it cannot find any information on it so fails at this step. Now if you were to run the below query it would succeed:

```sql
SELECT * 
FROM dbo.TestTable
```

Now with the above query the Query Parser will succeed and so will the Algebrizer. The algebrizer will then output something called a Query Processor Tree. This is then passed onto the Query optimizer. This output includes a hash also, which allows SQL to find other references of this hash in the instance. At this point it decides whether to create a new plan or use the plan that already exists. If a valid plan exists already then that is used and the process completes. If no plan is found or a plan is found but it isn’t valid, for example if it needs to be recompiled due to changes in the table definition then it will move onto the Query Optimizer step.

## Query Optimizer
The Query Optimizer is an internal process that makes decisions based on information available to it and gathered for the best way to run a query. The input parameter is the Query Processor Tree the Algebrizer has just created. The Query Optimizer will then generate a cost (this is a unitless measurment) against each possible execution. It will use the query which has the lowest cost. There are 2 types of way the Query Optimizer generates execution plans:

- Full Cost Based optimization
- Trivial Plan

### Full Cost Based Optimization
This type of optimization takes 3 parameters:

- The Query Processor Tree – This is the output parameter from the Algebrizer. It holds all the objects and object definitions that were found in the previous step.
- SQL Statistics – For each of the objects that are passed in via the Processor Tree, SQL will then grab the Statistics available to enhance its deicison making.
- Constraints – These are important, SQL needs to know any limitations/requirements for the data it needs to store. Things like Primary Keys and Foreign Keys, will give the optimizer information to decide which route to take.

Using these parameters it then changes the Query Processor Tree into a query plan with different physical operators. It will generate multiple different plans and estimate the cost of each. It does this by using the above parameters. This allows it to estimate the cost at a subsecond speed. When it has found the plan with the lowest cost then it will use that plan to execute the query. Before it does that, it will save the Query Plan in the Plan Cache. The plan cache holds queries so that they can be reused if needed.

### Trivial Plans
When SQL decides to use a Trivial Plan isn’t known or documented, so is mostly a guess. But a trivial plan is one that is deemed as easy to execute so a small amount of physical operators. For example the below query would be a trivial plan:

```sql
SELECT * 
FROM dbo.TestTable
```
![QueryInternals](/assets/images/QueryExecutionInternals1.png){: .dark .w-75 .normal }

The table we are running against has no indexes and is selecting all from 1 table so is considered trivial. If there were multiple indexes or more tables included then it would need to go through Full Cost Based Optimization as it would need to analyse these objects.

### Query Execution
Now that the plan has been created, the Query Execution Engine will follow the set of instructions in the Query Plan to execute the query.

## The Plan Cache and Plan Reuse
All the above processes come with their overhead, most noticeably their CPU cost. For complicated queries that have large plans will have more CPU cost than simple queries, they will also take a longer time to compile.

To reduce the constant cost of these compiles, SQL server will hold plans in an area of the server memory called the plan cache. SQL will then try and reuse these plans wherever possible. Being able to reuse plans means that you skip the majority of the query compilation phase and just push the plan straight to the execution engine. There are a few reasons why query plans might be removed from the cache.

- Plan Aging
- Forced out due to memory pressure
- Manually clearing the cache

### Plan Aging
Each plan holds an age value that is the estimated CPU cost of compilation multiplied by number of uses. So a CPU cost of 50 that has been executed 5 times has an age of 250. SQL server wants to keep highly expensive queries that are executed frequently for as long as possible. The lazywriter process will check the plans periodically and decrease the age value by age each time.

### Manually Clearing the Plan Cache
Manually clearing the plan cache is only really used in testing environments and is not a great idea in production for obvious reasons. The below query will clear the plan cache for all databases on the server.

```sql
DBCC FREEPROCCACHE
```
As well as clearing the cache for the entire server you can also clear a specific plan. There may be a plan in the plan cache that is being used but is unperformant. To do that you can run the below query to pull back plan_handles and sql_handles.

```sql
SELECT      S.dbid
            ,S.text
            ,Q.query_plan
            ,T.plan_handle
            ,T.sql_handle
FROM        SYS.DM_EXEC_QUERY_STATS T
CROSS APPLY SYS.DM_EXEC_SQL_TEXT(SQL_HANDLE) S
CROSS APPLY SYS.DM_EXEC_QUERY_PLAN(PLAN_HANDLE)Q
```

Then once you have the plan_handle or sql_handle you can run the below to remove the plan

```sql
DBCC FREEPROCCACHE(PLAN_HANDLE)
```

### Plan Bloat
Plan bloat can cause alot of noise in your plan cache and really waste space. It comes from queries that cause SQL to store single use plans in the plan cache.

The below test will show you this. A query is dynamically created so that a different number is added to the query each execution. This causes SQL to store the same plan 100 times because of the different number.

```sql
--Clear the query plan cache
DBCC FREEPROCCACHE
 
--Check contents of the query plan for our table
SELECT * 
FROM        SYS.dm_exec_cached_plans P
CROSS APPLY SYS.DM_EXEC_QUERY_PLAN(PLAN_HANDLE) Q
CROSS APPLY SYS.DM_EXEC_SQL_TEXT(PLAN_HANDLE) T
WHERE       t.text like '%PlanCacheBloat%'
 
--Create table and populate
USE  [QueryInternals]
GO
DROP TABLE IF EXISTS PlanCacheBloat
GO
CREATE TABLE PlanCacheBloat (
ID INT IDENTITY(1,1))
GO
 
INSERT INTO dbo.PlanCacheBloat
DEFAULT VALUES
GO 1000
 
--Run loop to select each row 
DECLARE @ID INT = 0
DECLARE @SQL NVARCHAR(MAX)
 
WHILE @ID <=100
    BEGIN
 
        SET @SQL = '
        SELECT id
        FROM dbo.PlanCacheBloat
        WHERE ID = ' + CONVERT(NVARCHAR,@ID)
 
        EXEC(@SQL)
 
        SET @ID +=1
 
    END
 
 
--Check how many plans are in the table now
SELECT t.text,q.query_plan,p.objtype,p.usecounts
FROM SYS.dm_exec_cached_plans P
CROSS APPLY SYS.DM_EXEC_QUERY_PLAN(PLAN_HANDLE) Q
CROSS APPLY SYS.DM_EXEC_SQL_TEXT(PLAN_HANDLE) T
WHERE t.text like '%PlanCacheBloat%'
```

Now if you run the below query. This will show how the user of paramaterization can cause those 100 plans to be cached into 1 plan and reused. This not only reduces space used in the plan cache, it also reduces the number of compilations SQL has to do.

![QueryInternals](/assets/images/QueryExecutionInternals2.png){: .dark .w-75 .normal }

```sql
--Clear the query plan cache
DBCC FREEPROCCACHE
 
--Check contents of the query plan for our table
SELECT * 
FROM        SYS.dm_exec_cached_plans P
CROSS APPLY SYS.DM_EXEC_QUERY_PLAN(PLAN_HANDLE) Q
CROSS APPLY SYS.DM_EXEC_SQL_TEXT(PLAN_HANDLE) T
WHERE       t.text like '%PlanCacheBloat%'
 
--Create table and populate
USE  [QueryInternals]
GO
DROP TABLE IF EXISTS PlanCacheBloat
GO
CREATE TABLE PlanCacheBloat (
ID INT IDENTITY(1,1))
GO
 
INSERT INTO dbo.PlanCacheBloat
DEFAULT VALUES
GO 1000
 
--Run loop to select each row 
DECLARE @ID INT = 0
DECLARE @SQL NVARCHAR(MAX)
 
WHILE @ID <=100
    BEGIN
 
         
        SELECT id
        FROM dbo.PlanCacheBloat
        WHERE ID = @ID
 
        EXEC(@SQL)
 
        SET @ID +=1
 
    END
 
 
--Check how many plans are in the table now
SELECT t.text,q.query_plan,p.objtype,p.usecounts
FROM SYS.dm_exec_cached_plans P
CROSS APPLY SYS.DM_EXEC_QUERY_PLAN(PLAN_HANDLE) Q
CROSS APPLY SYS.DM_EXEC_SQL_TEXT(PLAN_HANDLE) T
WHERE t.text like '%PlanCacheBloat%'
```

![QueryInternals](/assets/images/QueryExecutionInternals3.png){: .dark .w-75 .normal }

### Plan Recompilation
Recompilation can happen for a number of reasons, majority of reasons are changes made to underlying objects that affect query execution. This means that that related plans will be marked for recompilation upon next execution. The below are the main reasons why an execution plan may be marked for recompilation:

- Changing the structure of a table, view or function referenced by the query plan
- Amendments to an index being used for a query plan
- Statistics update for a specific index for a query plan
- Using sp_recompile