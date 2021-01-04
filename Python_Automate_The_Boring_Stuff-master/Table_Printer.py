tableData = [['apples', 'oranges', 'cherries', 'banana'],
             ['Alice', 'Bob', 'Carol', 'David'],
             ['dogs', 'cats', 'moose', 'goose']]

def printTable(my_table):
    for item in range(len(my_table[0])):
        for my_list in my_table:
            print(my_list[item].rjust(10),end = '')
        print('')

if __name__ == "__main__":
    printTable(tableData)
