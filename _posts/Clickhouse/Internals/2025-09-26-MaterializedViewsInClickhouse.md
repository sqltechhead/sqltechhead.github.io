---
title: Materialized Views in Clickhouse
date: 2025-09-26 13:30:00 +0000
layout: post
categories: [Clickhouse, Internals]
---

# Materialized Views in ClickHouse

Materialized views in ClickHouse allow you to store data in a separate table with a different **sort order**, **primary key**, **aggregation**, or **structure**. They are automatically updated in near real-time based on changes to the source table.

##How They Work

*   Data is **pushed** from the source table to the materialized view whenever new data is inserted or existing data is modified.
*   The **source table** is defined by the `FROM` clause in the materialized view's query. Only inserts into this table will trigger updates to the materialized view.
*   **Deletes and updates** in the source table are **not** propagated to the materialized view.
*   Other tables referenced in the query (e.g., via joins) will not trigger updates if they change.

* * *

## Syntax

The simplest way to create a materialized view is:

```sql
        CREATE MATERIALIZED VIEW name
	ENGINE = name
	ORDER BY field
	POPULATE AS 
	SELECT .. 
        FROM .. 
        GROUP BY ...
```

> **Note:** This approach is not recommended for production use, as it makes schema changes difficult.  
> **Best practice:** Define the target table separately and use the `TO` clause:

* * *

### Common Engines for Materialized Views

#### `ReplacingMergeTree`

*   Used to **deduplicate** versioned data.
*   Retains only the **latest version** of a row based on a version column (if defined) or insertion order.

#### `CollapsingMergeTree`

*   Supports **asynchronous deletion** of rows using a special `Sign` column.
*   Pairs of rows with the same sorting key but opposite `Sign` values (`1` and `-1`) are collapsed (i.e., deleted).
*   Rows without a matching pair are retained.
**Example:**


``` sql
     CREATE TABLE UAct  
     (ContactID UInt64,  
     BookID UInt64
     Sign Int8  
     )  
    ENGINE = CollapsingMergeTree(Sign)  
    ORDER BY USerAccountID, ContactID
```

If a row is inserted with `Sign = 1` and later another with the same key and `Sign = -1`, the pair will be removed asynchronously.

#### `VersionCollapsingMergeTree`

*   Similar to `CollapsingMergeTree`, but allows you to define a **custom versioning column**.
*   Useful when versioning is based on a user-defined field rather than ingestion time.

* * *

Let me know if you'd like this formatted for a specific platform (e.g., Markdown, Confluence, Azure DevOps Wiki) or combined with other documentation!