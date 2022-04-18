from Frontiers import StackFrontier, QueueFrontier
from Node import Node

class MazeSolver():
    
    def parse_maze(self, maze):
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

        #making sure there is a start and end
        if self.start is None or self.goal is None:
            return None
        
        return 1
        
    def solve_maze(self, method):
        
        #keep track of the no of states explored
        self.num_states_explored = 0

        #explored states
        self.explored = []

        #starting node
        start = Node(state=self.start, parent=None, action=None, goal=self.goal)

        #init frontier depending on method
        if method == "A* Search" or method == "Depth First Search":
            frontier = StackFrontier()
        elif method == "Breadth First Search":
            frontier = QueueFrontier()

        #add starting node to frontier
        frontier.add(start)

        #loop
        while True:
            
            #if frontier is empty, there is no solution
            if frontier.empty():
                return None, None

            #remove a node from the frontier
            node = frontier.remove()
            self.num_states_explored += 1

            #checking if we reached the solution
            if node.state == self.goal:
                #backtracing to the solution
                states = []
                while node.parent is not None:
                    states.append(node.state)
                    node = node.parent
                    
                #reversing because they are currently from the goal to the start
                states.reverse()
                self.solution = states
                return self.solution, self.explored

            #else add state to explored states
            self.explored.append(node.state)

            #adding neighbors to frontier if they are not already explored and are not currently in the frontier
            for action, state in self.neighbors(node.state):
                if state not in self.explored and not frontier.contains_state(state):
                    child_node = Node(state=state, parent=node, action=action, goal = self.goal)
                    frontier.add(child_node)

            #sorting the nodes in the frontier are in descending order
            #so that the ones with the lowest cost are explored first
            if method == "A* Search":
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