---
title: Indexing in Clickhouse
date: 2025-09-26 13:30:00 +0000
layout: post
categories: [Clickhouse, Internals]
---

# Data Skipping in ClickHouse

ClickHouse provides several powerful features to **skip unnecessary data** during query execution, significantly improving performance by reducing I/O and memory usage.
Some of these techniques have already been mentioned, such as:
*   **Projections**: Define alternative sort orders or column subsets to optimize query paths.
*   **Aggregated Views**: Use projections or materialized views to pre-aggregate data and reduce the volume scanned at query time.
In addition to these, ClickHouse supports **data skipping indexes**, which help the query engine avoid reading blocks of data that are guaranteed not to match the query conditions.

* * *

## Data Skipping Index Types

### 1. **MinMax Index**

*   Stores the **minimum and maximum values** for a specified column within each data block.
*   During query execution, ClickHouse compares the query predicate to these min/max values to determine whether a block can be skipped.
*   **Best for**: Range queries on numeric or date fields.

* * *

### 2. **Set Index**

*   Stores a **set of unique values** for a column within each block.
*   If the query condition references a value not present in the set, the block can be skipped.
*   **Best for**: Columns with low to medium cardinality (e.g., status codes, categories).

* * *

### 3. **Bloom Filter Index**

*   Uses a **probabilistic data structure** to test whether a value might exist in a block.
*   May produce **false positives**, but never false negatives — meaning some unnecessary blocks might be read, but no relevant data will be missed.
*   **Best for**: High-cardinality fields (e.g., UUIDs, email addresses) where exact matching is required.

> Bloom filters are space-efficient but should be used when the indexed expression is **expected to match**. If the condition is rarely true, false positives can lead to unnecessary reads.

* * *

## What Is a “Block”?

In the context of skipping indexes:
*   A **block** refers to a group of rows within a part.
*   The size of a block is determined by:
    *   The **granule size** (default: 8192 rows).
    *   The **index granularity** setting (e.g., 4).
*   For example, with a granule size of 8192 and granularity of 4, each indexed block contains **32,768 rows**.

* * *

## Summary of Use Cases

| Index Type | Best For | Pros | Cons |
| --- | --- | --- | --- |
| MinMax | Range filters on numeric/date | Fast, simple, low overhead | Not effective on unordered data |
| Set | Low/medium cardinality fields | Accurate, efficient | Larger memory footprint |
| Bloom Filter | High-cardinality exact matches | Space-efficient, flexible | May read unnecessary blocks |