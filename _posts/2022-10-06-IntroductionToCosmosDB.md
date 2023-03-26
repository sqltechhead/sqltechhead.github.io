---
title: Introduction To CosmosDB
date: 2022-10-06 15:30:00 +0000
layout: post
categories: [NoSQL, CosmosDB]
---
## Introduction

Cosmos DB is a managed noSQL product by Microsoft Azure, because it is managed it means that the administration of the product is very little to none, which is highly attractive to majority of companies. Allowing DBAs to concentrate more on tuning systems and writing code without the time consuming administration is a big win.

CosmosDB provides millisecond response time and instantly scalable infrastructure. Using the standard JSON document model of noSQL databases it allows indexes of all properties to enable faster queries.

As well as that it offers a really cool functionality. It provides multiple different APIs for you to communicate with CosmosDB such as:

- Standard SQL (Default)
- API for MongoDB
- API for Cassandra
- API for Gremlin
- DB Table

For example if you already have a MongoDB codebase in your company, you can use that same codebase and communicate with Cosmos, meaning you can communicate with Mongo and Cosmos in the same way reducing code. This is really cool and makes it really attractive to customers who want to do that. The default API is SQL which is where new customers to noSQL come in at.

Azure Cosmos DB is a fully managed NoSQL database for modern app development.

![IntroductionToCosmosDB](/assets/images/IntroductionToCosmos.png){: .dark .w-75 .normal }

CosmosDB scales horizontally which gives it the speed when querying data, what that means is Cosmos scales by increasing the worker nodes for the databases, increasing processing power and increasing performance along with it.

To carry out this horizontal scaling CosmosDB uses partitioning, you create a partition key, and dependent on that key Cosmos will scale the data out across its worker nodes. When you get your partitioning key right, this allows for huge performance benefits as the data is split out across the nodes and allows point reads when predicating by partition key.

Microsoft have an amazing youtube series on Azure CosmosDB Essentials, i would highly recommend taking a watch and skilling up.

<https://www.youtube.com/playlist?list=PLLasX02E8BPDd2fKwLCHnmWoyo4bL-oKr>