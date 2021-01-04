import re

def one_digit(my_string):
    num_check = re.compile(r'\d')
    return True if num_check.search(my_string) != None else False

def eight_long(my_string):
    return True if len(my_string) > 7 else False

def has_caps(my_string):
    caps_check = re.compile(r'[A-Z]')
    return True if caps_check.search(my_string) != None else False

def has_lower(my_string):
    lower_check = re.compile(r'[a-z]')
    return True if lower_check.search(my_string) != None else False

if __name__ == "__main__":
    my_password = str(input("Please Enter Your Password : "))
    if (one_digit(my_password) and eight_long(my_password) and
        has_caps(my_password) and has_lower(my_password)):
        print("This is a strong password!")
    else:
        print("This is not a strong password please try adding : ")
        if not one_digit(my_password):
            print("At Least One Number")
        if not eight_long(my_password):
            print("More Characters")
        if not has_caps(my_password):
            print("Some Caps")
        if not has_lower(my_password):
            print("Some Lowercases")
