# Explanation of code
This document will provide a brief overview of certain patterns that I have adopted in writing this
softwar, so as to make reading and understanding the code easier

## deepCopy decorator

Example:
```python
@deepCopyArgs("arg1", "argk")
def function(arg1, arg2, ..., argn):
	pass
```

**Motivation:**  
This decorator is needed because of python's pass by reference when combined with the use of
higher order functions in the program.

Since python passes every argument by value in the case of a function which generates another
function to be used later the risk is for some of these passed parameters to be changed after the
function has been generated yet they would still influence the function (which by now is likely 
embedded in another object)

At the same time for some of these parameters this referential nature is intended and necessary, as
is the case for the Hub object, whose changes **must** be visible to old objects

**Explanation:**  
The decorator takes as input the string names of the parameters which shouldn't be copied, the 
returned value is a function which, when called makes a deep copy of all parameters given (except 
the one specified by the decorator call) and then calls the original function with these parameters

## Function generation

```python
def generating_function(*gargs, **gkwargs):
	def generated_function(self, *args, **kwargs):
		pass
	return generated_function
```

**Motivation:**  
This is the most basic form of code generation in python and I make use of this pattern inside of 
metaclasses to generate specific functions based on the parametrization provided by the 
configuration file

**Explanation:**  
This code simply returns a closure of the generated function with the arguments provided to the 
generating function. 

In this case the self is not necessary but will be useful to understand the next pattern

NB.: See the deepCopy pattern for caveats due to pythons argument passing standard

## Function Embedding

```python
class Metaclass(type):
	def __new__(cls, *args, **kwargs):
		args[2]['func_name'] = generating_function(*fargs, **fkwargs)
		return super().__new__(cls, *args, **kwargs)
```

**Motivation:**  
This is the pattern used to make a function part of the class that is being created by the given
Metaclass.

**Explanation:**  
Class creation in python is achieved throug calls to `type` or derived classes. In particular the
standard class creation:

```python
class A(B,C):
	a = 1
	....
```

is equivalent to the function call:

```python
A = type("A", (B, C), {'a':1, ...})
```

so in order to create programmatically a class with a given function I make use of metaclasses which
interject themselves between the call and type, each adding functions and attributes to the 
namespace dictionary (which, being the third argument in the call, is referred to as `args[2]`

In doing so I don't need to do any of the binding which would be required in order to assign a 
preexistent class a new method, moreover many metaclasses can be used to create a single class and
each can see and manipulate functions created by the others

## Case based functions:

```python
def gen_func(old_f, case_to_handle, ...):
	def func(case, ...):
		if case==case_to_handle:
			...
		else:
			return old_f(case, ...)
	return func
```

**Motivation:**  


