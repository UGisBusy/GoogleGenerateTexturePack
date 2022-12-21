import numpy as np
import os
import shutil
import cv2 as cv

class Processor:
    def __init__(self, resultion=128, types=[], pack_name='hell', raw_images_path='raw_images' ,buffer_path='buffer', result_path='result'):
        '''
        resultion:               the resultion of the image
        types:              types we want to be included in the pack
        raw_images_path:    the path of the raw images crawled
        buffer_path:        the path of the processed images
        result_path:        the path of the compressed texture pack
        '''
        self.resultion = resultion
        self.raw_images_path = raw_images_path
        self.pack_name = pack_name
        self.buffer_path = buffer_path
        self.result_path = result_path
        self.buffer_path = 'pack/assets/minecraft/textures'
        self.types = types


    def clean_buffer_path(self):
        if(os.path.exists(self.buffer_path)):
            shutil.rmtree(self.buffer_path)
        
    
    def init_buffer_path(self):
        # make/clean the buffer path
        self.clean_buffer_path()
        os.makedirs(self.buffer_path)
        for type in self.types:
            os.mkdir(f'{self.buffer_path}/{type}')
    
    
    def img_process(self, type):
        # process images with givin type
        raw_images_floder = f'{self.raw_images_path}/{type}'
        buffer_floder = f'{self.buffer_path}/{type}'
        for file in os.listdir(raw_images_floder):
            input_img = cv.imread(f'{raw_images_floder}/{file}',cv.IMREAD_COLOR)
            img = cv.resize(input_img, (self.resultion, self.resultion))
            cv.imwrite(f'{buffer_floder}/{file}',img)
    
         
    def output_pack(self):
        # compress and move the texture to result path
        pass
    
    
    def process_all(self):
        # do everything
        self.init_buffer_path()
        for type in self.types:
            self.img_process(type)
        # WIP
        
