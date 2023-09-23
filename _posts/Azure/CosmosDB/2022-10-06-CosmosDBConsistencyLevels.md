---
title: CosmosDB Consistency Levels
date: 2022-10-18 13:30:00 +0000
layout: post
categories: [Microsoft Azure, CosmosDB]
---
## Introduction

Consistency is something that every database system needs to take into consideration in one form or another. SQL Server for examples follows the ACID principles (Atomicity, Consistency, Isolation, Durability). Cosmos is a little different. Because Cosmos is a distributed database consistency is actually the uniformity of data in the database. Cosmos can have Replicas across many regions, so the consistency levels work as an SLA against when data should be replicated and available in those regions.

The consistency models available are:

- Strong
- Bounded-Staleness
- Session
- Consistent Prefix
- Eventual

![ConsistencyLevels](/assets/images/ConsistencyLevels.png){: .dark .w-75 .normal }

## Strong
Strong consistency is the highest consistency level in Cosmos providing the lowest risk of data loss. With strong consistency Cosmos agrees that when a write occurs it will replicate that write against every region associated with your database.

This means that if a node was to be destroyed or have a catastrophic failure then we can be sure that no data has been lost as it is present on every other node. This does mean however, that writes can take a little longer, as for 1 write to be complete it needs to write to multiple regions and then circle back to confirm the write is successful. If regions are very far away from each other the latency can increase further. Its a big trade off, some applications need this latency and understand the lower throughput and higher latency.

## Bounded Staleness
In Bounded Staleness consistency, writes are written asynchronously. This means they occur in the background after a write is initially executed. This increases throughput as Cosmos does not have to wait for a successfully response from every node in every region, as this is done in the background.

Cosmos allows the configuring of a staleness window which can either be in time or number of writes, this is how it determines how to write the data asynchronously. As you can imagine this has a higher risk of data loss, as if a node goes down and it hasn’t written its data to another region then that data is lost. This must be thought of when choosing this consistency model.

## Session
Session consistency model is a little different, instead of being data centric it is Client centric. So, every client that is using the same session token reads will follow the Consistent Prefix model in the majority of cases. For exact behavior check the MS link below which explains it really well

<https://learn.microsoft.com/en-us/azure/cosmos-db/consistency-levels#session-consistency>

## Consistent Prefix
Consistent Prefix will guarantee that you will always see the order of writes. So, every region will need to have their writes written in the same order to ensure logical consistency. This is needed for a lot of applications such as messaging where you need to see the order of each message

## Eventual
Eventual Consistency is the lowest form of consistency but also provides the highest throughput. There are essentially no rules, writes will be written when they can with no order guarantees a lot of time, this consistency model is chosen when the application needs really high throughput and is willing to trade off everything else.

MS Explain all consistency models in the below link through the examples of musical notes. Its a really good page to keep handy and refer back to if you need it.

<https://learn.microsoft.com/en-us/azure/cosmos-db/consistency-levels>