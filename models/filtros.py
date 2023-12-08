import numpy as np
import cv2
from skimage.util import random_noise


class Filters:
    def __init__(self, img, mask) -> None:
        self.img = img
        self.mask = mask
        self.H = self.img.shape[0]
        self.W = self.img.shape[1]
        
        
    def horizontal_flip(self,  points_numbers):
        
        img_result = np.fliplr(self.img.copy())
        mask_result = np.fliplr(self.mask.copy())
        
        flips = self.flip_img(points_numbers, True)
        black_flip = self.fill_flip(flips)
        
        return img_result, mask_result, black_flip, flips
    
    
    def vertical_flip(self, points_numbers):
        img_result = np.flip(self.img.copy(), 0)
        mask_result = np.flip(self.mask.copy(), 0)
        
        flips = self.flip_img(points_numbers, True)  
        black_flip = self.fill_flip(flips)
        
        return img_result, mask_result, black_flip, flips
    
    
    def flip_img(self, points_numbers, flip_r):
        
        flips = []
        
        for x in points_numbers:
            new_f = []
            for y in x:
                if flip_r:
                    new_f.append([abs(1-y[0]), y[1]])
                else:
                    new_f.append([y[0], abs(1-y[1])])
                    
            flips.append(new_f)  
            
        return flips
        
        
    def fill_flip(self, flips):
        
        mask_points = []
        
        for points in flips:
            mask = []
            for point in points:
                mask.append([point[0] * self.W, point[1] * self.H])
            mask_points.append(np.array(mask, np.int32))

        black_flip = 0 * np.ones(self.img.shape, np.uint8)
        
        for point in mask_points:
            pts = point.reshape(-1, 1, 2)
            cv2.fillPoly(black_flip, [pts], (255, 255, 255))
        
        return black_flip
    
    
    def noise(self):
        img_result = random_noise(self.img, mode = 'salt')
        return cv2.convertScaleAbs(img_result, alpha=(255.0))


    def gray_scale(self):
        gray_image = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY) 
        return gray_image
    
    