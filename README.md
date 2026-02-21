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

### Parameters

- `debug` (bool, default=True): Enable or disable debugging output.
- `color_scheme` (dict, optional): Custom color scheme for terminal output.
- `track_vars` (list or str, optional): Variables to track for changes during execution.
- `log_file` (str, optional): File path to write output instead of stdout (plain text, no colors).
- `deep_track` (bool, default=False): Use deep copying for variable tracking to detect in-place changes.

## Variable Tracking

Track changes to specific variables during function execution:

```python
@show_information(track_vars=['result'])
def calculate(x, y):
    result = x + y
    result *= 2
    return result

calculate(3, 4)
```

For deep tracking of in-place modifications:

```python
@show_information(track_vars=['data'], deep_track=True)
def modify_list(data):
    data.append(5)  # Detected with deep_track
    return data
```

## Output Redirection

Redirect debug output to a file:

```python
@show_information(log_file='debug.log')
def my_function(a, b):
    return a + b

my_function(1, 2)  # Output to debug.log
```

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
    'error_dashes': Style.BRIGHT + Fore.RED,
    'tracking': Style.BRIGHT + Fore.MAGENTA,
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
- `tracking`: Variable change messages

Uses Colorama styles (DIM, NORMAL, BRIGHT) and colors (Fore.*, Back.*, Style.*).

## Error Handling

The decorator catches and displays exceptions with colors:

```python
@show_information()
def failing_function():
    raise ValueError("Something went wrong")

failing_function()  # Shows error message and re-raises
```

## Testing

Run the test suite:

```bash
python -m pytest tests/ -v
```

## Performance Notes

- Variable tracking uses `sys.settrace`, which may slow down execution for large functions.
- A warning is printed if execution takes more than 1 second.
- For production, set `debug=False` to disable output.

## Development

- Variable tracking uses `sys.settrace`, which may slow down execution for large functions.
- A warning is printed if execution takes more than 1 second.
- For production, set `debug=False` to disable output.

### Building the Package

To build the package for distribution:

```bash
pip install build
python -m build
```

This creates `dist/debugger_decorator-<version>.tar.gz` and `dist/debugger_decorator-<version>-py3-none-any.whl`.

### Publishing to PyPI

1. Install Twine:

   ```bash
   pip install twine
   ```

2. Upload to Test PyPI (recommended first):

   ```bash
   python -m twine upload --repository testpypi dist/*
   ```

3. Upload to Production PyPI:

   ```bash
    python -m twine upload dist/*
   ```

You'll need a PyPI account and API token. Set it up at [pypi.org](https://pypi.org/account/register/) and use `__token__` as username with your token as password.
