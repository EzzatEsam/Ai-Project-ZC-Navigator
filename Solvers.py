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
    if problem.goal_test(problem.init_state): return solution(Node.root(problem))
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
    if problem.goal_test(problem.init_state): return solution(Node.root(problem))
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
            
def dls(problem , limit ) :
    if problem.goal_test(problem.init_state): return solution(Node.root(problem))
    frontier = deque([Node.root(problem)])
    explored = 0
    
    #print(limit)
    while frontier:

        node = frontier.pop()
        print(limit)
        print(f'Index {node.get_child_index()}')
        for action in problem.actions(node.state):
            explored += 1
            child = Node.child(problem, node, action)
            if child.get_child_index() < limit : 
                if problem.goal_test(child.state):
                    return solution(child)  , explored
                frontier.append(child)
    return None , explored 

def ids(problem  ,start_limit = 0) :
    limit = start_limit
    explored =0
    while 1 :
        result = dls(problem,limit)
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

def uniform_cost_search(problem):
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

states_list = []

def hill_climbing(problem, verbose = False):
    ''' Hill climbing search implementation.'''
    current_state = problem.init_state
    current_value = problem.heuristic(current_state)

    if verbose: visualizer = Visualizer(problem)
    while True:
        if verbose: visualizer.visualize([current_state])
        next_state, next_value = None, None

        for action in problem.actions(current_state):
            new_state = problem.result(current_state, action)
            new_value = problem.heuristic(new_state)

            if next_value is None or next_value > new_value:
                next_state, next_value = new_state, new_value

        if current_value <= next_value: return current_state
        current_state, current_value = next_state, next_value
        states_list.append(current_state)

def random_restart_hill_climbing(problem, verbose=False):
    '''Random-restart hill climbing search implementation.'''
    while True:  # Keep repeating till the problem is solved
        #problem = problem_gen()  # Generate a new problem instance (only works if each problem instance is different from the previous, e.g., random initial state)
        solution_state = hill_climbing(problem, verbose)  # Try to solve the problem instance with hill climbing
        if problem.goal_test(solution_state):  return solution_state  # If succeeded, return the solution

from random import choice, random
from math import exp
from itertools import count

def simulated_annealing(problem, schedule, verbose=False):
    '''Simulated annealing search implementation.'''
    current_state = problem.init_state
    current_value = problem.heuristic(current_state)

    if verbose: visualizer = Visualizer(problem)
    for t in count():
        
        if verbose: visualizer.visualize([current_state])
        T = schedule(t)  # A function that determines the "temperature" (acceptability of a bad state) as a function of the step count
        
        if current_value is 0 or T is 0: return current_state  # Return if a goal state is found or if the temperature hits 0
        next_states = [problem.result(current_state, action) for action in problem.actions(current_state)]  # Generate all possible next states
        
        while True:  # Repeat the following till the current state is updated
            next_state = choice(next_states)  # Choose a random next state
            states_list.append(next_state)
            next_value = problem.heuristic(next_state)
            delta = current_value - next_value
            if delta > 0 or random() < exp(delta / T):  # Accept the randomly chosen state immediately if it is better than the current state or with a probability (exponentially) proportional to the temperature and how bad it is
                current_state, current_value = next_state, next_value
                states_list.append(current_state)
                break


def local_search_states(problem, type): 
    states_list.clear()
    if type == 'hill_climbing': hill_climbing(problem)
    elif type == 'Simulated Annealing': simulated_annealing(problem, lambda t: exp(-t))
    return states_list