---
title: Projections in Clickhouse
date: 2025-09-26 13:30:00 +0000
layout: post
categories: [Clickhouse, Internals]
---
# Projections in ClickHouse

**Projections** are a performance optimization feature in ClickHouse that allow you to store alternative representations of your table data — similar in concept to materialized views, but with key differences in how they are stored and maintained.

* * *

## What Are Projections?

*   A **projection** is a physical subset of a table’s data, stored with a different **sort order**, **column selection**, or **aggregation**.
*   Unlike materialized views, projections are stored **within the same part** as the source table. This means they share the same storage lifecycle and are tightly coupled with the base table’s data.
*   Projections are defined as part of the table schema and are automatically maintained by ClickHouse.

* * *

## How Projections Work

*   When new data is inserted into the source table, the projection is automatically populated as part of the same write operation.
*   If data is **mutated** (e.g., via `ALTER TABLE ... DELETE` or `UPDATE`), the changes are **propagated to the projection** as well.
*   Projections are **read-only** — you cannot directly modify or update them independently of the base table.
*   The **query optimizer** can automatically choose to use a projection instead of the base table if it determines that doing so will improve query performance.

* * *

## Limitations

*   **Schema changes** to projections are not supported. Once a projection is created, it cannot be altered — you would need to drop and recreate it.
*   Projections are not suitable for all use cases. They are most effective when:
    *   Queries frequently filter or aggregate on a specific subset of columns.
    *   A different sort order can significantly reduce scan time.
    *   You want to optimize performance without maintaining a separate materialized view.

* * *

## Use Cases


*   Accelerating analytical queries that use different sort orders or aggregations than the base table.
*   Reducing I/O by precomputing and storing frequently accessed subsets of data.
*   Improving performance without the overhead of managing separate materialized views.