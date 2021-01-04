def collatz(number):
    if (number % 2 == 0):
        print (number // 2)
        return number // 2
    else:
        print (3 * number + 1)
        return 3 * number + 1

if __name__ == "__main__":
    while (True):
        try:
            my_num = int(input("Enter A Number : "))
            break
        except ValueError as ve:
            print("A Value Error Has Occured : {}\n\nPlease Make Sure You Are Typing An Int".format(ve))
    while (my_num != 1):
        my_num = collatz(my_num)
