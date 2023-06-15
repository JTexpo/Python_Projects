import csv
from typing import List

def get_midpoint_list(my_list: list)->list:
    """A function to return the middle values of a list

    ex.
    [ 0, 1, 2, 4, 10 ]
    would return
    [ .5, 1, 2, 6 ]

    Args:
        my_list (list): the list that you wish to find the midpoints of

    Returns:
        list: the mid points of the list
    """
    # if the list is of length 1, we return because we can't find it's midpoint
    if len(my_list) <= 1:
        return my_list

    # creating a new list & itterating over the input list
    new_list = []
    for index in range(1, len(my_list)):
        # adding the previous element with the delta of the current element and the previous element divided by 2
        new_list.append(
            my_list[index - 1] + (my_list[index] - my_list[index - 1]) / 2.0
        )

    return new_list

def read_csv_file(file_path:str)->List[list]:
    """A function to read a csv file 

    Args:
        file_path (str): path to the file

    Returns:
        List[list]: a list of list indicating all of the cells in the csv
    """
    data = []
    with open(file_path, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            data.append(row)
    return data