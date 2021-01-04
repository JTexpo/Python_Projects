import matplotlib.pyplot as plt

# Possible colours for matplotlib
possible_colours = ['ro', 'bo', 'go', 'co', 'mo', 'yo']
# Colour for the centroid
centroid_colour = 'ko'

# Given Inits / feel free to change or add own data
x =[35, 34, 32, 37, 33, 33, 31, 27, 35, 34, 62, 54, 57, 47, 50,57, 59, 52, 61, 47, 50, 48, 39, 40, 45, 47,39, 44, 50, 48]
y =[79, 54, 52, 77, 59, 74, 73, 57, 69, 75, 51, 32, 40, 47, 53,36, 35, 58, 59, 50, 23, 22, 13, 14, 22, 7, 29, 25, 9, 8]

# Creating a list of all the points, the reason why I am using a nested list and not a dictionary is because
# We do not know if each point we are given is unique, and if not then a dictionary would be messed up
# I am also not using a class because classes takes up more memory if I recall correctly and I don't
# want to take up more memory when the structor for this is simple enough to not require a class
# The following structor is :
# [ [ node_val_x, node_val_y, int_val_centroid_ref ] , ... ]
myNodes = []
for index in range(len(x)):
    myNodes.append( [ x[index] , y[index] , -1 ] )

# Given Inits / feel free to change or add own data
cx = [39, 62, 35]
cy = [13, 51, 79]

# Creating a list of all the centroids, for the same reason as mentioned above, also index will be the key value for nodes
# The following structor is :
# [ [ centroid_x, centroid_y ], ... ]
myCentroids = []
for index in range(len(cx)):
    myCentroids.append( [ cx[index] , cy[index] ] )

def assing_nodes_centroids():
    global myCentroids, myNodes
    # Itterating through all the nodes
    for node_index in range(len(myNodes)):
        # A list that has the info of the
        closest_nodes_info = [ -1, 10000 ]
        # Itterating through all the centroids to find which is closet to the node
        for centroid_index in range(len(myCentroids)):
            # Creating a x and y so we can take the pythageran therom to help find the 
            py_x = abs( myNodes[node_index][0] - myCentroids[centroid_index][0] )
            py_y = abs( myNodes[node_index][1] - myCentroids[centroid_index][1] )
            # Pythageram therom
            pythag = (py_x**2 + py_y**2)**(.5)
            # if the distance that we found is less than the current distance
            if pythag < closest_nodes_info[1]:
                # The new closest centroid is the one we are at
                closest_nodes_info[0] = centroid_index
                # The new closest distance is the one we found
                closest_nodes_info[1] = pythag
        # Assigning the node its closest centroid
        myNodes[node_index][2] = closest_nodes_info[0]

def recenter_centroids():
    global myCentroids, myNodes
    # Itterating through all the centroids to reassing them
    for centroid_index in range(len(myCentroids)):
        # creating varibles that will keep tract of the information from each node
        total_x = 0
        total_y = 0
        count = 0
        # Itterating through each node
        for node in myNodes:
            # If the nodes ID is the same as the centroid that we are on
            if (node[2] == centroid_index):
                # add the x and y values to the total and increment the count
                total_x += node[0]
                total_y += node[1]
                count += 1
        # Taking the mean of the x and y values
        myCentroids[centroid_index][0] = total_x / count
        myCentroids[centroid_index][1] = total_y / count

# Defining the process of one step
def cluster_step():
    assing_nodes_centroids()
    recenter_centroids()

# init a backup so we know when we are done
backupCentroids = []
# Function for a backup since it is a nested list
def create_backup():
    global backupCentroids
    backupCentroids = []
    for centroid in myCentroids:
        backupCentroids.append(list(centroid))

def backup_is_equal():
    global backupCentroids, myCentroids
    # comparing each centroid to each backup centroid
    for centroid_index in range(len(myCentroids)):
        if ( (backupCentroids[centroid_index][0] != myCentroids[centroid_index][0]) or 
            (backupCentroids[centroid_index][1] != myCentroids[centroid_index][1]) ):
            return False
    return True

# Defining the process of solving
def cluster_solve():
    while True:
        create_backup()
        cluster_step()
        if (backup_is_equal()):
            break

def grid_plot():
    global myCentroids, myNodes
    # Ploting all of the nodes with their respective colour
    for node in myNodes:
        plt.plot( node[0] , node[1] , possible_colours[node[2]] )
    # Plotting all the centroids with the same colour
    for centroid in myCentroids:
        plt.plot( centroid[0] , centroid[1] , centroid_colour )
    plt.show()

if __name__ == "__main__":
    # Showing a before
    grid_plot()
    # Solving
    cluster_solve()
    # Showing an after
    grid_plot()