#used for a stack data structure for DFS
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

    def sort_by_cost(self):
        
        #sorting the nodes in the frontier in descending order
        #so that the ones with the lowest cost are explored first
        self.frontier.sort(key = lambda x : x.cost, reverse = True)
    

#used for a queue data structure for BFS
#inherits from StackFrontier
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