from multiprocessing import Event
from tracemalloc import start
from turtle import update
from matplotlib.pyplot import draw
import pygame

BLACK = (0,0,0) 
WHITE = (255,255,255) 
BLUE = (0, 0, 128)

MAP_POS = (0,0)
LABEL1_POS = (850,80)
LABEL2_POS = (850,160)
LABEL3_POS = (850,240)


class py_game_window :
    running = False
    label1 = None
    label2 = None
    label3 = None
    current_path = [(0,0),(100,150),(80,23), (20,58)]
    def start(self) :
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Zc pathfinder")
        self.screen = pygame.display.set_mode((1000   ,650))
        self.label1 = self.create_text_texture('Test1')
        self.label2 = self.create_text_texture('Test2')
        self.label3 = self.create_text_texture('Test3')
        self.running = True
        while self.running:
            clock.tick(60)
            self.update()
        pygame.quit()

    def update(self) :

        self.draw()
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN :
                self.reset_path()

        pygame.display.flip()

    
    def reset_path(self) :
        self.current_path = []
        self.label1 = self.create_text_texture('hmmm')

    def draw(self) :
        self.screen.fill("black")
        self.screen.blit(self.zc_map, MAP_POS)
        self.screen.blit(self.label1, LABEL1_POS)
        self.screen.blit(self.label2, LABEL2_POS)
        self.screen.blit(self.label3, LABEL3_POS)
        if len(self.current_path) > 1 :
            lines = []
            for i in range(len(self.current_path) -1) :
                lines.append([self.current_path[i] ,self.current_path[i+1]])
            for ln in lines :
                pygame.draw.line(self.screen, BLUE, ln[0],ln[1], 5)
        
        




    def create_text_texture(self,text) :
        return  pygame.font.Font('freesansbold.ttf', 32).render(text,True,WHITE)

    def __init__(self) -> None:
        self.zc_map = pygame.image.load('map.png')
        self.start()
    
        pass

