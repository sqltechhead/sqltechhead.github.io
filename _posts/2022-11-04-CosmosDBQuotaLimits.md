---
title: CosmosDB Quota Limits
date: 2022-11-04 18:00:00 +0000
layout: post
categories: [NoSQL, CosmosDB]
---
## Introduction
Knowing your quota limits are very important when it comes to capacity planning, this page will act as a list of all those limits for database operations for easy reference. These tables come from the MSDN article which will be linked at the bottom of the page for a full list of quotas.

## Provisioned Throughput

| Resource	                                               | Limit       |
|:---------------------------------------------------------|------------:|
| Minimum RU/s required per 1 GB                           | 10RUs       |
| Maximum storage per container	                           | Unlimited   |
| Maximum storage across all items per (logical) partition | 20GB        |
| Maximum RUs per partition (logical & physical)	       | 10,000      |
| Maximum RUs per database	                               | 1,000,000   |
| Maximum RUs per container	                               | 1,000,000   |
| Maximum number of distinct (logical) partition keys	   | Unlimited   |
| Maximum attachment size per Account                      | 2GB         |

### Minimum Throughput Limits
Azure sets a minimum throughput you must provision of 400RU/s as a first step when creating a container. This is to ensure that there is enough provisioned. This is a huge estimation though and it is highly likely you will exceed this if you have a high throughput system. Azure just needs to set the minimum limit somewhere.

As your container size grows, so does the minimum RU limit. This shouldn’t be an issue for you as long as you are monitoring your size and load.

#### Dedicated Throughput
The minimum throughout is worked out by taking the maximum value of below:

- 400 RU/s
- Current Storage in GB * 10RU/s
- Highest RU/s ever provisioned on the container/100

So as an example if you have 1 database, 5 containers, 2TB worth of data in 1 container. You have provisioned 30,000 RU/s and havent ever provisioned higher than that, you would then be looking for the max of the below:

- 400RU/s
- (2,000GB * 10) = 20,000RU/s
- (30,000RU/s / 100) = 300RU/s

### Shared Throughput
On a shared throughput database one more equation is added:

- 400 + MAX(Container count – 25, 0) * 100 RU/s

So using the same example we would be looking for the maximum value of:

- 400RU/s
- (2,000GB * 10) = 20,000RU/s
- (30,000RU/s / 100) = 300RU/s
- 400 +(MAX(5,0) * 100 RU/s) = 400 +0 = 400RU/s

## Serverless Model
Serverless model is designed for workloads that arent always active and therefore provisioning constant throughput isnt needed. As such you will notice there are no minimum values for serverless

|Resource	                                               |Limit       |
|:---------------------------------------------------------|-----------:|
|Maximum RU/s per container	                               | 5,000      |
|Maximum storage across all items per (logical) partition  | 20GB       |
|Maximum storage per container	                           | 50GB       |

## Other Quota Limits
As always there are limits on many more things to ensure consistency and allow Cosmos to scale so well. There are limits on things like:

- Number of databases per account
- Number of containers per database
- Per container limits
- Per item limits

Microsoft as always has an extensive list of all these limits which can be found below.

<https://learn.microsoft.com/en-us/azure/cosmos-db/concepts-limits>