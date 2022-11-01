from algorithms.frontiers import StackFrontier
from algorithms.node import Node
from algorithms.maze_text_to_array_converter import convertTextFile

#uses A* search
#calculates the most optimal path, but explores more states as a result

#only heuristic search will not always calculate optimal path, but will explore lesser states


class Maze:
    def __init__(self, maze):

        #parse 2d maze array

        #arr of boolean that stores true if wall, and false if no wall at that coord
        self.walls = []

        self.start = None
        self.goal = None

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
                    
                    if cell == 'A':
                        self.start = (row, col)
                        walls_row.append(False)
                    elif cell == 'B':
                        self.goal = (row, col)
                        walls_row.append(False)
                    
                    if cell == ' ':
                        walls_row.append(False)
                    elif cell == '#':
                        #wall exists
                        walls_row.append(True)
                    
                except IndexError:
                    #for rows that are shorter that the rest, they are assumed to be clear cells
                    walls_row.append(False)

            self.walls.append(walls_row)                 

        #setting up solution and explored arr
        self.solution = [[], []]
        self.explored = []

        #making sure there is a start and end
        if self.start is None or self.goal is None:
            raise Exception("needs one start and end cell")

    def print(self, show_solution = False, show_explored = False):
        solution = self.solution[1] #only the states

        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                if col:
                    print("█", end="") #the end arg makes it so no new line is printed
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal: 
                    print("B", end="")
                elif show_solution and (i, j) in solution:
                    print("*", end="")
                #explored states
                elif show_explored and (i, j) in self.explored:
                    print("●", end="")
                else:
                    print(" ", end="")

            print() 
        print()

    def solve(self):

        #keep track of the no of states explored
        self.num_states_explored = 0

        #explored states
        self.explored = set()

        #starting node
        start = Node(state=self.start, parent=None, action=None, goal=self.goal)
        #init frontier
        frontier = StackFrontier()


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
                return self.solution

            #else add state to explored states
            self.explored.add(node.state)

            #adding neighbors to frontier if they are not already explored and are not currently in the frontier
            for action, state in self.neighbors(node.state):
                if state not in self.explored and not frontier.contains_state(state):
                    child_node = Node(state=state, parent=node, action=action, goal = self.goal)
                    frontier.add(child_node)

            #sorting the nodes in the frontier are in descending order
            #so that the ones with the lowest cost are explored first
            frontier.sort_by_cost()  

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

    #pasing in file to be parsed
    mazeTemplate = convertTextFile("mazes/maze8.txt")
    #maze object
    maze = Maze(mazeTemplate)

    #print unsolved maze first
    print("Maze: ")
    maze.print()
    print("Solving....")

    maze.solve()

    #printing out solved maze
    print("Maze solved! ")
    print("states explored: " + str(maze.num_states_explored))
    print()
    maze.print(show_solution=True, show_explored=False)   

if __name__ == '__main__':
    main()









    
