import numpy as np
import os
import shutil
import cv2 as cv

class Processor:
    def __init__(self, size):
        self.SIZE = size
        self.texture_path = 'pack/assets/minecraft/textures'
        self.types = ['block']

    def init_dir(self):
        if(os.path.exists(self.texture_path)):
            shutil.rmtree(self.texture_path)
        os.makedirs(self.texture_path)
        for type in self.types:
            os.mkdir(f'{self.texture_path}/{type}')
            

    def process(self, type):
        #cv.IMREAD_COLOR : BGR layer
        #cv.IMREAD_UNCHANGED : BGR layer + alpha
        input_path = f'raw_images/{type}'
        output_path = f'{self.texture_path}/{type}'

        for file in os.listdir(input_path):
            input_img = cv.imread(f'{input_path}/{file}',cv.IMREAD_COLOR)
            img = cv.resize(input_img, (self.SIZE, self.SIZE))
            # cv.imshow(name, img)
            # cv.waitKey(0)
            cv.imwrite(f'{output_path}/{file}',img)
