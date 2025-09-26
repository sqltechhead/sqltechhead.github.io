---
title: Managing data in Clickhouse
date: 2025-09-26 13:30:00 +0000
layout: post
categories: [Clickhouse, Internals]
---

# Compression & TTL

ClickHouse offers several mechanisms to optimize storage and lifecycle management of data. Two key features are **column-level compression** and **TTL policies**, which help reduce disk usage and automate data retention or transformation.

* * *

## Compression

ClickHouse supports multiple compression algorithms that can be applied **per column**, allowing fine-grained control over storage efficiency and query performance.

### Common Compression Modes

Refer to the official documentation for a full list:  
[Compression Modes | ClickHouse Docs](https://clickhouse.com/docs/data-compression/compression-modes)
*   **`lz4`**: Fast and efficient with low CPU overhead, but offers a lower compression ratio.
*   **`lz4hc`**: High-compression variant of `lz4`, offering better compression at the cost of slower performance.
*   **`zstd`**: Provides higher compression ratios than `lz4`, but is slower and may impact query performance.

### Optimization Tip
> If a column has fewer than **10,000 unique values**, consider using LowCardinality()
{: .prompt-tip }

```sql
LowCardinality(column_name)
```
This stores the column as a dictionary-encoded structure in memory, reducing storage and improving performance for filtering and grouping operations. It actually stores the string values as integer representations which is alot more compressable.

### Measuring Compression Efficiency

You can inspect compression statistics using the following query:
```sql
SELECT 
    name,
    formatReadableSize(data_compressed_bytes) AS compressed,
    formatReadableSize(data_uncompressed_bytes) AS uncompressed
FROM system.columns
WHERE table = 'your_table_name'
```

This helps identify which columns benefit most from compression and where further tuning may be needed.

* * *

## TTL (Time-To-Live)

TTL rules in ClickHouse allow you to **automatically expire, move, or aggregate data** based on time conditions. TTL can be applied at the **table**, **partition**, or **column** level.

### Table-Level TTL Example

Automatically delete rows 1 month after their timestamp:
```sql
CREATE TABLE ...
ENGINE = MergeTree
ORDER BY ...
TTL timestamp_column + INTERVAL 1 MONTH
```

* * *

### Moving Data Between Volumes (Non-Cloud Only)

You can use TTL to move older data to a different disk volume (e.g., from hot to cold storage):
```sql
CREATE TABLE ...
ENGINE = MergeTree
PARTITION BY toYYYYMM(timestamp)
ORDER BY ...
TTL timestamp + INTERVAL 1 MONTH TO VOLUME 'cold_volume',
    timestamp + INTERVAL 12 MONTH
```

> This feature is not supported in ClickHouse Cloud.

* * *

### Rolling Up Old Data

TTL can also be used to **aggregate** older data into summaries:
```sql
CREATE TABLE ...
ENGINE = MergeTree
PARTITION BY toYYYYMM(timestamp)
ORDER BY ...
TTL timestamp + INTERVAL 12 MONTH GROUP BY sum_x = SUM(x)
```

This is useful for long-term storage where detailed granularity is no longer needed.

* * *

Summary
---------

| Feature | Purpose | Best Use Case |
| --- | --- | --- |
| Compression | Reduce disk usage | Columns with repetitive or large data |
| LowCardinality | Optimize low-cardinality columns | Categorical fields with <10k values |
| TTL Delete | Auto-expire old data | Time-based retention policies |
| TTL Volume | Move data to cold storage | Tiered storage (non-cloud) |
| TTL Rollup | Aggregate old data | Long-term summaries |