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
    np.savetxt("test.csv", Encoding(encoding_parameter=1 ,img_name= zc_map_name),fmt='%d' ,delimiter=",")
    return Encoding(encoding_parameter=1 ,img_name= zc_map_name)

def load_buildings() -> Dict[str, np.array]:
    blds = {}
    blds['HB'] = get_rooms(hb_name)
    blds['AB'] = get_rooms(ab_name)
    blds['Dorms'] = Encoding(img_name=dorms_name ,encoding_parameter=1)
    blds['NB'] = get_rooms(nb_name)
    return blds

def load_buildings_rooms() -> Dict[str, list]:
    js = json.load(open('interiors.json'))
    res = {}
    for key , val in js.items() :
        res[key] = [str(key) for key in val.keys() ] 
    return(res)



    
        
    

    
