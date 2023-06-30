from debugger.tools import show_information

@show_information()
def casa(re,rea=12):
    print(f"hello world ({re}) ")
    return 1

@show_information()
def plaza(re,te):
    casa(2,5)

    print(f"hello world ({re} , {te})")


@show_information(True)
def calculate_power(base, exponent):
    result = base ** exponent
    return result


@show_information(True)
def add_numbers(a, b):
    result = a + b
    
    return result / calculate_power(a,b)


add_numbers(1,3)