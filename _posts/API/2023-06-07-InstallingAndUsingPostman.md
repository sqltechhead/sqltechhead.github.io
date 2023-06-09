---
title: Installing and using Postman
date: 2023-06-07 19:00:00 +0000
layout: post
categories: [API]
---

## Introduction
Postman is an application that makes communicating with APIs so easy. It makes APIs accessible to anybody without any coding knowledge. While giving that accessibility it also provides easy ways to convert into things such as a curl command if you want to work with APIs by code. It really is the best starter tool in my opinion to getting into using APIs.

## Install Postman
* Navigate to the below link and click on the download link

<https://www.postman.com/downloads/>

* Double click on downloaded file and follow prompts to install

The most basic application will look like below, there are plenty of expert features that postman provides but we will just stick with the basics for now.

![Postman](/assets/images/Postman.png){: .dark .w-75 .normal }

## Running your first API Call
* Select New at the top of the postman screen
* Select HTTP Request to get started with an API

![Postman](/assets/images/Postman2.png){: .dark .w-75 .normal }

* You will now get your API area to work with as below

![Postman](/assets/images/Postman3.png){: .dark .w-75 .normal }

You get the option to do many things with APIs such as:

* GET - Read data
* PUT - Set data
* POST - Set Data
* DELETE - Delete data

You then have sections such as Authorization which allows you to pass credentials to APIs that require it. Then sections such as Header sna Body usually pertain to API Endpoints where you need to set data, these sections allow you to set the data to be pushed and the type of data it is.

For the most basic example we are going to use an API endpoint. We will stick with GET for now. The below link is a fun free api that requires no authentication so is a great starter API. 

<https://pokeapi.co/>

* As you will see on the page it provides you with you api endpoint which is:

```https://pokeapi.co/api/v2/```

* Then the method can be found after for example:

```pokemon/charizard```

* Jump onto your postman window and put the below into the URL section

```https://pokeapi.co/api/v2/pokemon/charizard```

* Then press send.

![Postman](/assets/images/Postman4.png){: .dark .w-75 .normal }

You now have your very own pokedex! Test out some other pokemon to get more acquainted

## Using Parameters
Now im a big beer enthusiast, i love brewing my own beer so why wouldn't i love to use a beer recipe api!

If you go to the below link, you will find a 3rd party implementation of BrewDogs DIYDog API allowing for searchable and pageable API calls. No authentication is needed here either, they rate limit based off number of calls from certain IP addresses to keep it fair

<https://punkapi.com/documentation/v2>

Using this API we will get into how to use parameters.
* Open up postman
* Add another http request
* Enter the below url into the url section

```https://api.punkapi.com/v2/beers```

* Press send now and you will return every single recipe

Having every single recipe is great but as well as a beer enthusiast i am a STRONG beer enthusiast. I want to be looking at any beer that is over 7% how do i do that?

* Scroll down to the Get Beers section in the documentation

![Postman](/assets/images/Postman5.png){: .dark .w-75 .normal }

> In majority of good API documentation they will provide easy ways to access different endpoints/params.
{: .prompt-tip }

* We want a beer with a high ABV (Alcohol by Volume.) so we want to use the ```abv_gt``` parameter
* In postman for your http request open the parameters tab.
* Add abv_gt as the key
* Add 7 as the value as below

![Postman](/assets/images/Postman6.png){: .dark .w-75 .normal }

> Notice that your url has now had the parameter syntax updated automatically
{: .prompt-info }

* Click send on the API call

You now have a list of all the best types of beer for you to make to have a really good night! Try out some other parameters to test your skills. 