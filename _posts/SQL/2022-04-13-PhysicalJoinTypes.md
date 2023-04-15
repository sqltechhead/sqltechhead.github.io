---
title: SQL Server Physical Join Types
date: 2023-04-13 07:33:00 +0000
layout: post
categories: [SQL, SQLPerformance]
---

## Introduction
Lets debunk join types slightly before we get into the chunk of the post. In SQL Server there are Logical and Physical join types. Logical join types include the below TSQL Syntax':
- Inner Join
- Left Join
- Right Join
- Cross Join

Whereby physical join types are what you will see in Query Execution plans and include:
- Loop Join
- Merge Join
- Hash Join
- Adaptive Join

## Loop Joins
