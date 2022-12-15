from collections import deque


class Node:
    '''Node data structure for search space bookkeeping.'''
    _child_index : int = 0
    def __init__(self, state, parent, action, path_cost):
        '''Constructor for the node state with the required parameters.'''
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self._child_index = 0 if parent is None else parent.get_child_index() +1

    @classmethod
    def root(cls, init_state):
        '''Factory method to create the root node.'''
        return cls(init_state, None, None, 0)

    

    @classmethod
    def child(cls, problem, parent, action):
        '''Factory method to create a child node.'''
        return cls(
            problem.result(parent.state, action),
            parent,
            action,
            parent.path_cost + problem.step_cost(parent.state, action))
    
    def get_child_index(self) -> int :
        return self._child_index

def solution(node):
    '''A method to extract the sequence of actions representing the solution from the goal node.'''
    actions = []
    cost = node.path_cost
    while node.parent is not None:
        actions.append(node.action)
        node = node.parent
    actions.reverse()
    return actions, cost

def bfs_graph(problem):
    '''Breadth-first graph search implementation.'''
    if problem.goal_test(problem.init_state): return solution(Node.root(problem.init_state))
    frontier = deque([Node.root(problem.init_state)])
    explored = {problem.init_state}
    
    while frontier:
        node = frontier.pop()
        #print(node.chld_count())
        for action in problem.actions(node.state):
            child = Node.child(problem, node, action)
            if child.state not in explored:
                if problem.goal_test(child.state):
                    return solution(child) , len(explored) +1
                frontier.appendleft(child)
                explored.add(child.state)

def dfs(problem , verbose :bool =1) :    
    if problem.goal_test(problem.init_state): return solution(Node.root(problem.init_state))
    frontier = deque([Node.root(problem.init_state)])
    explored = {problem.init_state}
    #if verbose: visualizer = Visualizer(problem)
    while frontier:
        #if verbose: visualizer.visualize(frontier)
        node = frontier.pop()
        for action in problem.actions(node.state):
            child = Node.child(problem, node, action)
            if child.state not in explored:
                if problem.goal_test(child.state):
                    return solution(child)
                frontier.append(child)
                explored.add(child.state)
            
def dls(problem , limit , verbose : bool = 1) :
    if problem.goal_test(problem.init_state): return solution(Node.root(problem.init_state))
    frontier = deque([Node.root(problem.init_state)])
    #if verbose: visualizer = Visualizer(problem)
    while frontier:
        #if verbose: visualizer.visualize(frontier)
        node = frontier.pop()
        print('child index :',node.get_child_index())
        if node.get_child_index() < limit :
            for action in problem.actions(node.state):
                child = Node.child(problem, node, action)
                if problem.goal_test(child.state):
                    return solution(child)
                frontier.append(child)

def ids(problem  ,start_limit = 0 ,  verbose : bool = 1) :
    limit = start_limit
    while 1 :
        result = dls(problem,limit,verbose)
        if result is not None :
            return result
        limit += 1