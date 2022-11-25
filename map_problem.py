import numpy as np
class Problem:    
    road_map : np.array
    def __init__(self,road_map,targets_positions , init_state):
        self.init_state = init_state
        self.road_map = road_map
        self.targets_positions = targets_positions   
        
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

    def result(self, state, action):
        if action == 'left' : return (state[0] ,state[1] -1)
        if action == 'right' : return (state[0] ,state[1] +1)
        if action == 'up' : return (state[0] -1,state[1] )
        if action == 'down' : return (state[0] +1 ,state[1])
        if action == 'left_up' : return (state[0] -1 ,state[1] -1)
        if action == 'right_up' : return (state[0] -1 ,state[1] +1)
        if action == 'left_down' : return (state[0] +1 ,state[1] -1)
        if action == 'right_down' : return (state[0] +1 ,state[1] +1)
    
    def goal_test(self, state):
        '''Returns whether or not the given state is a goal state.'''
        raise NotImplementedError
    
    def heuristic(self,state) :
        raise NotImplementedError