from PIL import Image, ImageOps
import numpy as np

def Encoding(img_name: str, encoding_parameter: int) -> list:
    """ This Fuction takes opens an image, converts to grayscale,
        makes it a python list, and encodes it """
    img = Image.open(img_name)
    img = ImageOps.grayscale(img)
    img_list = np.asarray(img).tolist()

    for i in range(len(img_list)):
        for j in range(len(img_list[i])):
            if img_list[i][j] != 0:
                img_list[i][j] = encoding_parameter
                
    return img_list

from typing import List

def adding_img_lists(*img_lists: List[List[int]]) -> List[List[int]]:

    def adding_2d_lists(x, y):
        for i in range(len(x)):
            for j in range(len(x[i])):
                x[i][j] += y[i][j]
        return x

    output = img_lists[0]
    for i in range(1, len(img_lists)):
        adding_2d_lists(output, img_lists[i])
    
    return output