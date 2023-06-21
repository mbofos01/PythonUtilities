#!/usr/bin/env python3

import time

def show_information(debug):
    def decorator(func):
        def wrapper(*args):
            if debug:
                start_time = time.time()
                print("\n---------------------------------------------------------")
                print(f"Function '{func.__name__}' was called with:")
                print("---------------------------------------------------------")
                for i, arg in enumerate(args):
                    print(f"\t--> {func.__code__.co_varnames[i]}: {arg}")
                print("---------------------------------------------------------")
                print("Running . . .")
                print("---------------------------------------------------------")
                output = func(*args)
                print("---------------------------------------------------------")
                print(f"Returns: {output}")
                print("---------------------------------------------------------")
                end_time = time.time()
                execution_time = end_time - start_time
                print(f"Function '{func.__name__}' took {execution_time} seconds to execute.")
                print("---------------------------------------------------------\n")
            else:
                func(*args)
            return args
        return  wrapper
    return decorator


@show_information(True)
def showMe(test1,test2):
    print(test1)
    print(test2)
    return test1 + test2

if __name__ == '__main__':
    showMe(5,10)