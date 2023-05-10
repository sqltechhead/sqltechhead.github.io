---
title: SQL Server Merge Join
date: 2023-04-22 07:33:00 +0000
layout: post
categories: [SQL, SQLPerformance]
---

## Introduction
A Merge join is another physical join type SQL uses to join 2 datasets together. Now within the SQL community alot of time it is thought of as the most efficient join type. This isnt always the case. It is true that the Merge Join is the fastest join type if you have the correct dataset for it to use. But if you don't it can quickly become a very bad join type, as it is with all join types, theres no 1 size fits all which is why SQL has multiple for the optimizer to use but also for you as a DBA to use yourself if you know what you're doing. 

## Merge Joins
Now 1 thing to keep in mind. A merge join needs its data sorted exactly the same way to be used. This is either done by using an existing index, or SQL will add a sort operator to the plan and sort it the way it needs it. 

