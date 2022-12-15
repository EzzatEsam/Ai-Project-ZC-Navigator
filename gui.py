from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import ttk

BLACK = (0,0,0) 
WHITE = (255,255,255) 
BLUE = (0, 0, 128)

MAP_POS = (0,0)
LABEL1_POS = (800,80)
LABEL2_POS = (800,160)
LABEL3_POS = (800,240)
WIDTH = 790
HEIGHT = 688
GEOMETRY  = '1280x720'

DROP_DOWN_X = 1000 ;
DROP_DOWN_Y = 20 ;

LABEL1_POS = (800,80)
LABEL2_POS = (800,160)
LABEL3_POS = (800,240)

MAP_NAME = 'map.png'

class gui_handler :
    current = None
    target = None
    path = []
    drawed_lines = []

    def __init__(self , gen) -> None:
        self.gen = gen
        root = Tk();
        root.geometry(GEOMETRY)
        

        window = Canvas(root, width= WIDTH, height=HEIGHT)
        window.place(x =0 ,y= 0)
        window.bind("<Button 1>",self.OnMousePressed)
        
        img = Image.open(MAP_NAME)
        self.map_img = ImageTk.PhotoImage(img)
        self.zc_map = window.create_image(0,0 ,image = self.map_img , anchor="nw")
        
        self.label1 = Label(root  , text = 'Label 1')
        self.label1.place(x=LABEL1_POS[0] ,y=LABEL1_POS[1])
        self.label2 = Label(root  , text= 'Label 1')
        self.label2.place(x=LABEL2_POS[0] ,y=LABEL2_POS[1])
        self.label3 = Label(root  , text= 'Label 1')
        self.label3.place(x=LABEL3_POS[0] ,y=LABEL3_POS[1])


        options = ['BFS' , 'DFS' , 'DLS' , 'A*']
        alg_choice = StringVar(root)
        alg_choice.set('BFS')
        

        self.drop_down = OptionMenu(root  , alg_choice , *options)
        self.drop_down.place(x= DROP_DOWN_X ,y= DROP_DOWN_Y)
        
        self.window = window
        root.mainloop()



    def OnMousePressed(self,evnt) :
        print(evnt.x)
        print(evnt.y)
        if not self.current : 
            self.current = (evnt.y, evnt.x)
            self.label1.config(text= f'Current location set at {self.current}') 

        else :
            self.target = (evnt.y, evnt.x)
            self.label1.config(text= f'Current location set at {self.current} ,Target location set at {self.target} ') 
            self.get_path()
        

    def draw_path(self) :
        for ln in self.drawed_lines :
            self.window.delete(ln)

        if len(self.current_path) > 1 :
            lines = []
            for i in range(len(self.current_path) -1) :
                lines.append([self.current_path[i] ,self.current_path[i+1]])
            for ln in lines :
                self.drawed_lines.append(self.window.create_line(ln[0][1] , ln[0][0] , ln[1][1] , ln[1][0]  , fill="blue", width=5 )) 
                #pygame.draw.line(self.screen, BLUE, ln[0],ln[1], 5)

    def get_path(self) :
        res = self.gen.create_problem(self.current ,self.target)
        if res :
            self.current_path = res[0]
            self.label2.config(text =f'Path Retrieved , Nodes explored : {res[2]}') 
            self.label3.config(text =f'Total path Cost : {res[1]}') 

        else :
            messagebox.showinfo("Error happened", "Invalid input")
            self.current = []
        
        self.current = None;
        self.target = None;
        
        self.draw_path()




