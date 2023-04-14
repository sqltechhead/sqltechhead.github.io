---
title: Big Query Storage Internals
date: 2023-04-14 00:00:00 +0000
categories: [Google Cloud, BigQuery]
---
## Introduction
Big Query by its purpose provides performant querying for large amounts of data. To get this performant querying it stores its data in Columnar format. Youre usual RDBMS system such as SQL Server by default stores its data by rows as row store enables quick 1 rows lookups that you would see in front end applications. BigQuerys column format works much better when lots of data needs to be returned and aggregations need to be performed. A good graphic can be seen below:

![BigQueryStorage](/assets/images/BigQueryStorage.png){: .dark .w-75 .normal }