from debugger.tools import show_information

@show_information()
def casa(re,rea=12):
    print(f"hello world ({re}) ")
    return 1

@show_information()
def plaza(re,te):
    casa(2,5)

    print(f"hello world ({re} , {te})")


plaza(2,3)

