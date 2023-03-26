---
title: Python Syntax
date: 2022-08-16 19:00:00 +0000
categories: [Python]
---
## Introduction

Python syntax is fairly simple, if you’ve come from any other programming language you should find it quite easy to adapt. In my experience the main syntax you want to know to get started would include:

- Declaring a variable
- Outputting a variable to screen
- Adding a comment
- Conditional Statements
- Basic Loops
- Declaring a Variable

```python
myTestVariable = "Test"
```

There are a few rules you must follow when naming variables:

- It must start with a letter or an underscore
- It can only contain alpha-numberic characters and underscores
- Remember that variables are case sensitive

## Outputting a variable to screen

```python
myTestVariable = "Test"

print(myTestVariable)
```

Super easy and very similar to alot of other languages. Remember that variables are case sensitive so get your casing right.

## Adding a comment

```python
# This is an example of how you can declare and print a variable
 
myTestVariable = "Test"
 
print(myTestVariable)
```

Nice and easy using the hashtag as a comment declaration the same as powershell. Comments are super useful when writing code to explain what you are doing. They make reviewing your code even easier.

## Conditional Statements

```python
# This is an example of how you can declare and print a variable
# It also shows you how to write a conditional statement
 
myTestVariable = "Test"
 
print(myTestVariable)
 
if myTestVariable == "Test":
    print("Correct Value")
elif myTestVariable == "Test1":
    print("Still a correct value")
else:
    print("IncorrectValue")
```

Conditional statements are your standard If, elseif, else code blocks that are used in all languages. They can be as simple as just using the if, or you can use a combination of all to get the needed outcome.

Notice a couple of things here:

- We use a colon to end each conditional statement. This tells the interpreter, where the conditional statement ends and the action begins.
- We use == instead of =. In Python
  + == – Is an equality operator, used to compare the value of 2 objects
  + = – Is an assignment operator, used to assign a value to an object

## Loops
### For Loop

```python
# This is an example of how you to use a basic for loop
 
myTestVariable = ["A","B","C","D","E"]
 
for a in (myTestVariable):
    print(a)
```

These types of loops are useful when you want to specifically loop over a set number of values usually held in a variable. We have 5 values in our list so we know the loop will execute 5 times.

### While Loop

```python
# This is an example of how you to use a basic while loop
iteration = 0
maxIteration = 10
 
while iteration < maxIteration:
    print(iteration)
    iteration = iteration +1
```    
This type of loop is best when you want to control the outcome within the loop itself. The easiest way to show this is using an 
iteration, you want to iterate x times but you want to control when it iterates during the loop.