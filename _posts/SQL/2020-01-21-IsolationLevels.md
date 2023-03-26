---
title: Isolation Levels
date: 2020-01-21 07:33:00 +0000
layout: post
categories: [SQL, SQLIndexing]
---

## Introduction
Books online describes Isolation Levels as “SQL Server isolation levels are used to define the degree to which one transaction must be isolated from resource or data modifications made by other concurrent transactions”. Each isolation level can be thought of as a set of rules related to how locks and transactions act within SQL Server. There are 4 isolation levels:

- Read Uncommitted
- Read Committed
- Repeatable Read
- Snapshot
- Serializable
- Read Committed Snapshot

## Issue Prevention
Before we start talking about the isolation levels, i think its a good idea to outline, some SQL issues each level allows or prevents.

### Dirty Reads
A Dirty Read is a read which is carried out on uncommitted data.

```sql
--Session 1
CREATE TABLE dbo.DirtyReads 
(ID INT)
 
BEGIN TRANSACTION
INSERT INTO dbo.DirtyReads 
VALUES (1)
```
```sql
--Session 2
BEGIN TRANSACTION
 
SELECT * 
FROM dbo.DirtyReads 
 
COMMIT TRANSACTION
```

As you can see Session 1 has begun a transaction and inserted into a table, but it has not committed the transaction. If Session 2 is able to read to read ID 1 from the table then it is carrying out a dirty read. Dirty reads arent ideal, because session 1 could always error and rollback, which means session 2 has brought back non existent data

### Phantom Reads
A phantom read is a read which is carried out and get x results, then queried again in the same transaction and get y results. To demonstrate:

```sql
--Session 1
CREATE TABLE dbo.PhantomReads
(ID INT)
INSERT INTO dbo.PhantomReads
VALUES (1),(2),(3),(4)
 
BEGIN TRANSACTION
SELECT * 
FROM dbo.PhantomReads
 
WAITFOR DELAY '00:00:10.000'
 
SELECT * 
FROM dbo.PhantomReads
```

```sql
--Session 2
 
BEGIN TRANSACTION
 
INSERT INTO dbo.PhantomReads
VALUES (5)
 
COMMIT TRANSACTION
```
Here Session 1 will run. It will begin a transaction and select from dbo.PhantomReads, it will then wait for 10 seconds. During that 10 seconds session 2 will run and insert an extra row into the table. When session 1 carries out the second select it will have an extra record, which is the “phantom read”.

![Phantom Reads](/assets/images/IsolationLevels1.png){: .dark .w-75 .rounded-10 .normal }

### Non-Repeatable Read
You will notice a non-repeatable read is similar to a phantom read, the only difference is that it is an update rather than an insert.

```sql
--Session 1
CREATE TABLE dbo.NonRepeatableRead
(ID INT)
INSERT INTO dbo.NonRepeatableRead
VALUES (1),(2),(3),(4)
 
BEGIN TRANSACTION
SELECT * 
FROM dbo.NonRepeatableRead
 
WAITFOR DELAY '00:00:10.000'
 
SELECT * 
FROM dbo.NonRepeatableRead
 
COMMIT TRANSACTION
```
```sql
--Session 2
 
BEGIN TRANSACTION
 
UPDATE dbo.NonRepeatableRead
SET ID = 4
WHERE ID = 1
 
COMMIT TRANSACTION
```

Session 1 will start and select from NonRepeatable read table. It will then wait for 10 seconds. During that 10 seconds session 2 will update id 1 to = 4. Session 1 will then query the table again and have a different value for id 1. You will now have 2 ids of 4. Hence a non-repeatable read.

![Non Repetable Reads](/assets/images/IsolationLevels2.png){: .dark .w-75 .normal }

### Concurrent Update Errors
Concurrent update errors can occur in the snapshot isolation level. The jist of it is that 2 transactions can come along and update data based on a point in time snapshot of the data, so when they come to commit their transaction they have 2 different versions of the story. 1 transaction cannot complete, because the data is inconsistent. 1 Transaction will then error.

```sql
-Session 1
CREATE TABLE dbo.ConcurrentUpdates
(Seconds INT)
INSERT INTO dbo.ConcurrentUpdates
VALUES (60)
 
 
BEGIN TRANSACTION
SELECT * 
FROM dbo.ConcurrentUpdates
 
WAITFOR DELAY '00:00:05.000'
 
UPDATE dbo.ConcurrentUpdates
SET Seconds = Seconds - 5
 
UPDATE dbo.ConcurrentUpdates
SET Seconds = Seconds - 5
 
SELECT * 
FROM dbo.ConcurrentUpdates
COMMIT TRANSACTION
```
```sql
--Session 2
BEGIN TRANSACTION
SELECT * 
FROM dbo.ConcurrentUpdates
 
WAITFOR DELAY '00:00:10.000'
 
UPDATE dbo.ConcurrentUpdates
SET Seconds = Seconds - 1
 
UPDATE dbo.ConcurrentUpdates
SET Seconds = Seconds - 1
 
SELECT * 
FROM dbo.ConcurrentUpdates
COMMIT TRANSACTION
```
Session 1 will start it will pull back records from the table. It will then wait for 5 seconds. Next session 2 will start and pull back records from the table and wait for 10 seconds. Session 1 will now update the table and reduce the number of seconds by 5 and 5 again. Session 2 will then try and reduce the number by 1 and 1 again. You will be given the below error on session 2. This is because each session has taken a snapshot of the rows. It cant ensure that the rows are consistent because there are now 2 versions being changed, so 1 has to fail to ensure consistency.

> Msg 3960, Level 16, State 6, Line 8
Snapshot isolation transaction aborted due to update conflict. You cannot use snapshot isolation to access
 table 'dbo.ConcurrentUpdates' directly or indirectly in database '' to update, delete, or insert 
the row that has been modified or deleted by another transaction. Retry the transaction or change the isolation level 
for the update/delete statement.
{: .prompt-danger }

## Isolation Levels
### Read Uncommitted
This isolation level specifies that queries can read uncommitted data from another transaction. This is similar to the with(nolock) query hint. When under this isolation level the database does not issue shared locks. Meaning there will be no contention with any other locks, hence being able to read uncommitted data. This is the least restrictive isolation level and subjects querys to:

- Dirty Reads
- Phantom Reads
- Non Repeatable Reads

### Read Committed
This is the most common isolation level. Under this level queries cannot read data that has been modified by another transaction but not yet committed. This prevents dirty reads. However data can still be modified in between issuing statements in a transaction. Because of this, queries are still subjected to:

- Phantom Reads
- Non- Repeatable Reads

### Read Committed Snapshot

This is a very cool isolation level and can really help with systems with highly concurrent reads. This isolation level utilizes tempdb and its version store. When data modifications occur. The old version of the row is stored in tempdb’ version store, then SQL will go ahead and modify the data. What this means is that Select statements are not blocked during this, queries will read data from the version store. So if multiple selects and a data modification occur on 1 table at once, the selects wont be blocked they will read the current data and the data modification can also update it. This can cause data to be slightly out of date so you need to ensure you know your system before implementing this. One other thing to watch out for is that on a highly concurrent system, tempdb’ version store can fill up because of the all the data modifications, so ensure your system is sized correctly.

### Repeatable Read
In this isolation level a query cannot read data currently being modified by another transaction. As well as that no transactions can modify data currently being read by another transaction. This prevents dirty reads as well as Non Repeatable reads. However it is still subject to:

- Phantom Reads
- Snapshot
A query can use data only if it will be consistent throughout. If a second transaction modifies data after the first transaction has started, the first transaction will ignore it, it runs off a snapshot of data at time of starting. They do not request locks when reading data, they also do not block other transactions from updating the data. They prevent dirty reads, Non-Repeatable reads and phantom reads. However they are subject to concurrent update errors.

### Serializable
A query under this isolation level cannot read data currently being modified by another transaction. No transactions can modify data currently being modified by another transaction. Serializable only allows one thread at time to access data, because of this they prevent dirty reads, non-repeatable reads and phantom reads