from debugger.tools import show_information

@show_information(True)
def casa(re,rea=12):
    print(f"hello world ({re}) ")
    return 1

@show_information(debug = False)
def plaza(re,te):
    print(f"hello world ({re} , {te})")


casa(2)
plaza(2,5)

