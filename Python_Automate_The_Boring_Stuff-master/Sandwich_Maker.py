import pyinputplus as pyip

if __name__ == "__main__":
    price_dic = {"bread" : {"wheat" : 1.25, "white" : 1.25, "sourdough" : 1.75},
                 "protien" : {"chicken" : 2.15, "turkey" : 2.15, "ham" : 2.50, "tofu" : 1.85},
                 "cheese" : {"cheddar" : 1.00, "swiss" : 1.15, "mozzarella" : 1.35},
                 "mayo" : {"yes" : .05, "no" : 0},
                 "mustard" : {"yes" : .05, "no" : 0},
                 "lettuce" : {"yes" : .05, "no" : 0},
                 "tomato" : {"yes" : .05, "no" : 0}}
    
    my_bread = pyip.inputMenu(list(price_dic["bread"]))
    my_protien = pyip.inputMenu(list(price_dic["protien"]))
    my_yn = pyip.inputYesNo("Would You Like Cheese : ")
    if my_yn == "yes":
        my_cheese = pyip.inputMenu(list(price_dic["cheese"]))
        cost = price_dic["cheese"][my_cheese]
    else:
        cost = 0
    my_mayo = pyip.inputYesNo("Would You Like Mayo : ")
    my_mustard = pyip.inputYesNo("Would You Like Mustard : ")
    my_lettuce = pyip.inputYesNo("Would You Like Lettuce : ")
    my_tomato = pyip.inputYesNo("Would You Like Tomato : ")

    cost += (price_dic["bread"][my_bread] + price_dic["protien"][my_protien] +
            price_dic["tomato"][my_tomato] + price_dic["mayo"][my_mayo] +
            price_dic["mustard"][my_mustard] + price_dic["lettuce"][my_lettuce])
    print("Your total cost for your sandwhich is ${}".format(round(cost,3)))
            
