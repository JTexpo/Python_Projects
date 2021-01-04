import time
import random

if __name__ == "__main__":
    
    input ("Welcome To The Multiplication Quiz.\n\
You'll Have 10 Question With 8 Seconds Per Question.\n\
You May Get Up To 3 Guesses Per Question Before Counted Incorrect.\n\
Type Anything To Continue To The Quiz : ")
    correct = 0
    for question in range(10):
        trys = 0
        start = time.time()
        answer = False
        num1 = random.randint(0,9)
        num2 = random.randint(0,9)
        ans = num1*num2
        while True:
            if (time.time() - start) > 8:
                print("Too Slow : True Answer Was : {}".format(ans))
                time.sleep(1)
                break
            try:
                my_guess = int(input("What is {}x{} : ".format(num1,num2)))
            except Exception as e:
                print ("Please Enter A Number : {}".format(e))
                continue
            if (time.time() - start) > 8:
                print("Too Slow True Answer Was : {}".format(ans))
                time.sleep(1)
                break
            if my_guess == ans:
                print("Correct")
                time.sleep(1)
                correct += 1
                break
            else:
                trys += 1
            if trys == 3:
                print("Incorrect True Answer Was : {}".format(ans))
                time.sleep(1)
                break
    print("Your Score Was {}/10".format(correct))
        
