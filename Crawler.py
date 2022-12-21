import shutil
import os

class Crawler:

    def __init__(self, types=['block'], source='google', raw_images_path='raw_images'):
        '''
        types:              types of things to be crawled
        source:             which website to crawl
        raw_images_path:    the floder where images crawled to be putted in
        '''
        self.types = types
        self.source = source
        self.raw_images_path = raw_images_path
        self.names_path = 'names'
        self.keyword_dict = dict()


    def init_raw_images_path(self):
        # clean/make raw_floder_path
        self.clean_raw_images_path()
        os.mkdir(self.raw_images_path)
        for type in self.types:
            os.mkdir(f'{self.raw_images_path}/{type}')

    
    def clean_raw_images_path(self):
        # clean the raw images path
        if(os.path.exists(self.raw_images_path)):
            shutil.rmtree(f'{self.raw_images_path}')


    def build_keyword_dict(self):
        # make keyword dict
        for type in self.types:
            file = f'{self.names_path}/{type}_names.txt'
            self.keyword_dict[type] = []
            with open(file, 'r') as f:
                for line in f.readlines():
                    self.keyword_dict[type].append(line.strip().replace('_', ' ')[:-4])


    def crawl_images(self, type):
        # crawl images of certain type, need to be overloaded 
        print('NO DERIVED CLASS TO OVERLOAD THIS')
    

    def crawl_all(self):
        # crawl all types of images
        self.init_raw_images_path()
        self.build_keyword_dict()
        for type in self.types:
            self.crawl_images(type)
