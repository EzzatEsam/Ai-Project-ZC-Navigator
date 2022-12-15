from collections import deque
from heapq import heappop, heappush
from itertools import count


class Node:
    '''Node data structure for search space bookkeeping.'''
    _child_index : int = 0
    def __init__(self, state, parent, action, path_cost, heuristic):
        '''Constructor for the node state with the required parameters.'''
        self.state = state
        self.parent = parent
        self.action = action
        self.g = path_cost
        self.h = heuristic
        self.f = path_cost + heuristic
        self._child_index = 0 if parent is None else parent.get_child_index() +1

    @classmethod
    def root(cls, problem):
        '''Factory method to create the root node.'''
        init_state = problem.init_state
        return cls(init_state, None, None, 0, problem.heuristic(init_state))

    

    @classmethod
    def child(cls, problem, parent, action):
        '''Factory method to create a child node.'''
        child_state = problem.result(parent.state, action)
        return cls(
            child_state,
            parent,
            action,
            parent.g + problem.step_cost(parent.state, action),
            problem.heuristic(child_state))
    
    def get_child_index(self) -> int :
        return self._child_index

def solution(node):
    '''A method to extract the sequence of actions representing the solution from the goal node.'''
    actions = []
    cost = node.g
    while node.parent is not None:
        actions.append(node.action)
        node = node.parent
    actions.reverse()
    return actions, cost

def bfs_graph(problem):
    '''Breadth-first graph search implementation.'''
    if problem.goal_test(problem.init_state): return solution(Node.root(problem.init_state))
    frontier = deque([Node.root(problem)])
    explored = {problem.init_state}
    
    while frontier:
        node = frontier.pop()
        
        for action in problem.actions(node.state):
            child = Node.child(problem, node, action)
            if child.state not in explored:
                if problem.goal_test(child.state):
                    return solution(child) , len(explored) +1
                frontier.appendleft(child)
                explored.add(child.state)

def dfs(problem , verbose :bool =1) :    
    if problem.goal_test(problem.init_state): return solution(Node.root(problem.init_state))
    frontier = deque([Node.root(problem)])
    explored = {problem.init_state}
    #if verbose: visualizer = Visualizer(problem)
    while frontier:
        #if verbose: visualizer.visualize(frontier)
        node = frontier.pop()
        for action in problem.actions(node.state):
            child = Node.child(problem, node, action)
            if child.state not in explored:
                if problem.goal_test(child.state):
                    return solution(child) , len(explored) +1
                frontier.append(child)
                explored.add(child.state)
            
def dls(problem , limit , verbose : bool = 1) :
    if problem.goal_test(problem.init_state): return solution(Node.root(problem.init_state))
    frontier = deque([Node.root(problem)])
    explored = 0
    #if verbose: visualizer = Visualizer(problem)
    while frontier:
        #if verbose: visualizer.visualize(frontier)
        node = frontier.pop()
        
        if node.get_child_index() < limit :
            for action in problem.actions(node.state):
                explored += 1
                child = Node.child(problem, node, action)
                if problem.goal_test(child.state):
                    return solution(child)  , explored
                frontier.append(child)
    return None , explored

def ids(problem  ,start_limit = 0 ,  verbose : bool = 1) :
    limit = start_limit
    explored =0
    while 1 :
        result = dls(problem,limit,verbose)
        if result[0] is not None :
            return result[0] , explored + result[1]
        explored += result[1]
        limit += 1


def greedy_best_first(problem, verbose=False):
    '''Greedy best-first search implementation.'''
    counter = count()
    frontier = [(None, None, Node.root(problem))]
    explored = set()

    while frontier:
        _, _, node = heappop(frontier)
        if node.state in explored: continue
        if problem.goal_test(node.state):
            
            return solution(node) , len(explored) +1
        explored.add(node.state)
        for action in problem.actions(node.state):
            child = Node.child(problem, node, action)
            if child.state not in explored:
                heappush(frontier, (child.h, next(counter), child))

def uniform_cost_search(problem, verbose=False):
    counter = count()
    frontier = [(None, None, Node.root(problem))]
    explored = set()
    while frontier:

        _, _, node = heappop(frontier)
        if node.state in explored: continue
        if problem.goal_test(node.state):
            
            return solution(node) , len(explored) +1
        explored.add(node.state)
        for action in problem.actions(node.state):
            child = Node.child(problem, node, action)
            if child.state not in explored:
                heappush(frontier, (child.g, next(counter), child))

def a_star_search(problem, verbose=False):
    counter = count()
    frontier = [(None, None, Node.root(problem))]
    explored = set()

    while frontier:
        _, _, node = heappop(frontier)
        if node.state in explored: continue
        if problem.goal_test(node.state):
           
            return solution(node) , len(explored) +1
        explored.add(node.state)
        for action in problem.actions(node.state):
            child = Node.child(problem, node, action)
            if child.state not in explored:
                heappush(frontier, (child.g+ child.h, next(counter), child))