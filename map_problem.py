from cmath import sqrt
import numpy as np

from Solvers import a_star_search, bfs_graph, dfs, greedy_best_first, ids
class Problem:    
    road_map : np.array

    def __init__(self,road_map,targets_positions , init_state , target_state):
        self.init_state = init_state
        self.road_map = road_map
        self.targets_positions = targets_positions   
        self.target_state = target_state
        
    def actions(self, state):
        nxt = []
        y ,x= state[0] , state[1]
        
        if y > 0 and self.road_map[y-1,x] :
            nxt.append('up')
        
        if x > 0 and self.road_map[y,x-1] :
            nxt.append('left')
        
        if y < len(self.road_map) -1 and self.road_map[y+1,x] :
            nxt.append('down')

        if x < len(self.road_map[1]) -1 and self.road_map[y,x+1] :
            nxt.append('right')

        if y > 0 and  x > 0 and self.road_map[y-1,x-1] :
            nxt.append('left_up')

        if y > 0 and  x < len(self.road_map[1]) -1 and self.road_map[y-1,x+1] :
            nxt.append('right_up')

        if y < len(self.road_map) -1 and  x > 0 and self.road_map[y+1,x-1] :
            nxt.append('left_down')

        if y < len(self.road_map) -1 and  x < len(self.road_map[1]) -1 and self.road_map[y+1,x+1] :
            nxt.append('right_down')
        
        
        return nxt

    def result(self, state, action):
        #print(state , action)
        if action == 'left' : return (state[0] ,state[1] -1)
        if action == 'right' : return (state[0] ,state[1] +1)
        if action == 'up' : return (state[0] -1,state[1] )
        if action == 'down' : return (state[0] +1 ,state[1])
        if action == 'left_up' : return (state[0] -1 ,state[1] -1)
        if action == 'right_up' : return (state[0] -1 ,state[1] +1)
        if action == 'left_down' : return (state[0] +1 ,state[1] -1)
        if action == 'right_down' : return (state[0] +1 ,state[1] +1)
    
    def goal_test(self, state):
        y ,x= state[0] , state[1]
        yy ,xx= self.target_state[0] , self.target_state[1]
        return yy ==y and xx == x
        #return state == self.target_state       
    
    def heuristic(self,state) :
        return abs(sqrt((state[0] - self.target_state[0]) **2 + (state[1] - self.target_state[1]) **2)) 
    
    def step_cost(self,state,action) : 
        return self.sqrt_distance(state , self.result(state,action));

    def sqrt_distance(self , s1 , s2) :
        return abs(sqrt((s1[0] - s2[0]) **2 + (s1[1] - s2[1]) **2)) 

    def is_valid_target(self) : return self.road_map[self.target_state[0],self.target_state[1]] != 0


class generator :
    def __init__(self , zc_map , buildings_locs) -> None:
        self.zc_map  = zc_map;
        self.buildings_locs  = buildings_locs;
        
    def create_problem(self , current , target , algorithm) : 
        prblm = Problem(road_map= self.zc_map ,targets_positions  =self.buildings_locs ,target_state= target , init_state= current)
        if not prblm.is_valid_target() : return None;
        print(f'Algorithm {algorithm}')
        res = None
        if algorithm == 'BFS' : 
            res = bfs_graph(prblm)
        elif algorithm == 'DFS' :
            res = dfs(prblm)
        elif algorithm == 'IDS' :
            res = ids(prblm)
        elif algorithm == 'A*' :
            res = a_star_search(prblm)
        elif algorithm == 'Greedy' :
            res = greedy_best_first(prblm)

        
        if not res : return None
        sol , path_cost ,nodes_explored = res[0][0] , res[0][1] ,res[1]
        print(sol)
        
        path = [ current] 
        for action in sol :
            current = prblm.result(action= action ,state= current)
            path.append(current)
        #print(path)
        return path ,path_cost ,nodes_explored

    def create_problem_rooms(self , bl1 ,room1 , bl2 ,room2) :
        pass
