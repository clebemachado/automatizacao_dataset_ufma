import cv2
import json
import numpy as np
import pandas as pd
import shortuuid
import itertools 

class Utils:
    
    def generate_name(self, path):
        return f"{path.parent.stem}_{shortuuid.uuid()}"


    def generate_name_img(self, path):
        return f"{path.parent.stem}_{path.stem}_{shortuuid.uuid()}"
    
    
    def read_img(self, path):
        return cv2.imread(str(path.resolve()))
    
    
    def convert_yolo(self, file):
    
        image_height = file["imageHeight"]
        image_width = file["imageWidth"]
        
        classe = "0"
        point_txt = []
        points_numbers = []
        
        for shape in file["shapes"]:
            txt = f"{classe}"
            numbers = []
            for w, h in  shape["points"]:
                result = [float(w)/image_width , float(h)/image_height]
                txt = f'{txt} {result[0]} {result[1]}'
                numbers.append(result)
                
            point_txt.append(txt)
            points_numbers.append(numbers)
            
        return point_txt, points_numbers
        
    
    def get_points(self, path):
    
        point_mask = None
        point_txt = None
        points_numbers = None
        
        with open(path.resolve()) as file:
            load = json.load(file)
            point_mask = [np.array(data["points"], np.int32) for data in load["shapes"] if data["shape_type"] == "polygon"]
            point_txt, points_numbers = self.convert_yolo(load)
            
        return point_mask, point_txt, points_numbers

    def points_to_txt(self, points):
        
        marcacoes = []
        for n_p in points:
            result = ["0"] + list(itertools.chain.from_iterable(n_p))
            marcacoes.append(" ".join(map(str, result)))
            
        return marcacoes 
     