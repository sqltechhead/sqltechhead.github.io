---
title: CosmosDB Hierarchy
date: 2022-10-22 19:00:00 +0000
layout: post
math: true
categories: [NoSQL, CosmosDB]
---
## Introduction

As with any database system, there must be some kind of hierarchy behind it that allows grouping of resources together and allow for a smooth flow from the top to the bottom. Cosmos is no different its main hierarchy is:

- Database Account
- Database
- Container

Below is a great image from the MS documentation to show this model

![CosmosHierarchy](/assets/images/CosmosHierarchy.png){: .dark .w-75 .normal }

A Database Account is the account you first create in azure when you create a cosmos instance.

![CosmosHierarchy](/assets/images/CosmosHierarchy1.png){: .dark .w-75 .normal }

Then within a Database Account you can have multiple databases a database much like any other database language allows you to separate out functionality into its own repositories of sorts.

![CosmosHierarchy](/assets/images/CosmosHierarchy2.png){: .dark .w-75 .normal }

Then within Databases you can have multiple containers. Now think of containers as a namespace within your database, that allows you to further chunk up items.

![CosmosHierarchy](/assets/images/CosmosHierarchy3.png){: .dark .w-75 .normal }

If you look at our first visual on this page you can see that containers have many child properties underneath. Within a container you can have items obviously, but you can also have Triggers, Stored Procs and User Defined Functions to allow you to control and communicate with your data.

![CosmosHierarchy](/assets/images/CosmosHierarchy4.png){: .dark .w-75 .normal }

## Containers
Containers are where you set the majority of your control rules and where you control throughput. When you create a container you can set it up with either Dedicated Throughput or Shared Throughput.

Dedicated Throughput allows you to provision your container with a specific amount of RU/s, essentially allowing you to fine tune your load at a container level. At that level you can also enable standard or autoscale, allowing you to further configure whether or not the throughput should autoscale if it is reached.

Shared Throughput is set at a database level. You set the throughput/RU setting that you would like that database to have, then dependant on the amount of containers you have underneath, the container value is a division of the database limit. For example:

- Database Throughput – 1000RU/s
- Container Throughput – 4 Containers under the database @250RU/s reach

## System Defined Properties
Both containers and items have system defined properties, these can be likened to SQL properties you’ll find in its base tables. These are used for identification in parts but also allows for viewing key settings set at a container or item level. The below visuals are taken from the MS documentation and list the available properties.

## Container Properties

| System-defined property| System-generated or user-configurable|Purpose	|API for NoSQL|API for Cassandra|API for MongoDB|API for Gremlin|API for Table|
|:-----------------------|:-------------------------------------|:----------|:------------|:----------------|:--------------|:--------------|:-----------:|
|_rid	                 |System-generated	|Unique identifier of container	|Yes	|No	|No|	No|	No|
|_etag	                 |System-generated	|Entity tag used for optimistic concurrency control	|Yes	|No	|No	|No	|No|
|_ts	                 |System-generated	|Last updated timestamp of the container	|Yes	|No	|No	|No	|No|
|_self	                 |System-generated	|Addressable URI of the container	|Yes	|No	|No	|No	|No|
|id	                     |User-configurable	|Name of the container	|Yes	|Yes	|Yes	|Yes	|Yes|
|indexingPolicy	         |User-configurable	|Provides the ability to change indexes	|Yes|	No|	Yes|	Yes|	Yes|
|TimeToLive	             |User-configurable	|Provides the ability to delete items automatically from a container after a set time period. For details, see Time to Live.	|Yes|	No|	No|	No|	Yes|
|changeFeedPolicy	     |User-configurable	|Used to read changes made to items in a container. For details, see Change feed.	|Yes|	No|	No|	No|	Yes|
|uniqueKeyPolicy	     |User-configurable	|Used to ensure the uniqueness of one or more values in a logical partition. For more information, see Unique key constraints.	|Yes	|No	|No	|No	|Yes|
|AnalyticalTimeToLive	 |User-configurable	|Provides the ability to delete items automatically from a container after a set time period. For details, see Time to Live.	|Yes	|No	|Yes	|No	|No|