#Part One

def displayInventory(inventory):
    print("Inventory:")
    item_total = 0
    for k, v in inventory.items():
        print("{}:{}".format(str(v).ljust(4),k))
        item_total += v
    print("Total number of items: " + str(item_total))

#Part Two
def addToInventory(inventory, addedItems):
    for item in addedItems:
        inventory.setdefault(item,0)
        inventory[item] = inventory[item]+1
    return inventory

inv = {'gold coin': 42, 'rope': 1}
dragonLoot = ['gold coin', 'dagger', 'gold coin', 'gold coin', 'ruby']

if __name__ == "__main__":
    inv = addToInventory(inv, dragonLoot)
    displayInventory(inv)
