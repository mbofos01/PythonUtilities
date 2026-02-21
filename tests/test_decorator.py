import time
import pytest
from debugger_decorator import show_information
from io import StringIO
import sys


@show_information(debug=True)
def dummy():
    return 42


def test_output(capsys):
    dummy()
    captured = capsys.readouterr()
    assert "Function 'dummy'" in captured.out
    assert "Returns: 42" in captured.out


@show_information(debug=True, track_vars=['x'])
def tracked_func():
    x = 1
    x = 2
    return x


def test_tracking(capsys):
    tracked_func()
    captured = capsys.readouterr()
    assert "Variable 'x' initialized" in captured.out
    assert "Variable 'x' changed" in captured.out


@show_information(debug=True, log_file='test_log.txt')
def log_func():
    return 'logged'


def test_log_file():
    log_func()
    with open('test_log.txt', 'r') as f:
        content = f.read()
    assert "Function 'log_func'" in content
    assert "Returns: logged" in content
    # Check no ANSI codes
    assert '\x1b[' not in content
    # Clean up
    import os
    os.remove('test_log.txt')


@show_information(debug=True, track_vars=['data'], deep_track=True)
def deep_tracked_func():
    data = [1, 2]
    data.append(3)
    return data


def test_deep_tracking(capsys):
    deep_tracked_func()
    captured = capsys.readouterr()
    assert "Variable 'data' initialized" in captured.out
    assert "Variable 'data' changed" in captured.out  # Should detect append


@show_information(debug=False)
def silent_func():
    return 'silent'


def test_debug_false(capsys):
    silent_func()
    captured = capsys.readouterr()
    assert captured.out == ''  # No output


@show_information(debug=True, color_scheme={'header': '', 'params': '', 'dashes': '', 'return': '', 'time': '', 'error': '', 'error_dashes': '', 'running': '', 'tracking': ''})
def custom_color_func():
    return 123


def test_custom_color_scheme(capsys):
    custom_color_func()
    captured = capsys.readouterr()
    # Should have no ANSI codes
    assert '\x1b[' not in captured.out
    assert "Function 'custom_color_func'" in captured.out


@show_information(debug=True, track_vars='single_var')
def single_track_func():
    single_var = 'start'
    single_var = 'end'
    return single_var


def test_single_track_var(capsys):
    single_track_func()
    captured = capsys.readouterr()
    assert "Variable 'single_var' initialized" in captured.out
    assert "Variable 'single_var' changed" in captured.out


@show_information(debug=True)
def exception_func():
    raise ValueError("test error")


def test_exception_handling(capsys):
    with pytest.raises(ValueError):
        exception_func()
    captured = capsys.readouterr()
    assert "An exception occurred" in captured.out
    assert "test error" in captured.out


@show_information(debug=True, track_vars=['nonexistent'])
def nonexistent_track_func():
    x = 1
    return x


def test_nonexistent_var_tracking(capsys):
    nonexistent_track_func()
    captured = capsys.readouterr()
    # Should not crash, and no tracking messages for nonexistent var
    assert "Variable 'nonexistent'" not in captured.out
    assert "Function 'nonexistent_track_func'" in captured.out


@show_information(debug=True, track_vars=['counter', 'data'], deep_track=True)
def stress_test_func():
    counter = 0
    data = []
    for i in range(1000):
        counter += 1
        data.append(i)
        if i % 100 == 0:
            data = [x * 2 for x in data]  # Modify list
    return counter, len(data)


def test_stress_tracking(capsys):
    result = stress_test_func()
    captured = capsys.readouterr()
    assert "Function 'stress_test_func'" in captured.out
    assert result == (1000, 1000)
    # Check that some tracking happened
    assert "Variable 'counter'" in captured.out or "Variable 'data'" in captured.out


@show_information(debug=True)
def slow_func():
    time.sleep(1.1)
    return 'slow'


def test_performance_warning(capsys):
    slow_func()
    captured = capsys.readouterr()
    assert "Warning: Tracing may slow execution" in captured.out
