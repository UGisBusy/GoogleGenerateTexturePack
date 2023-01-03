import numpy as np
import os
import shutil
import cv2 as cv
import zipfile

class Processor:
    def __init__(self, resolution=128, types=['block'], pack_name='hell', raw_images_path='raw_images' ,buffer_path='buffer', result_path='result'):
        '''
        resolution:          the resolution of the image
        types:              types we want to be included in the pack
        raw_images_path:    the path of the raw images crawled
        buffer_path:        the path of the processed images
        result_path:        the path of the compressed texture pack
        '''
        self.resolution = resolution
        self.names_path = 'names'
        self.raw_images_path = raw_images_path
        self.pack_name = pack_name
        self.buffer_path = buffer_path
        self.result_path = result_path
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
            try:
                img = cv.resize(input_img, (self.resolution, self.resolution))
            except:
                print(f'{raw_images_floder}/{file} broken, skip process it')
            cv.imwrite(f'{buffer_floder}/{file}',img)
    
         
    def output_pack(self):
        # compress and move the texture to result path
        with zipfile.ZipFile(f'{self.result_path}/{self.pack_name}.zip', 'w') as zf:
            for type in self.types:
                buffer_floder = f'{self.buffer_path}/{type}'
                for file in os.listdir(buffer_floder):
                    if(type=='nature_block'):
                        zf.write(f'{buffer_floder}/{file}', f'assets/minecraft/textures/block/{file}')
                    else:
                        zf.write(f'{buffer_floder}/{file}', f'assets/minecraft/textures/{type}/{file}')
                if(type in ('block')):
                    mcmeta_floder = f'{self.names_path}/{type}_mcmeta'
                    for file in os.listdir(mcmeta_floder):
                        zf.write(f'{mcmeta_floder}/{file}', f'assets/minecraft/textures/{type}/{file}')
            zf.write(f'{self.names_path}/pack.mcmeta', 'pack.mcmeta')
        

    def process_all(self):
        # do everything
        self.init_buffer_path()
        for type in self.types:
            self.img_process(type)
        self.output_pack()
