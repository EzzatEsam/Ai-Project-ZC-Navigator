from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from profiling import *     
from loader import *


BLACK = (0,0,0) 
WHITE = (255,255,255) 
BLUE = (0, 0, 128)

MAP_POS = (0,0)

WIDTH = 790
HEIGHT = 688
GEOMETRY  = '1280x720'

DROP_DOWN_X = 1000 ;
DROP_DOWN_Y = 30 ;

LABEL1_POS = (800,80)
LABEL2_POS = (800,160)
LABEL3_POS = (800,240)

BL1_POS = (839, 390)
BL2_POS = (839, 460)

ROOM1_POS = (1100, 390)
ROOM2_POS = (1100, 460)

BTN1_POS = (1021, 536)

MAP_NAME = 'map.png'

class gui_handler :
    current = None
    target = None
    current_path = []
    drawed_lines = []

    def __init__(self , gen) -> None:
        self.gen = gen
        self.buidlings = load_buildings_rooms()
        self.current_ind = None
        self.target_ind = None
        root = Tk();
        root.geometry(GEOMETRY)
        root.resizable(False, False)
        root.title('ZC pathfinder')
        root.bind("<Button 1>",lambda evnt :print((evnt.x, evnt.y)) )
        

        window = Canvas(root, width= WIDTH, height=HEIGHT)
        window.place(x =0 ,y= 0)
        window.bind("<Button 1>",self.OnMousePressedMap)
        
        img = Image.open(MAP_NAME)
        self.map_img = ImageTk.PhotoImage(img)
        self.zc_map = window.create_image(0,0 ,image = self.map_img , anchor="nw")
        
        self.label1 = Label(root  , text = '' , wraplength= 300)
        self.label1.place(x=LABEL1_POS[0] ,y=LABEL1_POS[1])
        self.label2 = Label(root  , text= '')
        self.label2.place(x=LABEL2_POS[0] ,y=LABEL2_POS[1])
        self.label3 = Label(root  , text= '')
        self.label3.place(x=LABEL3_POS[0] ,y=LABEL3_POS[1])


        options = ['BFS' , 'DFS' , 'IDS' , 'A*' , 'Greedy','HillClimbing' ,'Annealing'] 
        alg_choice = StringVar(root)
        alg_choice.set('A*')
        

        self.alg_drop_down = OptionMenu(root  , alg_choice , *options)
        self.alg_drop_down.place(x= DROP_DOWN_X ,y= DROP_DOWN_Y)
        Label(root , text= 'Algorithm').place(x= DROP_DOWN_X ,y= DROP_DOWN_Y -20)

        h_options = ['ECLD' , 'MANHATTEN'] 
        self.h_choice = StringVar(root)
        self.h_choice.set('ECLD')
        self.h_drop_down = OptionMenu(root  , self.h_choice , *h_options)
        self.h_drop_down.place(x= DROP_DOWN_X -160,y= DROP_DOWN_Y)
        Label(root , text= 'Heuristic').place(x= DROP_DOWN_X -160 ,y= DROP_DOWN_Y -20)


        buildings_opts = [str(bl) for bl in self.buidlings.keys()]
        bl1_choice = StringVar(root)
        bl1_choice.set('')
        lbl = Label(root , text= 'Current Building')
        lbl.place(x= BL1_POS[0] , y =BL1_POS[1] -20)
        bl1_drop_down =OptionMenu(root  , bl1_choice , *buildings_opts ,command= self.load_rooms1)
        bl1_drop_down.place(x= BL1_POS[0] , y =BL1_POS[1])


        bl2_choice = StringVar(root)
        bl2_choice.set('')
        lbl = Label(root , text= 'Target Building')
        lbl.place(x= BL2_POS[0] , y =BL2_POS[1] -20)
        bl1_drop_down = OptionMenu(root  , bl2_choice , *buildings_opts , command= self.load_rooms2)
        bl1_drop_down.place(x= BL2_POS[0] , y =BL2_POS[1] )

        tmp = ['Select Building First']

        room1_choice = StringVar(root)
        room1_choice.set(tmp[0])
        lbl = Label(root , text= 'Current Room')
        lbl.place(x= ROOM1_POS[0] , y =ROOM1_POS[1] -20)
        self.rm1_drop_down = OptionMenu(root  , room1_choice , *tmp )
        self.rm1_drop_down.place(x= ROOM1_POS[0] , y =ROOM1_POS[1])

        room2_choice = StringVar(root)
        room2_choice.set(tmp[0])
        lbl = Label(root , text= 'Target Room')
        lbl.place(x= ROOM2_POS[0] , y =ROOM2_POS[1] -20)
        self.rm2_drop_down = OptionMenu(root  , room2_choice , *tmp )
        self.rm2_drop_down.place(x= ROOM2_POS[0] , y =ROOM2_POS[1])

        btn1 = Button(root ,text="Get Path" , command=self.get_path_rooms )
        btn1.place(x = BTN1_POS[0] , y  = BTN1_POS[1] )



        
        self.window = window
        self.alg_choice = alg_choice
        self.b1_choice = bl1_choice
        self.b2_choice = bl2_choice
        self.room1_choice = room1_choice
        self.room2_choice = room2_choice
        self.root = root
        root.mainloop()


    def load_rooms1(self , choice) :
        self.rm1_drop_down.destroy()
        options = [str(rm) for rm in self.buidlings[choice]]
        self.room1_choice.set(options[0]) 
        self.rm1_drop_down = OptionMenu(self.root  , self.room1_choice , *options )
        self.rm1_drop_down.place(x= ROOM1_POS[0] , y =ROOM1_POS[1])

    def load_rooms2(self , choice) :
        self.rm2_drop_down.destroy()
        options = [str(rm) for rm in self.buidlings[choice]]
        self.room2_choice.set(options[0]) 
        self.rm2_drop_down = OptionMenu(self.root  , self.room2_choice , *options )
        self.rm2_drop_down.place(x= ROOM2_POS[0] , y =ROOM2_POS[1])


    def get_path_rooms(self) :
        self.reset()
        tm = timer().start()
        res =  self.gen.create_problem_rooms(  self.b1_choice.get() ,self.room1_choice.get() , self.b2_choice.get() ,self.room2_choice.get() , self.alg_choice.get() , self.h_choice.get())
        elabsed  =tm.get_elabsed()
        if res :
            self.current_path = res[0]
            self.label2.config(text =f'Path Retrieved , Nodes explored : {res[2]} \n Elabsed time {elabsed : .3e}') 
            self.label3.config(text =f'Total path Cost : {res[1] :.3f}') 

        else :
            messagebox.showinfo("Error happened", "Invalid input")
            self.current = None
        
        
        if self.current_path :
            self.draw_path()


    def OnMousePressedMap(self,evnt) :
        print(evnt.x)
        print(evnt.y)
        
        
        self.reset()


        if not self.current : 
            self.current = (evnt.y, evnt.x)
            points = [evnt.x , evnt.y , evnt.x +10 , evnt.y -20 , evnt.x -10 ,evnt.y-20]
            self.current_ind = self.window.create_polygon(points ,fill = 'green')
            self.label1.config(text= f'Current location set at {self.current}') 

        else :
            self.target = (evnt.y, evnt.x)
            points = [evnt.x , evnt.y , evnt.x +10 , evnt.y -20 , evnt.x -10 ,evnt.y-20]
            self.target_ind = self.window.create_polygon(points ,fill = 'red')
            self.label1.config(text= f'Current location set at {self.current} ,Target location set at {self.target} ') 
            self.get_path()
        

    def draw_path(self) :
        self.reset()
        if len(self.current_path) > 1 :
            lines = []
            for i in range(len(self.current_path) -1) :
                lines.append([self.current_path[i] ,self.current_path[i+1]])
            for ln in lines :
                self.drawed_lines.append(self.window.create_line(ln[0][1] , ln[0][0] , ln[1][1] , ln[1][0]  , fill="blue", width=5 )) 
                #pygame.draw.line(self.screen, BLUE, ln[0],ln[1], 5)

            x = self.current_path[0][1]
            y = self.current_path[0][0]
            points = [x , y , x +10 , y -20 , x -10 ,y-20]
            self.current_ind = self.window.create_polygon(points ,fill = 'green')
            x = self.current_path[-1][1]
            y = self.current_path[-1][0]
            points = [x , y , x +10 , y -20 , x -10 ,y-20]
            self.target_ind = self.window.create_polygon(points ,fill = 'red')

        self.current_path = []
        self.current = None
        self.target = None

    def reset(self) :
        for ln in self.drawed_lines :
            self.window.delete(ln)
        
        if self.current_ind : self.window.delete(self.current_ind)
        if self.target_ind : self.window.delete(self.target_ind)
        

    def get_path(self) :
        tm = timer().start()
        res = self.gen.create_problem(self.current ,self.target ,self.alg_choice.get(), self.h_choice.get())
        elabsed  =tm.get_elabsed()
        if res :
            self.current_path = res[0]
            self.label2.config(text =f'Path Retrieved , Nodes explored : {res[2]} \n Elabsed time {elabsed : .3e}') 
            self.label3.config(text =f'Total path Cost : {res[1] :.3f}') 

        else :
            messagebox.showinfo("Error happened", "Invalid input")
            self.current = []
        
        
        
        self.draw_path()




