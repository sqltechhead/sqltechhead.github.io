---
title: Passing Complex Objects To Job Matrix
date: 2023-05-10 18:00:00 +0000
layout: post
categories: [Azure, YamlPipelines]
---
## Introduction
Using a job matrix in YAML pipelines is a really powerful tool to enable you to run parallel deploys with different variable values. Use cases include:
- Running MSBuild in parralel against multiple configurations with no extra code
- Running Deploys against multiple different environments 
- Running Deploys against different regions in Azure
- Restarting VMs in Azure in parralel

## Matrix Basics
MSDN has a good starter document to go through the basic syntax and how to use a matrix

<https://learn.microsoft.com/en-us/azure/devops/pipelines/yaml-schema/jobs-job-strategy?view=azure-pipelines>

The basic and most common declaration is within a job and can be done as below. 
```yaml
jobs:
- job: Build
  strategy:
    matrix:
```

A matrix can be defined in a very similar way to a complex object. So lets use MSBuild as an example, with MSBuild usually you will have a debug and a release configuration. Debug for testing and release for production. You could set you matrix as below

```yaml
jobs:
- job: Build
  strategy:
    matrix:
      debug:
        Configuration: debug
      release:
        Configuration: Release
```

You set the matrix with 2 properties debug and release. Within those properties you can set variables to be used. We set configuration to be debug and release in each. So lets try and visualise it now within the pipeline. The below pipeline code will show a basic matrix in action.

```yaml
trigger: none

pool:
  vmImage: ubuntu-latest

jobs:
  - job: Build 
    strategy:
     matrix: 
       debug:
         Configuration: debug
       release:
         Configuration: release
    steps:
    - script: echo 'Building $(Configuration) Configuration.'
      displayName: Building $(Configuration) Configuration
```
As you can see in the below screenshot with this simple yaml code we have now been able to create 2 parralel jobs to run.

![MatrixExample](/assets/images/MatrixExample.png){: .dark .w-75 .normal }

## Passing Complex Objects to matrix
As well as defining a matrix as above, in some cases pipelines can get complicated and we may need to repeat certain matrixes across lots of jobs. Instead of repeating matrix code across multiple jobs we can actually define it as a parameter and then pass it into the matrix dynamically this allows code reuse and neatens up yaml code a hell of alot. The best thing is, its super easy. Take a look below

```yaml
trigger: none

pool:
  vmImage: ubuntu-latest

parameters:
  - name: matrix
    type: object
    default:
        debug:
          Configuration: debug
        release:
          Configuration: release

jobs:
  - job: Build 
    strategy:
     matrix: ${{ parameters.matrix }}
    steps:
    - script: echo 'Building $(Configuration) Configuration.'
      displayName: Building $(Configuration) Configuration
```

## Changing the maximum number of parallel executions 
Another key feature of a matrix is being able to set the number of max parallel threads that occur at once. This can be really useful in scenarios such as restarting VMs where you only want a certain number off at a time or other scenarios where you want to control the number of executions. We have changed our example to be a restarting server example as below, with a max parralel of 1:

```yaml
trigger: none

pool:
  vmImage: ubuntu-latest

parameters:
  - name: matrix
    type: object
    default:
        local:
          servername: local01
        staging:
          servername: staging01
        development:
          servername: development01
        production:
          servername: production01

jobs:
  - job: RestartServer 
    strategy:
     matrix: ${{ parameters.matrix }}
     maxParallel: 1
    steps:
    - script: echo 'Restarting $(servername).'
      displayName: Restarting $(servername)
```
As you can see from the below screenshots each job executes and waits until the previous job has completed to continue. This allows you to only have 1 server off at a time but still use a matrix to really promote code reuse. 

![MatrixExample1](/assets/images/MatrixExample1.png){: .dark .w-75 .normal }
![MatrixExample2](/assets/images/MatrixExample2.png){: .dark .w-75 .normal }