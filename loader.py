import json
from BasicFunctions import *
import numpy as np
import json
from typing import Dict

zc_map_name = 'path.png'
hb_name = 'HB_INT.png'
nb_name = 'NB_INT.png'
ab_name = 'AB_INT.png'
dorms_name = 'dorms.png'

def load_main_map():
    return get_colors_encoding(img_name= zc_map_name)

def load_buildings() -> Dict[str, np.array]:
    blds = {}
    blds['HB'] = get_colors_encoding(hb_name)
    blds['AB'] = get_colors_encoding(ab_name)
    blds['DORMS'] = get_colors_encoding(dorms_name )
    blds['NB'] = get_colors_encoding(nb_name)
    return blds

def load_buildings_rooms() -> Dict[str, list]:
    js = json.load(open('interiors.json'))
    res = {}
    for key , val in js.items() :
        res[key] = [str(key) for key in val.keys() ] 
    return(res)



    
        
    

    
