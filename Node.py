#node class
class Node:
    def __init__(self, state = None, parent = None, action = None, goal = None):
        #the state in this case is a 2D coordinate
        self.state = state
        self.parent = parent
        self.action = action

        #heuristic is the sum of x and y distances from a state to the goal
        if goal is not None:
            self.heuristic = abs(self.state[0] - goal[0]) + abs(self.state[1] - goal[1])