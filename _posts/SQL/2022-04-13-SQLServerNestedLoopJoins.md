---
title: SQL Server Nested Loop Join
date: 2023-04-13 07:33:00 +0000
layout: post
categories: [SQL, SQLPerformance]
---

## Introduction
Lets debunk join types slightly before we get into the chunk of the post. In SQL Server there are Logical and Physical join types. Logical join types include the below TSQL Syntax':
- Inner Join
- Left Join
- Right Join
- Cross Join

Whereby physical join types are what you will see in Query Execution plans and include:
- Loop Join
- Merge Join
- Hash Join
- Adaptive Join

## Nested Loop Joins

### Indexed Nested Loop
We will be using the Adventure Works database to demo this type of Loop. If we run the below on the AdventureWorks database we should be able to replicate an indexed Nested Loop Join
```sql
SELECT TOP(1000) b.[BusinessEntityID]
				,b.[AddressID]
				,b.[AddressTypeID]
				,a.[name]
FROM			[AdventureWorks].[Person].[AddressType] a
INNER JOIN		[AdventureWorks].[Person].[BusinessEntityAddress] b
ON				a.addresstypeid = b.addresstypeid
```
![IndexedNestedLoopPlan](/assets/images/IndexedNestedLoopPlan.png){: .dark .w-75 .normal }

A nested loop consists of 2 tables and outer table and an inner table. 
- Outer Table = Top table in the plan
- Inner Table = Bottom table in the plan

Usually (not always) the outer table will be the smaller table. Then for each row in the outer table it will search for its related row in the inner table. This is how SQL joins the table and brings back the rows that match. 

In our example it picks up 3 rows from the outer table, and then for each one of those rows it searches for its matches, so in total it executes 3 loops. Nice and efficient, what makes it even more efficient is that SQL is doing an Index Seek on the inner table, this means for each row in the outer table it can seek straight to the row it needs and read no un-necessary rows. 

If we look at the inner table then it has read and brought back exactly 1000 rows. This is exactly what we want, no excess reads so really good

![IndexedLoopJoinInner](/assets/images/IndexedLoopJoinInner.png){: .dark .w-75 .normal }

Now imagine if SQL decides to choose the larger table for the outer table, it would have to do alot more executions which would take alot longer and use alot more resources, even with an index its still alot of work. 

Bert Wagner created a great visual to explain how these work in a little more detail and a great blog post on Nested Loop Joins as well which can be found [here](https://bertwagner.com/posts/visualizing-nested-loops-joins-and-understanding-their-implications/)

![IndexedNestedLoop](/assets/images/IndexedNestedLoop.gif){: .dark .w-75 .normal }

### UnIndexed Nested Loop
I had to force this demo a little to show an unindexed nested loop. Its not a hugely efficient join type, but there are times SQL will choose to do this type over the others. I've forced this with a query hint LOOP JOIN which can be used to force it if needed.
```sql
SELECT TOP(1000)	 b.[BusinessEntityID]
					,b.[AddressID]
					,b.[AddressTypeID]
					,a.[name]
FROM				[AdventureWorks].[Person].[AddressType] a
INNER LOOP JOIN		[AdventureWorks].[Person].[BusinessEntityAddress] b
ON					a.addresstypeid = b.addresstypeid
```
![UnindexedNestedLoopPlan](/assets/images/UnindexedNestedLoopPlan.png){: .dark .w-75 .normal }

On the surface it looks fairly similar to the indexed nested loop other than an Index Scan rather than an Index Seek. This difference makes all the difference when it comes to performance. To see this lets look at the properties. Its read 41,068 rows to bring back 1000 thats 40,068 rows it didnt need to read to get to its needed rows. This will result in really bad performance on large tables. 

![UnindexedLoopJoinInner](/assets/images/UnindexedLoopJoinInner.png){: .dark .w-75 .normal }

Again Bert Wagner created a great visual which really shows how it works. Showing the unordered state and the extra work it needs to do. 
![UnindexedNestedLoop](/assets/images/UnindexedNestedLoop.gif){: .dark .w-75 .normal }