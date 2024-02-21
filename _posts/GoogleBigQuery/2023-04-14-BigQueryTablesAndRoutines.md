---
title: Big Query Tables and Routines
date: 2023-04-14 00:00:00 +0000
categories: [Google Cloud, BigQuery]
---
## Introduction
BigQuery allows you to store and access data using things called Tables and Routines.
- Table - Much like any relational database stores your data in a table columnar format
- Routine - Think of the Programability Tab in SQL Server. Routines are User Definied functions and Procedures in Big Query

There are many different versions of tables and routines. They will be very familiar to you if you come from a SQL Server background. 

## Tables
### Managed Tables
These are your standard tables. They are backed and stored by the BigQuery Storage Engine and are the most common tables. Much like SQL Server they allow your to partition your data as well as cluster your tables to order them how you like. One the main benefits of Managed Tables that Google stress is the ability to use the Time Travel feature. This is a powerful feature that allows you to see your data at a specific point in time, while the actual real time data has already moved on. This allows for really powerfull analytics to be run on this data. There are a few different ways to create a table. Some are shown below

#### Create standard table
```sql
CREATE TABLE mydataset.newtable (
  a STRING,
  b STRING,
  c STRUCT<
    x FLOAT64
    y ARRAY<STRING>
  >
)
```
#### Create table from existing table
```sql
CREATE TABLE mydataset.top_words
OPTIONS(
  description="Top ten words per Shakespeare corpus"
) AS
SELECT
  corpus,
  ARRAY_AGG(STRUCT(word, word_count) ORDER BY word_count DESC LIMIT 10) AS top_words
FROM bigquery-public-data.samples.shakespeare
GROUP BY corpus;
```
#### Create table if not exists
```sql
CREATE TABLE mydataset.top_words
OPTIONS(
  description="Top ten words per Shakespeare corpus"
) AS
SELECT
  corpus,
  ARRAY_AGG(STRUCT(word, word_count) ORDER BY word_count DESC LIMIT 10) AS top_words
FROM bigquery-public-data.samples.shakespeare
GROUP BY corpus;
```

#### Create or replace table
```sql
CREATE OR REPLACE TABLE mydataset.newtable (x INT64, y STRUCT<a ARRAY<STRING>, b BOOL>)
OPTIONS(
  expiration_timestamp=TIMESTAMP "2025-01-01 00:00:00 UTC",
  description="a table that expires in 2025",
  labels=[("org_unit", "development")]
)
```


### External Table
If you're familiar with technologies like Databricks or Azure Synapse then an external table will also be familiar to you. This allows you to query other types of data as if you were querying normal SQL data. What i mean by this is you can have various different file types such as csv, avro, parquet, all stored in:
- Cloud Storage
- BigTable
- Google Drive

You can create an external table which references that data. This then allows you to query the data in bigquery as you would with your native BigQuery data. Its not as fast as querying data on native storage but really makes it flexible for you to work with all your data. 

```sql
CREATE EXTERNAL TABLE dataset.table 
OPTIONS (
  format = 'NEWLINE_DELIMITED_JSON',
  uris = ['gs://bucket/*.json']
);
```

### Views
#### Logical Views
Again similar to SQL Server Views are a virtual table of sorts. Views can be created to group rerunnable performant code, whereby you only have to provide access to the view and not the underlying tables. This allows you to really secure objects if this is needed. Logical views will execute the SQL Statement underneath at run time.

```sql

CREATE VIEW Test.TestView as (
    SELECT * 
    FROM Test.TestTable
    )
```

#### Materialized Views
Materialized views in contrast to logical views are computed in the background. This happenes everytime the data changes in the backgroun. Meaning that the data is always available. BigQuery also aims to improve performance further, any query that is run against the main table, BigQuery will check whether the materilized view can be used to bring data back faster and use that instead. There are limitations with these types of views however which can be found [here](https://cloud.google.com/bigquery/docs/materialized-views-intro#limitations)
```sql
CREATE MATERIALIZED VIEW project-id.my_dataset.my_mv_table AS
SELECT date, AVG(net_paid) AS avg_paid
FROM project-id.my_dataset.my_base_table
GROUP BY date
```

### Temporary Tables and CTEs
#### Temporary Tables
Temporary tables allow you to save results to a table. You can then use this table further down in your query as long as you keep it to the same session. They are sometimes preferred to CTEs dependant on your use case. Temporary tables are created once and then referenced, whereas CTEs are evaluated each time it is referenced
```sql
-- Find the top 100 names from the year 2017.
CREATE TEMP TABLE top_names(name STRING)
AS
 SELECT name
 FROM `bigquery-public-data`.usa_names.usa_1910_current
 WHERE year = 2017
 ORDER BY number DESC LIMIT 100
;
-- Which names appear as words in Shakespeare's plays?
SELECT
 name AS shakespeare_name
FROM top_names
WHERE name IN (
 SELECT word
 FROM `bigquery-public-data`.samples.shakespeare
);
```
More information on Temporary tables can be found [here](https://cloud.google.com/bigquery/docs/multi-statement-queries#temporary_tables)

#### CTEs
CTEs or Common Table Expressions are heavily used within SQL Server and are much the same in Big Query. In BigQuery you can have 2 types of CTE:
- Non Recursive CTE
- Recursive CTE

A Non Recursive CTE allows you to store a query and then call that query as can be seen below
```sql
WITH subQ1 AS (SELECT SchoolID FROM Roster),
     subQ2 AS (SELECT OpponentID FROM PlayerStats)
SELECT * FROM subQ1
UNION ALL
SELECT * FROM subQ2
```

A recursive subquery allows you to reference your subquery within your subquery. It is used for complex access patterns and is more of a programming technique so it s a really cool functionality to have.
```sql
WITH RECURSIVE
  T1 AS ( (SELECT 1 AS n) UNION ALL (SELECT n + 1 AS n FROM T1 WHERE n < 3) )
SELECT n FROM T1
```
To find out more about recursive CTEs you can find it [here](https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax#recursive_cte)

To really make your head hurt [this](https://www.geeksforgeeks.org/introduction-to-recursion-data-structure-and-algorithm-tutorials/) is a great page on recursion as a practice which helps you to understand what it is alot more. 

## Routines
### User Defined Function
User definied functions in BigQuery are used to reuse code where it is needed. You can create a UDF in:
- SQL
- Javascript

They take inputs and provide a single output, they are usually used to run complicated logic behind the scenes, things like regexes, string concatenation, string splitting, any kind of cleaning task works well with a UDF.

```sql
 CREATE OR REPLACE FUNCTION
  my_dataset.cleanse_string_test (text STRING)
  RETURNS STRING
  AS (REGEXP_REPLACE(LOWER(TRIM(text)), '[^a-zA-Z0-9 ]+', ''));
```

Google also provide an open source repo holding lots of precreated functions that you can use without writing them from scratch, these can be found below

<https://github.com/GoogleCloudPlatform/bigquery-utils/tree/master/udfs>

### Procedures
Procedures are much like their SQL Server counterpart. They can run any SQL syntax DDL,DML etc and allow you condense your code and neaten it rather than having pages and pages of scripts.

```sql
CREATE PROCEDURE dataset_name.procedure_name()
BEGIN
-- statements here
END
```