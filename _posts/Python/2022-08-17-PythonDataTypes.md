---
title: Python Data Types
date: 2022-08-17 19:00:00 +0000
categories: [Python]
---
## Introduction
Data types allow the python interpreter to validate the contents of a variable. In Python data types are by default inferred by the value you assign a variable. This means if you set a variable as 1, it will infer it as an integer. If you set it as “one” it will infer it as a string.

There are 5 standard data types:

- Numbers
- String
- List
- Tuple
- Dictionary

## Numbers
There are 3 different numerical types within the numbers data type:

- Int
- Float
- Complex
Below will show some examples of declaring these

```python
integer = 1
float = 1.00
complex = 1+1j
```

Integer and float should be pretty self explanatory. Complex however lives up to its name, this datatype is used for complex calculations. It works by having a real and imaginary part to it. 1 is the real part and 1j is the imaginary part.

You can create a complex data type by using the complex function, then you access each part of the value real or imaginary.

```python
varA = 10
varB = 20
varC = complex(varA,varB)
```

## Strings
Strings are used for your standard character variables. These will be used alot in any python program. They can be defined by either single quotes or double quotes and can be output to screen using the print() function.

You can also have strings call f strings which allow you a neat and tidy way to inject other variables into the middle of the string.

```python
#string
codingLanguage = "Python"
print(codingLanguage)
 
#f string
codingLanguage = "Python"
print(f"This is a {codingLanguage} script)
```

The site Real Python has a great article on f strings as well as what needed to be used prior to f strings.

<https://realpython.com/python-f-strings/>

## Lists
Lists are used to store multiple values in your variable, usually you will then iterate over those values to run something in your program. Lists are indexable meaning you can get to the value using usual iteration values (0,1,2….). A list is define by using square brackets. The below example defines a countries list with 3 countries in and shows 2 ways to access values in that list.

```python
#Defining a list
countries = ["England","France","Germany","England"]
 
#Accessing a list option 1
for a in (countries):
    print(a)
 
#Accessing a list option 1
print(countries[0])
print(countries[1])
print(countries[2])
 
#Add a country to a list
countries.append("Spain")
```

## Tuples
Tuples are very similar to lists, they are ordered and allow duplicate values as they provide an index of all values in the tuple. The main difference between the two is that once you define a tuple you cannot add,amend or remove any item from it. Using the exact same example as the list you can see the slight difference between the two

```python
#Defining a tuple
countries = ("England","France","Germany","England")
 
#Accessing a tuple option 1
for a in (countries):
    print(a)
 
#Accessing a tuple option 1
print(countries[0])
print(countries[1])
print(countries[2])
```

## Dictionaries
Dictionaries are another data type that allow storing multiple values within a variable, however they behave very differently. Data in a dictionary is stored in key value pairs rather than an index. This means however you cannot have duplicates in a dictionary as the key has to be unique.

```python
#Define a dictionary
capitals = {
    "England": "London",
    "France": "Paris",
    "Germany": "Berlin",
    "Spain": "Barcelona"
}
 
#Access a dictionary
capitals["England"]
capitals["France"]
capitals["Germany"]
capitals["Spain"]
 
#Amending a dictionary
capitals["Spain"] = "Madrid"
 
#Looping through a dictionary
#Dictionaries allow the use of keys() and values() functions
for a in capitals.keys()
    print(a)
 
for a in capitals.values()
    print(a)
```