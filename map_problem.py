from cmath import sqrt

import numpy as np
from loader import *
from typing import Dict

from Solvers import *
class Problem:    
    
    def __init__(self, road_map: np.array, init_state: tuple, target_state: tuple, h_type: str = 'ecld' ,bad_road_penalty = 0):
        self.init_state = init_state
        self.road_map = road_map
        self.target_state = target_state
        self.h_type = h_type
        self.bad_road_penalty = bad_road_penalty
        
    def actions(self, state):
        nxt = []
        y ,x = state[0] , state[1]
        
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
        y, x= state[0] , state[1]
        yy, xx= self.target_state[0] , self.target_state[1]
        return yy == y and xx == x
    
    def heuristic(self,state) :
        return self.sqrt_distance(self.target_state,state) if self.h_type == 'ECLD' else self.manhatten_dist(self.target_state , state)

    def step_cost(self,state,action) : 
        y1 ,x1 = state
        y2 , x2 = self.result(state ,action)
        return (1 if (y1 == y2 or x1 == x2) else 1.41421356)  + (
            self.bad_road_penalty * (1 if (y1 == y2 or x1 == x2) else 1.41421356) if self.road_map[y2,x2] >1 else 0 );


    def sqrt_distance(self , s1 , s2) :
        return abs(sqrt((s1[0] - s2[0]) **2 + (s1[1] - s2[1]) **2)) 
    
    def manhatten_dist(self,s1,s2) :
        return abs(s1[0] - s2[0])  + abs(s1[1] - s2[1])

    

    def is_valid_target(self) : return self.road_map[self.target_state[0],self.target_state[1]] != 0

class Rooms_Problem:    
    def __init__(self, road_map: np.array, buildings_maps: Dict[str, np.array], init_state: tuple[str, str], target_state: tuple[str, str], h_type: str = 'ecld' , bad_road_penalty = 0) :
        self.bl1 = init_state[0]
        self.room1 = init_state[1]
        
        self.bl2 = target_state[0]
        self.room2 = target_state[1]

        self.index = load_buildings_rooms()[self.bl1].index(self.room1) + 2

        #self.init_state = np.where(buildings_maps[self.bl1] == self.index)[0]
        res0 = np.where(buildings_maps[self.bl1] == self.index)[0]
        res1 = np.where(buildings_maps[self.bl1] == self.index)[1]

        self.init_state = (res0[int(len(res0)/2)], res1[int(len(res0)/2)])

        self.index2 = load_buildings_rooms()[self.bl2].index(self.room2) + 2
        res0 = np.where(buildings_maps[self.bl2] == self.index2)[0]
        res1 = np.where(buildings_maps[self.bl2] == self.index2)[1]
        self.target_state = (res0[0], res1[0])

        self.road_map = road_map
        self.buildings_maps = buildings_maps 

        self.h_type = h_type
        self.bad_road_penalty = bad_road_penalty

    def actions(self, state):
        nxt = []
        y, x = state[0] , state[1]
        
        if y > 0 and (self.road_map[y - 1, x] or self.check_available(y - 1, x , state)):
            nxt.append('up')
        
        if x > 0 and (self.road_map[y, x - 1] or self.check_available(y, x - 1 , state)):
            nxt.append('left')
        
        if y < len(self.road_map) -1 and( self.road_map[y+1,x] or self.check_available(y + 1, x , state)):
            nxt.append('down')

        if x < len(self.road_map[1]) -1 and (self.road_map[y,x+1] or self.check_available(y, x + 1 , state)):
            nxt.append('right')

        if y > 0 and  x > 0 and( self.road_map[y-1,x-1] or self.check_available(y - 1, x - 1 , state)):
            nxt.append('left_up')

        if y > 0 and  x < len(self.road_map[1]) -1 and (self.road_map[y-1,x+1] or self.check_available(y - 1, x + 1, state)):
            nxt.append('right_up')

        if y < len(self.road_map) -1 and  x > 0 and (self.road_map[y+1,x-1] or self.check_available(y + 1, x - 1 , state)):
            nxt.append('left_down')

        if y < len(self.road_map) -1 and  x < len(self.road_map[1]) -1 and (self.road_map[y+1,x+1] or self.check_available(y + 1, x + 1 ,state)):
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
        y, x= state[0] , state[1]
        return self.buildings_maps[self.bl2][y, x] == self.index2  and not self.road_map[y,x]
          
    
    def heuristic(self,state):
        dist = self.sqrt_distance(self.target_state,state) if self.h_type == 'ECLD' else self.manhatten_dist(self.target_state , state) ; 
        return  dist
    

    def step_cost(self,state,action) : 
        y1 ,x1 = state
        y2 , x2 = self.result(state ,action)
        return (1 if (y1 == y2 or x1 == x2) else 1.41421356)  + (self.bad_road_penalty * (1 if (y1 == y2 or x1 == x2) else 1.41421356) if self.road_map[y2,x2] >1 else 0 );

    def sqrt_distance(self , s1 , s2) :
        return abs(sqrt((s1[0] - s2[0]) **2 + (s1[1] - s2[1]) **2)) 
    
    def manhatten_dist(self,s1,s2) :
        return abs(s1[0] - s2[0])  + abs(s1[1] - s2[1])

    def cosine_dist(self,s1,s2) :
        return (s1[0] * s2[0] +s1[0] * s2[0] ) /abs(sqrt((s1[0]**2 + s1[1]) *(s2[0]**2 + s2[1]) ) )


    def check_available(self, y, x , state):
        c_y , c_x = state
        for i in self.buildings_maps.values():
            if i[y, x] == 1 or ( i[y, x] and self.road_map[c_y,c_x] ==0 ): return True
        return False

class generator :
    def __init__(self, zc_map: np.array, buildings_locs: Dict[str, np.array]) -> None:
        self.zc_map  = zc_map;
        self.buildings_locs  = buildings_locs;
        
    def create_problem(self, current: tuple[int, int], target: tuple[int, int], algorithm: str , h ,p) : 
        prblm = Problem(road_map= self.zc_map, target_state= target , init_state= current ,
         h_type= h ,bad_road_penalty= int(p))
        if not prblm.is_valid_target() : return None;
        print(f'Algorithm {algorithm}')
        res = None
        if algorithm == 'BFS': 
            res = bfs_graph(prblm)
        elif algorithm == 'DFS':
            res = dfs(prblm)
        elif algorithm == 'IDS':
            res = ids(prblm)
        elif algorithm == 'A*':
            res = a_star_search(prblm)
        elif algorithm == 'Greedy':
            res = greedy_best_first(prblm)
        elif algorithm == 'hill_climbing':
            #pass
            res = local_search_states(prblm, 'hill_climbing')
            return res
        elif algorithm == 'Simulated Annealing':
            #pass
            res = local_search_states(prblm, 'Simulated Annealing')
            return res
        
        if not res : return None
        sol , path_cost ,nodes_explored = res[0][0] , res[0][1] ,res[1]
        
        path = [ current] 
        for action in sol :
            current = prblm.result(action= action ,state= current)
            path.append(current)
        print(self.get_instructions(sol))
        print(path)
        return path ,path_cost ,nodes_explored , 

    def create_problem_rooms(self , bl1: str, room1: str, bl2: str, room2: str, algorithm: str , h ,p):
        init_state = (bl1, room1)
        prblm = Rooms_Problem(road_map = self.zc_map, buildings_maps = self.buildings_locs, 
        init_state = init_state, target_state = (bl2, room2), h_type =h ,bad_road_penalty=int(p) )
        #if not prblm.is_valid_target() : return None;

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
        elif algorithm == 'hill_climbing':
            #pass
            res = local_search_states(prblm, 'hill_climbing')
            return res
        elif algorithm == 'Simulated Annealing':
            res = local_search_states(prblm, 'Simulated Annealing')
            return res

        
        if not res : return None
        sol, path_cost, nodes_explored = res[0][0], res[0][1], res[1]
        print(sol)
        current = prblm.init_state
        path = [current] 
        for action in sol :
            current = prblm.result(action= action ,state= current)
            path.append(current)
        print(self.get_instructions(sol))
        print(path)
        return path ,path_cost ,nodes_explored

    def get_instructions(self,path) :
        instructions = 'Instructions :'
        idx = 0
        while idx < len(path) :
            idx2 = idx +1
            while idx2 != len(path) and path[idx2] == path[idx] :
                idx2+=1
            instructions +=(f'{idx2 - idx}x {path[idx]} ,')
            idx = idx2

        return instructions
                

            
