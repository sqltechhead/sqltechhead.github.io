---
title: Big Query Getting Started
date: 2022-07-22 19:00:00 +0000
categories: [Google Cloud, BigQuery]
---
## Introduction
Getting started with Bigquery is relatively easy. If you have come with no prior knowledge at all then Google provides you with a free way to practice on BigQuery. They provide a sandbox account where you can import datasets as well as query to test your skills and learn more about Big Query. Follow the below link to set up your sandbox account.

<https://cloud.google.com/bigquery/docs/sandbox>

Once done have a little look around the UI, its fairly simple and you will be able to figure out what most things do just by looking at them.

![BigQuery](/assets/images/BigQueryGettingStarted.png){: .dark .w-75 .normal }

First lets play around with loading some data from one of googles public datasets.

Go to Add Data > Explore Public Datasets

![BigQuery](/assets/images/BigQueryGettingStarted1.png){: .dark .w-75 .normal }

You’ll find a wide range of datasets to choose from, we are going to look at the covid 19 dataset.

![BigQuery](/assets/images/BigQueryGettingStarted2.png){: .dark .w-75 .normal }

Click the dataset and then select View Dataset.

On the view page look for the dataset id, we are going to want to search for that dataset id in the search bar to the left. If 0 results come up there should be a link next to it to say Broaden Search to all projects click that and search again.

![BigQuery](/assets/images/BigQueryGettingStarted3.png){: .dark .w-75 .normal }

![BigQuery](/assets/images/BigQueryGettingStarted4.png){: .dark .w-75 .normal }

Now looking at the above you can see the hierarchy.

- bigquery-public-data – This is the project
- covid19_open_data – This is the dataset
- covid19_open_data – This is the table

Click on the ellipsis next to the table and then select query. Here this will present you with an example query for how to query the table. It shows you how to write the table name in a query as Project.Dataset.Table.

![BigQuery](/assets/images/BigQueryGettingStarted5.png){: .dark .w-75 .normal }

Notice it also shows you how much the query will cost you in GB in top right.

Run the query and you will be presented with the query results in the box below.

![BigQuery](/assets/images/BigQueryGettingStarted6.png){: .dark .w-75 .normal }

You have now run your first query on Google Big Query!