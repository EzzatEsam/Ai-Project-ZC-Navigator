from turtle import color
from PIL import Image, ImageOps
from matplotlib.colors import Colormap
import numpy as np
import matplotlib.pyplot as plt

import cv2


def Encoding(img_name: str, encoding_parameter: int) -> np.array:
    """ This Fuction takes opens an image, converts to grayscale,
        makes it a python list, and encodes it """
    img = Image.open(img_name)
    img = ImageOps.grayscale(img)
    img_list = np.asarray(img).copy()

    img_list[img_list != 0] = encoding_parameter        
    return img_list.astype(int)

def get_rooms(img_name: str) -> np.array:
    
    img = cv2.imread(img_name)
    
    whites = (cv2.inRange(img, (250, 250, 250), (255, 255, 255)))
    reds = (cv2.inRange(img, (250, 0, 0), (255, 10, 10)))
    greens = (cv2.inRange(img, (0, 250, 0), (10, 255, 10)))
    blues = (cv2.inRange(img, (0, 0, 250), (10, 10, 255)))
    


    res = np.zeros(shape=(img.shape[0] ,img.shape[1]  ))
    res[whites.astype(bool)] = 1
    res[reds.astype(bool)] = 2
    res[greens.astype(bool)] = 3
    res[blues.astype(bool)] = 4
    return res