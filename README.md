# Debugger Decorator

A simple Python decorator for debugging functions.

## Installation

```bash
pip install debugger-decorator
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

## Customizing Colors

You can customize the color scheme for better accessibility or personal preference:

```python
from debugger_decorator import show_information
from colorama import Fore, Style, Back

# High contrast color scheme
high_contrast_colors = {
    'header': Style.BRIGHT + Fore.WHITE,
    'params': Fore.CYAN,
    'running': Style.BRIGHT + Fore.YELLOW,
    'return': Back.GREEN + Style.BRIGHT + Fore.BLACK,
    'time': Style.BRIGHT + Fore.GREEN,
    'error': Style.BRIGHT + Fore.RED,
    'dashes': Style.BRIGHT + Fore.WHITE,
    'error_dashes': Style.BRIGHT + Fore.RED
}

@show_information(color_scheme=high_contrast_colors)
def my_function(a, b):
    return a + b

my_function(1, 2)
```

Available color keys:
- `header`: Function name and caller info
- `params`: Parameter names and values
- `running`: "Running . . ." message
- `return`: Return value display
- `time`: Execution time
- `error`: Error messages
- `dashes`: Separator lines
- `error_dashes`: Error separator lines

Uses Colorama styles (DIM, NORMAL, BRIGHT) and colors (Fore.*, Back.*, Style.*).
