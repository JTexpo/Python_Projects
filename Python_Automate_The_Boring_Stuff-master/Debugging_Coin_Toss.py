import random
'''
OLD CODE TO BE DEBUGGED

guess = ''
while guess not in ('heads', 'tails'):
    print('Guess the coin toss! Enter heads or tails:')
    guess = input()
toss = random.randint(0, 1) # 0 is tails, 1 is heads
if toss == guess:
    print('You got it!')
else:
    print('Nope! Guess again!')
    guesss = input()
    if toss == guess:
        print('You got it!')
    else:
        print('Nope. You are really bad at this game.')
'''

#putting into this if statement just to help make sure that we only do this when main
if __name__ == "__main__":
    #there needs to be a dictionary or some way to relate heads/tails to 1/0
    coin_dic = {'heads':1, 'tails':0}
    guess = ''
    #relocation of print statement to make, since theres only 1 guess
    print('Guess the coin toss! Enter heads or tails:')
    #adding a wrong statement which should be in the while loop instead of the repeated guess
    wrong = False
    while guess not in ('heads', 'tails'):
        if wrong:
            print ("Please type heads or tails")
        guess = input()
        wrong = True
    toss = random.randint(0, 1) # 0 is tails, 1 is heads
    #converting the heads/tails to a 1/0 for the future if statement
    guess = coin_dic[guess]
    if toss == guess:
        print('You got it!')
    else:
        print('Nope! Guess again!')
        #repeating the proper guess statement and correction practice mentioned earlier
        wrong = False
        while guess not in ('heads', 'tails'):
            if wrong:
                print ("Please type heads or tails")
            guess = input()
            wrong = True
        guess = coin_dic[guess]
        if toss == guess:
            print('You got it!')
        else:
            print('Nope. You are really bad at this game.')
