

# from matplotlib.pyplot import draw
# import pygame

# BLACK = (0,0,0) 
# WHITE = (255,255,255) 
# BLUE = (0, 0, 128)

# MAP_POS = (0,0)
# LABEL1_POS = (800,80)
# LABEL2_POS = (800,160)
# LABEL3_POS = (800,240)
# WIDTH_HEIGHT = ( 1280 , 720)

# class py_game_window :
#     running = False
#     label1 = None
#     label2 = None
#     label3 = None
#     current_path = [(0,0),(100,150),(80,23), (20,58)]
#     def start(self) :
#         pygame.init()
#         clock = pygame.time.Clock()
#         pygame.display.set_caption("Zc pathfinder")
#         self.screen = pygame.display.set_mode(WIDTH_HEIGHT)
#         self.label1 = self.create_text_texture('Test1')
#         self.label2 = self.create_text_texture('Test2')
#         self.label3 = self.create_text_texture('Test3')
#         self.running = True
#         while self.running:
#             clock.tick(60)
#             self.update()
#         pygame.quit()

#     def update(self) :

#         self.draw()
#         # event handling, gets all event from the event queue
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 # change the value to False, to exit the main loop
#                 self.running = False
#             if event.type == pygame.MOUSEBUTTONDOWN :
#                 self.reset_path()
#                 print(pygame.mouse.get_pos())
#                 x , y = pygame.mouse.get_pos()
#                 if not self.current : 
#                     self.current = (y,x)
#                     self.label1 = self.create_text_texture(f'Current location set at {self.current}')
#                 else :
#                     self.target = (y ,x)
#                     self.get_path()

#         pygame.display.flip()

    
#     def reset_path(self) :
#         self.current_path = []
#         self.label1 = self.create_text_texture('hmmm')

#     def draw(self) :
#         self.screen.fill("black")
#         self.screen.blit(self.zc_map, MAP_POS)
#         self.screen.blit(self.label1, LABEL1_POS)
#         self.screen.blit(self.label2, LABEL2_POS)
#         self.screen.blit(self.label3, LABEL3_POS)
#         if len(self.current_path) > 1 :
#             lines = []
#             for i in range(len(self.current_path) -1) :
#                 lines.append([self.current_path[i] ,self.current_path[i+1]])
#             for ln in lines :
#                 pygame.draw.line(self.screen, BLUE, ln[0],ln[1], 5)
        
        




#     def create_text_texture(self,text) :
#         return  pygame.font.Font('freesansbold.ttf', 21).render(text,True,WHITE)

#     def get_path(self) :
#         res = self.gen.create_problem(self.current ,self.target)
        
#         if res[0] :
#             self.current_path = res[0]
#             self.label2 = self.create_text_texture(f'Path Retrieved , Nodes explored : {res[2]}')
#             self.label3 = self.create_text_texture(f'Total path Cost : {res[1]}')

#         self.current = None
#         self.target = None

#     def __init__(self , generator) -> None:
#         self.gen: generator = generator
#         self.zc_map = pygame.image.load('map.png')
#         self.current = None
#         self.target = None
#         self.start()
    
#         pass

