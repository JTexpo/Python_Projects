import random

def list_creation(amount):
    my_list = []
    for flip in range(amount):
        my_list.append('heads' if random.randint(0,1) == 0 else 'tails')
    return my_list

def count_repeat(my_list, goal_streak):
    counter = 1
    prev = ''
    repeat_counter = 0
    for flip in my_list:
        if flip == prev:
            counter += 1
        else:
            prev = flip
            counter = 1
        if counter == goal_streak:
            repeat_counter += 1
            counter = 1
    return repeat_counter

if __name__ == "__main__":
    #inits
    amount_of_trials = 10000
    goal_streak = 6
    #computing
    my_list = list_creation(amount_of_trials)
    amount = count_repeat(my_list,goal_streak)
    #out message
    print("Out of {} amount of flips {} amount had a streak of {}.\n\
The odds of seeing a streak of {} in a normal coin flip is {}%".format(
              amount_of_trials, amount, goal_streak,
              goal_streak, round(amount / amount_of_trials * 100,4)))
    
        
        
