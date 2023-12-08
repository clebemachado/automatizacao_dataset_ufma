from pathlib import Path
import pandas as pd
import  cv2, shutil
import numpy as np
from .utils import Utils
from .select_filter import SelectFilter
import streamlit 
from stqdm import stqdm
from .filtros import Filters

class Process:
    
    def __init__(self, input: str, output: str, select_filter: SelectFilter) -> None:
        self.input = Path(input)
        self.ouput = Path(output)
        self.treinamento = None
        self.utils = Utils()
        self.select_filter = select_filter
    
    def init(self):
        
        RANDOM_STATE = 42
        df = pd.DataFrame(list(self.input.iterdir()), columns=['path'])
        self.treinamento = df.sample(15, random_state = RANDOM_STATE).stack().to_list()
        self.create_path()
        
    
    def create_path(self):

        if(self.ouput.exists()):
            shutil.rmtree(self.ouput)

        self.ouput.mkdir(parents=False, exist_ok=True)


        (self.ouput / 'train'/ 'images').mkdir(parents=True, exist_ok=True)
        (self.ouput / 'train'/ 'labels').mkdir(parents=True, exist_ok=True)

        (self.ouput / 'test'/ 'images').mkdir(parents=True, exist_ok=True)
        (self.ouput / 'test' / 'labels').mkdir(parents=True, exist_ok=True)
        
    
    def save_images_and_txt(self, img, points_txt, file_name, save_path='train'):
    
        path = self.ouput / f'{save_path}'
        img_save = (path / 'images'/ f'{file_name}.jpg').resolve()
        label_save = path / 'labels'/ f'{file_name}.txt'
        
        cv2.imwrite(str(img_save), img)
            
        with open(label_save, "w") as f:
            for point in points_txt:
                f.write(point + "\n")
                
    def save_test(self):
        
        teste = [path for path in self.input.iterdir() if path not in self.treinamento]

        imagens_folders_teste = sorted([path for path in self.input.rglob("*IMG_*.jpg") if path.parent in teste])
        labels_folders_teste = sorted([path for path in self.input.rglob("*IMG_*.json") if path.parent in teste])
        
        if len(imagens_folders_teste) != len(labels_folders_teste):
            raise Exception("A quantidade de Imagens e Labels devem ser iguais.")
        
        
        for img_path, json_path in stqdm(zip(imagens_folders_teste, labels_folders_teste), total=len(imagens_folders_teste)):
    
            img = self.utils.read_img(img_path)
            _, _, points_numbers = self.utils.get_points(json_path)
            points_txt = self.utils.points_to_txt(points_numbers)
            
            filename = self.utils.generate_name_img(img_path)
            
            self.save_images_and_txt(img, points_txt, filename, 'test')
    
    
    def create_image_treinamento(self, img_file, json_file):
        X = []
        Y = []
        
        point_mask, _, points_numbers = self.utils.get_points(json_file)
        
        img = cv2.imread(str(img_file.resolve()))
        points_txt_original = self.utils.points_to_txt(points_numbers)
        
        X.append(img)
        Y.append(points_txt_original)
        
        
        mask = 0 * np.ones(img.shape, np.uint8)

        for point in point_mask:
            pts = point.reshape(-1, 1, 2)
            cv2.fillPoly(mask, [pts], (255, 255, 255))
            
        filters = Filters(img, mask)
        
        # Noise - Salvar  o mesmo TXT
        if self.select_filter.noise:
            img_noise = filters.noise()
            X.append(img_noise)
            Y.append(points_txt_original)
        
        # Gray Scale - Mesmo TXT
        if self.select_filter.gray:
            img_gray = filters.gray_scale()
            X.append(img_gray)
            Y.append(points_txt_original)
            
        # Horizontal_Flip - TXT MUDA
        if self.select_filter.horizontal:
            img_flip_horizontal, _, _, pontos_flip_horizontal = filters.horizontal_flip(points_numbers)
            pontos_flip_horizontal = self.utils.points_to_txt(pontos_flip_horizontal)
            X.append(img_flip_horizontal)
            Y.append(pontos_flip_horizontal)
        
        # Vertical Flip - TXT MUDA
        if self.select_filter.vertical:
            img_flip_vertical, _, _, pontos_flip_vertical = filters.vertical_flip(points_numbers)
            pontos_flip_vertical = self.utils.points_to_txt(pontos_flip_vertical)
            X.append(img_flip_vertical)
            Y.append(pontos_flip_vertical)
        
        return X, Y


    def save_treinament(self):
        imgs_folders = sorted([path for path in self.input.rglob("*IMG_*.jpg") if path.parent in self.treinamento])
        json_folders = sorted([path for path in self.input.rglob("*IMG_*.json") if path.parent in self.treinamento])
        
        if len(imgs_folders) != len(json_folders):
            raise Exception("A quantidade de Imagens e Labels devem ser iguais.")
        
        for img_path, json_path in stqdm(zip(imgs_folders, json_folders), total = len(imgs_folders)):
            X, Y = self.create_image_treinamento(img_path, json_path)
            
            cont = 0
            for img, file in zip(X, Y):
                try:
                    file_name = f"{self.utils.generate_name_img(img_path)}_process_{cont}"
                    self.save_images_and_txt(img, file, file_name)
                    cont += 1
                except:
                    print(f"ERRO: {img_path.stem} count: {cont}, len: {len(X)}" )
            
            print(f"Finalizado para path: {img_path}")
    

        
    