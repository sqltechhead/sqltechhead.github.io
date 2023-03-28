---
title: Python Functions
date: 2022-09-06 19:00:00 +0000
categories: [Python]
---
## Introduction
You may be familiar with functions if you have come from other programming languages. Functions are logical groupings of code blocks that carries out certain tasks. Functions can be used to improve code reuse as well as to improve readability in scripts.

Functions can accept parameters to allow the coder to really define the input and output they want or expect from their script.

A really simple example to illustrate is below.

- We define the function by using the def keyword.
- Best practice is to have function names as lowercase.
- After the function name we have open and closed brackets, inside these brackets you can specify parameters.
- A function name must have a colon at the end to define it
- The line after must be tabbed in and then you can begin to write your content

For the example we have used the input() system function which allows user input to continue the script. If you run the below you will be prompted to enter your name, then the script will output a Hello Name string.

```python
def sayhello(name):
    print(f"Hello {name} how are you?")
 
 
username = input("Hello, welcome to sqlTechHead. Whats your name?")
 
sayhello(username)
```

![PythonFunctions](/assets/images/PythonFunctions.png){: .dark .w-75 .normal }

With functions you can also add default parameters to the function that can be used if you don’t pass anything else in. See below how we add a default to our function parameter. Then we just call the function with open close brackets. The default will be used

```python
def sayhello(name="mysterious user"):
    print(f"Hello {name} how are you?")
 
sayhello()
```
![PythonFunctions](/assets/images/PythonFunctions1.png){: .dark .w-75 .normal }

## Args and Kwargs
Args and kwargs are colloquially known as magic parameters in the python world. They are parameters used if you dont know what parameters will be passed in.

### Args
Args allow you to pass in multiple parameters to the function without defining the parameter name in the function

```python
def favouritefoods(*args):
    for arg in args:
        print(f"One of my favourite foods is {arg}")
 
favouritefoods("Pizza","Cookies","Pasta")
```

![PythonFunctions](/assets/images/PythonFunctions2.png){: .dark .w-75 .normal }

As you can see we use our magic args parameter, we can pass as many parameters into the function as we want and it will all be stored in the *args parameter as a tuple

### Kwargs
Kwargs are very similar to args, however instead of storing as a tuple, they are stored as a dictionary. This allows you to specify a key for the parameter while passing it in.

```python
def personaldetails(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")
 
personaldetails(FirstName="sql", LastName="TechHead",Age=31,JobTitle="Senior SQL DBA")
```

![PythonFunctions](/assets/images/PythonFunctions3.png){: .dark .w-75 .normal }

Here you can see we can make use of the key and value of the key value pair in the dictionary. Kwargs is great to use for more complicated scenarios