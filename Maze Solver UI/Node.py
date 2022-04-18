#node class
class Node:
    def __init__(self, state = None, parent = None, action = None, goal = None):
        #the state in this case is a 2D coordinate
        self.state = state
        self.parent = parent
        self.action = action

        #move number from the starting node
        if self.parent is not None:
            self.move_num = self.parent.move_num + 1
        else:
            self.move_num = 0

        #distance/heuristic is the sum of x and y distances from a state to the goal
        if goal is not None:
            distance = abs(self.state[0] - goal[0]) + abs(self.state[1] - goal[1])
            self.total_cost = distance + self.move_num