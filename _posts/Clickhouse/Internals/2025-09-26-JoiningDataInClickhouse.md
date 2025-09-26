---
title: Joining data in Clickhouse
date: 2025-09-26 13:30:00 +0000
layout: post
categories: [Clickhouse, Internals]
---

# Joining Data in ClickHouse

ClickHouse supports multiple join algorithms, each optimized for different use cases and memory constraints. Understanding how these joins work is essential for writing efficient queries, especially when working with large datasets.

* * *

## Key Considerations Before Joining

*   **Memory usage**: Some join types require the entire right-hand table to fit in memory.
*   **Table size**: The right-hand table (the one being joined) should ideally be smaller.
*   **Performance trade-offs**: Faster joins often require more memory or pre-sorted data.

* * *

## Join Algorithms Overview

### 1. **Hash Join**

*   The **default** and most commonly used join type.
*   The **right-hand table** is fully loaded into memory and hashed.
*   The **left-hand table** is scanned and matched against the hash.
*   **Best used when** the right-hand table is small enough to fit in memory.
🧠 _Tip: Always place the smaller table on the right side of the join._

* * *

### 2. **Parallel Hash Join**

*   Functions like a standard hash join but uses **parallel processing** to improve performance.
*   Can significantly reduce join time on large datasets with sufficient compute resources.

* * *

### 3. **Grace Hash Join**

*   Designed for **low-memory environments**.
*   Splits data into partitions and performs the join in stages.
*   **Slower** than hash joins but more memory-efficient.

* * *

### 4. **Partial Merge Join**

*   The **most memory-efficient** but also the **slowest** join type.
*   Performs a merge join on partially sorted data.
*   Useful as a fallback when memory is extremely limited.

* * *

### 5. **Full Sorting Merge Join**

*   Requires **both tables to be sorted** on the join key.
*   Offers **fast performance** when this condition is met.
*   Ideal for joining large, pre-sorted datasets.

* * *

### 6. **Direct Join**

*   Used when the right-hand table is **fully loaded into memory**, such as a **dictionary**.
*   Enables **fast lookups** and is ideal for joining against small, static reference tables.

* * *

## Example: Forcing a Join Algorithm

You can explicitly specify the join algorithm using the `SETTINGS` clause:

```sql
SELECT *
FROM TABLE 
JOIN TABLE
SETTING joinalgorithm = 'hash'
```

Available options include:
*   `'hash'`
*   `'parallel_hash'`
*   `'grace_hash'`
*   `'partial_merge'`
*   `'full_sorting_merge'`
*   `'direct'`

* * *

## Best Practices

*   Always **benchmark** different join strategies when working with large datasets.
*   Use **`EXPLAIN`** to inspect the query plan and verify which join algorithm is being used.
*   Consider **pre-sorting** tables or using **projections** to optimize merge joins.
*   For small reference data, consider using **dictionaries** for direct joins.