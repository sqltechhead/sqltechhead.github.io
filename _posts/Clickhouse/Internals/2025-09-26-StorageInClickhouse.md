---
title: Storage in Clickhouse
date: 2025-09-26 13:30:00 +0000
layout: post
categories: [Clickhouse, Internals]
---
# Parts & Granules in ClickHouse


In ClickHouse, a **Part** (short for partition) is a unit of table data stored on disk. Each part is saved in its own folder. During ingestion, each batch of data is compressed, indexed, and saved as a new **Part**. The structure of a part is outlined below:
*   **`ColumnName.bin`**: A compressed columnar data file for each column in the table. These files are further divided into **granules**, each containing up to 8192 rows — similar to row groups in Parquet files.
    
*   **`Primary.idx`**: An index file that stores the primary key for the first row of each granule. This index is kept in memory and is sorted for efficient access.
    
![Clickhouse1](/assets/images/Clickhouse1.png){: .dark .w-75 .normal }

##Notes:

*   When querying a table using a filter on the primary key, ClickHouse uses `Primary.idx` to identify which parts or granules contain relevant data.
*   If filtering by the primary key isn't possible and no other indexes exist, ClickHouse must scan the entire table.
*   A **granule** is the smallest unit of data that can be read. Since each granule contains up to 8192 rows, reading even a single row requires reading the entire granule.

* * *

# Real-Time Ingestion and Merging


When ingesting data in real time, ClickHouse continuously creates new parts. These parts are typically small, resulting in a large number of files. Since processing many small files can degrade performance, ClickHouse runs a background process that merges adjacent parts into larger ones. This continues until parts reach a maximum size of approximately **150 GB** (several billion rows). Old files are deleted as part of this background optimization.

![Clickhouse2](/assets/images/Clickhouse2.png){: .dark .w-75 .normal }

## Notes:

*   The default table engine in ClickHouse is the **MergeTree** engine, named after this merging strategy.
*   Ingesting data in very small batches is inefficient, as these small parts will need to be merged later. To improve performance, consider using the **async insert** feature for small inserts. This buffers data in memory and flushes it to disk when:
    *   The buffer reaches a configured size (`async_insert_max_data_size`)
    *   A configured time interval has passed (`async_insert_busy_timeout_ms`)
*   ClickHouse attempts to merge **contiguous** datasets. However, documentation is vague on what qualifies as "contiguous." Understanding this behavior is important, as it may influence how you design your primary key.