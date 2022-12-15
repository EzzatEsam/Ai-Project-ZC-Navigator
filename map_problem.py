from cmath import sqrt
import numpy as np

from Solvers import bfs_graph
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
        return sqrt((state[0] - self.target_state[0]) **2 + (state[1] - self.target_state[1]) **2)
    
    def step_cost(self,state,action) : return 1;

class generator :
    def __init__(self , zc_map , buildings_locs) -> None:
        self.zc_map  = zc_map;
        self.buildings_locs  = buildings_locs;
        
    def create_problem(self , current , target) : 
        prblm = Problem(road_map= self.zc_map ,targets_positions  =self.buildings_locs ,target_state= target , init_state= current)
        res = bfs_graph(prblm)
        if not res : return None
        sol , path_cost ,nodes_explored = res[0][0] , res[0][1] ,res[1]
        #print(sol)
        
        path = [ current] 
        for action in sol :
            current = prblm.result(action= action ,state= current)
            path.append(current)
        #print(path)
        return path ,path_cost ,nodes_explored
