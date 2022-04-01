

#node class
class Node:
    def __init__(self, state = None, parent = None, action = None):
        #the state in this case is a 2D coordinate
        self.state = state
        self.parent = parent
        self.action = action

#fronties classes: Stack and Queue
        #DFS
class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        #return any(node.state == state for node in self.frontier)
        
        for node in self.frontier:
            if node.state == state:
                return True

        return False


    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("Empty Frontier")

        else:
            #last element
            node = self.frontier[-1]
            #remove last element
            self.frontier.pop(-1)
            return node


#inherits from StackFrontier bc all functions except remove are the same
        #BFS
class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("Empty Frontier")

        else:
            #first element
            node = self.frontier[0]
            #remove first element
            self.frontier.pop(0)
            return node

class Maze:
    def __init__(self, maze):
        
        #parse mazeTemplate arr

        #arr of boolean that stores true if wall, and false if no wall at that coord
        self.walls = []

        #maze has to be a square
        self.height = len(maze)
        #width is taken as longest row
        self.width = max(len(row) for row in maze)
        
        for row in range(self.height):
            walls_row = []
            for col in range(self.width):
                #coord

                try:
                    cell = maze[row][col]
                    
                    if cell == 1:
                        self.start = (row, col)
                        walls_row.append(False)
                    elif cell == 2:
                        self.goal = (row, col)
                        walls_row.append(False)
                    elif cell == 0:
                        walls_row.append(False)
                    else:
                        #wall exists
                        walls_row.append(True)
                    
                except IndexError:
                    #for rows that are shorter that the rest, they are assumed to be walls as well
                    walls_row.append(False)
                   

            self.walls.append(walls_row)
        

    def print(self, default = True, show_explored = False):
        if not default:
            solution_states = self.solution[1]
            explored = self.explored_states
        else:
            solution_states = None
            explored = None

        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                if col:
                    print("█", end="") #the end arg makes it so no new line is printed
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution_states is not None and (i, j) in solution_states:
                    print("*", end="")
                #explored states
                elif show_explored and explored is not None and (i, j) in explored:
                    print("●", end="")
                else:
                    print(" ", end="")

            print() 
        print()
        

    def solve(self, method = "DFS"):

        #keep track of the no of states explored
        self.num_states_explored = 0

        #explored states
        self.explored_states = set()

        #starting node
        start = Node(state=self.start, parent=None, action=None)
        #init frontier
        if method == "BFS":
            frontier = QueueFrontier()
        elif method == "DFS":
            frontier = StackFrontier()
        else:
            raise Exception("Enter valid method: DFS or BFS")
            

        #add starting node to frontier
        frontier.add(start)

        #loop
        while True:
            
            #if frontier is empty, there is no solution
            if frontier.empty():
                raise Exception("No Solution")

            #remove a node from the frontier
            node = frontier.remove()
            self.num_states_explored += 1

            #checking if we reached the solution
            if node.state == self.goal:
                #backtracing to the solution
                actions = []
                states = []
                while node.parent is not None:
                    actions.append(node.action)
                    states.append(node.state)
                    node = node.parent

                #reversing because they are currently from the goal to the start
                actions.reverse()
                states.reverse()
                self.solution = (actions, states)

                return
                

            #else add state to explored states
            self.explored_states.add(node.state)


            #adding neighbors to frontier if they are not already explored and are not currently in the frontier
            for action, state in self.neighbors(node.state):
                if state not in self.explored_states and not frontier.contains_state(state):
                    child_node = Node(state=state, parent=node, action=action)
                    frontier.add(child_node)

            

    def neighbors(self, state):
        row, col = state
        #candidates for states next to current state
        candidates = [("up", (row - 1, col)),
                      ("down", (row + 1, col)),
                      ("left", (row, col - 1)),
                      ("right", (row, col + 1))]

        approved_states = []
        for action, (row, col) in candidates:
            if 0 <= row < self.height and 0 <= col < self.width and not self.walls[row][col]:
                approved_states.append((action, (row, col)))

        return approved_states
        
    

def main():
    
    # 0 = empty, 1 = start, 2 = end, 3 = wall
    #has to have one start and one end
    mazeTemplate = [[3, 3, 3, 0, 0, 3, 3, 3],
                    [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 3],
                    [2, 3, 3, 0, 3, 3, 0, 0, 0, 0, 3],
                    [0, 3, 0, 0, 0, 0, 3, 3, 3, 0, 3],
                    [0, 0, 0, 3, 0, 3, 0, 0, 0, 0, 3],
                    [3, 0, 3, 3, 0, 3, 0, 0, 0, 2, 3],
                    [3, 1, 0, 0, 0, 3, 3],
                    ]


    #maze object
    #pasing in template to be parsed
    maze = Maze(mazeTemplate)

    #print unsolved maze first
    print("Maze: ")
    maze.print()
    print("Solving....")

    #solve maze using BFS or DFS
    maze.solve("BFS")

    #printing out solved maze
    print("Maze solved! ")
    print("states explored: " + str(maze.num_states_explored))
    print()
    maze.print(default=False, show_explored=False)
   
    

    

if __name__ == '__main__':
    main()









    
