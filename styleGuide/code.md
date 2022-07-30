# The Code Style Guide

This style guide outlines basic code styles that when followed will ensure the codebase has a single uniform style.

## General

All lines should not excede 80 characters (within reason).

## Comments

Comments should be meaningfull, with a goal to provide understanding of tricky or easy to misunderstand code. Comments should also be used at the begining of funtions, classes (and class method definitions) to provide an understanding of what the code structure (function, class, class method) does.

Comments describing a function, class, or class method as a whole should explain at a **high** level.

Comments describing a class should use Docstrings. Denote any arguments that should be passed, and if a error is raised, denote it.

Example:

```python
def example(num1, num2):
    """Adds two numbers together

    Arguments:
    -----
    num1: int
    num2: int

    Raises:
    -----
    NotImplementedError
        If num1 is over 5
    """
    if num1 > 5:
        raise NotImplementedError("Numbers over 5 are not supported")
    else:
        return num2 + num1
```

Remember:

> “Code tells you how; Comments tell you why.”
>
> - Jeff Atwood

## Variables

Variables should be named using camelCase with a lowercase first character.

## Classes

Classes should be named using CamelCase with a uppercase first character.

## Functions

Functions should be named using camelCase with a lowercase first character.

## String Literals

String literals should use double quotes where possible.
