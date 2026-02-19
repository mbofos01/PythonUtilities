# Debugger Decorator

A simple Python decorator for debugging functions.

## Installation

```bash
pip install debugger-decorator
```

To include the optional `pretty_errors` dependency:

```bash
pip install debugger-decorator[pretty]
```

## Usage

```python
from debugger_decorator import show_information

@show_information()
def my_function(a, b):
    return a + b

my_function(1, 2)
```

This will print information about the function call, its arguments, return value, and execution time.
