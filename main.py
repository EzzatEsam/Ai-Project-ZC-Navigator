from Solvers import *
from gui import gui_handler
from Solvers import *
from map_problem import *
from loader import *


def main ():
    zc_roads = load_main_map();
    buildings_locs = load_buildings()
    gen = generator(buildings_locs= buildings_locs ,zc_map= zc_roads)
    wnd = gui_handler(gen)



if __name__ ==  "__main__":
    main()

