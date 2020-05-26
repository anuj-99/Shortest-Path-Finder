from matplotlib import pyplot as plt
import random


# Creating a class 'station' which would be like a node on the screen
class Station:
    def __init__(self, i, j):
        """ Set is present for the coloring purpose"""
        self.set = 0
        self.i = i
        self.j = j
        # f is the cost function
        # g is like the actual distance from the starting point
        # h is the heuristic - shortest possible distance - here, it would be displacement (euclidean distance)
        self.f = 0
        self.g = 0
        self.h = 0
        # To trace back the path, we need to record parents
        self.parent = None
        self.wall = False
        # list of neighbors of a station
        self.neighbors = []
        if random.random() < 0.5:
            self.wall = True

    def add_neighbors(self, grid_passed):
        """Returns list of neighbor stations"""
        i = self.i
        j = self.j
        if j < size - 1:
            self.neighbors.append(grid_passed[i][j + 1])
        if i > 0:
            self.neighbors.append(grid_passed[i - 1][j])
        if j > 0:
            self.neighbors.append(grid_passed[i][j - 1])
        if i < size - 1:
            self.neighbors.append(grid_passed[i + 1][j])
        if i < size - 1 and j < size - 1:
            self.neighbors.append(grid_passed[i + 1][j + 1])
        if i > 0 and j < size - 1:
            self.neighbors.append(grid_passed[i - 1][j + 1])
        if i < size - 1 and j > 0:
            self.neighbors.append(grid_passed[i + 1][j - 1])
        if i > 0 and j > 0:
            self.neighbors.append(grid_passed[i - 1][j - 1])


# Used a class instead of array just to update the value of set every time a station is added to open_set
class Set:
    def __init__(self, array):
        self.array = array

    def add(self, station, var):
        if var == 'open':
            station.set = -5
        self.array.append(station)


def heuristic(a, b):
    """Our heuristic function"""
    dist = ((a.i - b.i)**2 + (a.j - b.j)**2)**0.5
    return dist


open_set = []
open_set = Set(open_set)
closed_set = []
closed_set = Set(closed_set)
size = 50
grid = []

# Making a grid
for i in range(size):
    row = [Station(0, 0) for i in range(size)]
    grid.append(row)

# Allotting one Station object to each of the element in the grid
for i in range(size):
    for j in range(size):
        grid[i][j] = Station(i, j)

# Filling neighbours
for i in range(size):
    for j in range(size):
        grid[i][j].add_neighbors(grid)

start = grid[00][0]
end = grid[size - 1][size - 1]
grid[0][0].wall = False
grid[size - 1][size - 1].wall = False

# Adding the start point to the open_set
open_set.add(start, 'open')

# Actual loop
a = 0
while a < 1:
    if open_set.array:
        winner = 0
        for i in range(len(open_set.array)):
            if open_set.array[i].f < open_set.array[winner].f:
                winner = i
        current = open_set.array[winner]

        if current == end:
            # Calculating path
            current.set = 8
            while current.parent:
                current.parent.set = 16
                current = current.parent
            print('Done')
            a = a + 1

        # Remove the evaluated point from open_set and add to closed_set
        open_set.array.pop(winner)
        closed_set.array.append(current)

        # Adding a new point to evaluate in open_set
        neighbors = current.neighbors
        for neighbor in neighbors:
            if neighbor not in closed_set.array:
                if not neighbor.wall:
                    temp_g = current.g + 1
                    new_path = False
                    if neighbor in open_set.array:
                        if temp_g < neighbor.g:
                            neighbor.g = temp_g
                            new_path = True
                    else:
                        neighbor.g = temp_g
                        new_path = True
                        open_set.add(neighbor, 'open')
                    if new_path:
                        neighbor.h = heuristic(neighbor, end)
                        neighbor.f = neighbor.g + neighbor.h
                        neighbor.parent = current
            # print(neighbor.parent)
    else:
        current.set = 12
        while current.parent:
            current.parent.set = 8
            current = current.parent
        print('No path found!')
        a = a + 1

# For debugging purpose - Visualisation
vis_grid = []
for i in range(size):
    row = [0 for i in range(size)]
    vis_grid.append(row)

start.set = 20
end.set = 25
for i in range(size):
    for j in range(size):
        if grid[i][j].wall:
            vis_grid[i][j] = grid[i][j].set - 10
        else:
            vis_grid[i][j] = grid[i][j].set

plt.figure(figsize =(12, 12))
plt.title('A* Algorithm - Shortest Path Finder\n')
plt.imshow(vis_grid)
plt.show()
