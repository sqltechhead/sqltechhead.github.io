---
title: Big Query Partitioned Tables
date: 2022-07-28 19:00:00 +0000
categories: [Google Cloud,BigQuery]
---
## Introduction
In BigQuery you can partition 3 ways:

- By time – A Time column within your table.
- Ingestion time – Partitioned by the timestamp of when the data was inserted into the table.
- By Integer – An integer column within your table.

## Partitioning Types
### Partitioning by time
When partitioned by time this can be done using 3 column types:

- Date – Can partition by day, month or year
- Timestamp – Can partition by hour, day, month or year
- Datetime – Can partition by hour, day, month or year

When data is written to your table, based on the date/time column data will be inserted into the correct partition based on your partition key column.

This will make your queries more performant if you are predicating by date. For example you have a 100 million row table and have partitioned by month. You want to bring back all the data where the month is 2022-07. Because you have partitioned on month, it means BigQuery can look straight at that partition, and that partition has 1 million rows, so now you only have to access 1 million rows rather than 100 million. This not only improves performance but will make for much less expensive queries and help your wallet too!

Its also good to note that when you partition by time there are 2 extra partitions created.

- __NULL__ – Contains all rows where the date/time column used to partition has come through as null
- __UNPARTITIONED__ – Contains rows where the value of the row is earlier or later than biqquery date defaults:
  + Earlier than 1960-01-01
  + Later than 2159-12-31

### Partitioning by ingestion time
This type of method uses an extra column created by bigquery. You can specify to partition again by hour, day, month or year.

Bigquery upon an insert will automatically grab the date time and place the row into the correct partition based upon the current datetime and the partition type you have chosen. This works very well if you want to partition by date but you don’t currently have a date column in your table.

### Partition by integer
Integer partitions obviously needs to work in ranges. There needs to be 4 things specified when configuring integer partitioning:

- Column name holding the integers to use
- Start range for the integers
- End range for the integers
- Interval within the range that should be partitioned by

For example you could want to partition the first 100 million rows of your table based on your ID column, however you want your partition size to be 1 million each, you would provide the below information:


| Column Name	|Start Range	|End Range	    |Interval |
|:--------------|:--------------|:--------------|--------:|
| ID	        |0	            |100,000,000	|1,000,000|

## Quotas and Limits
There are set limits defined by biqquery, when it comes to partitioned tables. The main ones can be found below, but BiqQuery have a good article on it here

|Limit	                                    |Default	 |Notes|
|:------------------------------------------|:--------------|:--------------|--------:|
Number of partitions per partitioned table	|4,000 partitions	|Each partitioned table can have up to 4,000 partitions. If you exceed this limit, consider using clustering in addition to, or instead of, partitioning.|
|Number of partitions modified by a single job	|4,000 partitions	|Each job operation (query or load) can affect up to 4,000 partitions. BigQuery rejects any query or load job that attempts to modify more than 4,000 partitions.|
|Number of partition modifications per ingestion-time partitioned table per day	|5,000 modifications	|Your project can make up to 5,000 partition modifications per day to an ingestion-time partitioned table.|
|Number of partition modifications per column-partitioned table per day	|30,000 modifications	|Your project can make up to 30,000 partition modifications per day for a column-partitioned table.|
|Number of modifications per 10 seconds per table	|50 modifications	|Your project can run up to 50 modifications per partitioned table every 10 seconds.|
|Number of possible ranges for range partitioning	|10,000 ranges	|A range-partitioned table can have up to 10,000 possible ranges. This limit applies to the partition specification when you create the table. After you create the table, the limit also applies to the actual number of partitions.|

As well as quotas at the table level there are also quotas at the job level, documentation can be found here to describe those quotas.