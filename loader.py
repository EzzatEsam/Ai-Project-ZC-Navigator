from BasicFunctions import *
import numpy as np

zc_map_name = 'path.png'
hb_name = 'hb.png'
nb_name = 'nb.png'
ab_name = 'ab.png'
dorms_name = 'dorms.png'

def load_main_map() :
    np.savetxt("test.csv", Encoding(encoding_parameter=1 ,img_name= zc_map_name),fmt='%d' ,delimiter=",")
    return Encoding(encoding_parameter=1 ,img_name= zc_map_name)

def load_buildings() :
    blds = {}
    blds['Helmy'] = Encoding(img_name=hb_name ,encoding_parameter=1)
    blds['Academic'] = Encoding(img_name=ab_name ,encoding_parameter=1)
    blds['Dorms'] = Encoding(img_name=dorms_name ,encoding_parameter=1)
    blds['nano'] = Encoding(img_name=nb_name ,encoding_parameter=1)
    return blds

