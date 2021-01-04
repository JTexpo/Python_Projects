import re

def extract_date(my_string):
    findDate = re.compile(r'(\d\d)/(\d\d)/(\d\d\d\d)')
    my_date = findDate.search(my_string)
    return my_date

def date_checker(re_my_date):
    day = int(re_my_date.group(1))
    month = int(re_my_date.group(2))
    year = int(re_my_date.group(3))

    if year > 2999 or year < 1000 or day < 1 or day > 31 or month < 1 or month > 12:
        print("The date {} : is unreasonable".format(re_my_date.group()))
        return
    elif month in [4,6,9,11]:
        if day > 30:
            print("Invalid day {}. Does Not exist in {}".format(day,re_my_date.group()))
            return
    elif month == 2:
        if day > 29:
            print("Invalid day {}. Does Not exist in {}".format(day,re_my_date.group()))
            return
        elif day % 4 == 0:
            if day % 100 == 0 and not day % 400 == 0:
                if day > 28:
                    print("Invalid day {}. Does Not exist in {}".format(day,re_my_date.group()))
                    return
        elif day > 28:
            print("Invalid day {}. Does Not exist in {}".format(day,re_my_date.group()))
            return

    print("The date {} was found, and is a real date!".format(re_my_date.group()))
        
if __name__ == "__main__":
    my_string = str(input("Enter In Some Text, I Will Varfiy The Date DD/MM/YYYY Is Correct :\n"))
    my_date = extract_date(my_string)
    date_checker(my_date)
    
