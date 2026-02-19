#!/usr/bin/env python3

import time
import inspect

from colorama import Back
import pretty_errors

try:
    from colorama import Fore, Style, init
    init(autoreset=True)  # Initialize colorama
    COLORS_AVAILABLE = True
    TERMINAL_WIDTH = 80  # Default fallback
    DASHES = "-" * TERMINAL_WIDTH
except ImportError:
    COLORS_AVAILABLE = False
    # Define dummy functions if colorama not available

    class DummyColor:
        def __getattr__(self, name):
            return ""
    Fore = DummyColor()
    Style = DummyColor()
    TERMINAL_WIDTH = 80
    DASHES = "-" * TERMINAL_WIDTH
    DASHES_STYLE = ""


def colorize(text, color):
    if COLORS_AVAILABLE:
        return f"{color}{text}"
    return text


def _get_caller_info():
    """Get information about the caller of the decorated function."""
    caller_frame = inspect.stack()[2]
    return f"was called from line {caller_frame.lineno} in {caller_frame.function}"


def _format_parameters(func, args):
    """Format and return parameter information including defaults."""
    sig = inspect.signature(func)
    bound_args = sig.bind(*args)
    bound_from_call = set(bound_args.arguments.keys())
    bound_args.apply_defaults()

    param_lines = []
    for param_name, param_value in bound_args.arguments.items():
        is_default = param_name not in bound_from_call
        default_indicator = " (default)" if is_default else ""
        param_lines.append(
            f"\t--> {param_name}: {param_value}{default_indicator}")
    return param_lines


def _format_execution_time(execution_time):
    """Format execution time with appropriate units."""
    if execution_time >= 60:
        minutes = int(execution_time // 60)
        seconds = execution_time % 60
        return f"{minutes}m {seconds:.2f}s"
    elif execution_time >= 1:
        return f"{execution_time:.2f}s"
    else:
        return f"{execution_time*1000:.1f}ms"


# Only export the main decorator - helper functions are internal
__all__ = ["show_information"]


def show_information(debug=True, color_scheme=None):
    """
    Decorator that provides detailed debugging information for function calls.

    Args:
        debug (bool): Whether to enable debugging output
        color_scheme (dict, optional): Custom color scheme for accessibility.
            Keys: 'header', 'params', 'running', 'return', 'time', 'error', 'dashes', 'error_dashes'
            Note: Only colorama styles are supported (DIM, NORMAL, BRIGHT). Blinking is not available.
            Example: {'header': Fore.WHITE, 'params': Fore.CYAN} for high contrast

    Returns:
        Decorated function with debug output
    """
    # Default color scheme
    default_colors = {
        'header': Style.BRIGHT + Fore.BLUE,
        'params': Fore.BLUE,
        'running': Style.DIM + Fore.YELLOW,
        'return': Back.CYAN + Style.BRIGHT + Fore.BLACK,
        'time': Style.BRIGHT + Fore.GREEN,
        'error': Style.BRIGHT + Fore.YELLOW,
        'dashes': Style.BRIGHT + Fore.WHITE,
        'error_dashes': Style.BRIGHT + Fore.RED
    }

    # Merge with user-provided color scheme
    if color_scheme:
        colors = {**default_colors, **color_scheme}
    else:
        colors = default_colors

    def decorator(func):
        def wrapper(*args):
            if debug:
                start_time = time.time()
                caller_info = _get_caller_info()

                print(colorize(f"\n{DASHES}", colors['dashes']))
                print(colorize(
                    f"Function '{func.__name__}' {caller_info} with:", colors['header']))
                print(colorize(DASHES, colors['dashes']))

                param_lines = _format_parameters(func, args)
                for line in param_lines:
                    print(colorize(line, colors['params']))

                print(colorize(DASHES, colors['dashes']))
                print(colorize("Running . . .", colors['running']))
                print(colorize(DASHES, colors['dashes']))

                try:
                    output = func(*args)
                except Exception as e:
                    print(colorize(DASHES, colors['error_dashes']))
                    print(colorize(
                        f"An exception occurred in function '{func.__name__}': {e}", colors['error']))
                    print(colorize(f"{DASHES}\n", colors['error_dashes']))
                    raise  # Re-raise to terminate

                print(colorize(DASHES, colors['dashes']))
                print(colorize(f"Returns: {output} ", colors['return']))
                print(colorize(DASHES, colors['dashes']))

                end_time = time.time()
                execution_time = end_time - start_time
                time_str = _format_execution_time(execution_time)
                print(colorize(
                    f"Function '{func.__name__}' took {time_str} to execute.", colors['time']))
                print(colorize(f"{DASHES}\n", colors['dashes']))
            else:
                output = func(*args)
            return output
        return wrapper
    return decorator


if __name__ == '__main__':
    # Example with funky custom color scheme
    funky_colors = {
        # Magenta background with bright black text
        'header': Back.MAGENTA + Style.BRIGHT + Fore.BLACK,
        'params': Fore.YELLOW + Back.BLUE,  # Yellow text on blue background
        'running': Style.BRIGHT + Fore.CYAN + Back.BLACK,  # Bright cyan on black
        # Green background with bright red text
        'return': Back.GREEN + Style.BRIGHT + Fore.RED,
        'time': Style.BRIGHT + Fore.MAGENTA + Back.WHITE,  # Bright magenta on white
        # Red background with bright yellow text
        'error': Back.RED + Style.BRIGHT + Fore.YELLOW,
        'dashes': Style.BRIGHT + Fore.CYAN,
        'error_dashes': Style.BRIGHT + Fore.RED + Back.YELLOW
    }

    @show_information(True, color_scheme=funky_colors)
    def showMe(test1, test2=5):
        print(test1)
        print(test2)
        test1 = test1 / 0
        return test1 + test2
    showMe(5)
