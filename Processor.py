import numpy as np
import cv2 as cv

class Processor:
    def __init__(self, size):
        self.SIZE = size

    def process(self, name, loc):
        '''
        :desc:
            Take a image in input_test floder and make a texturepack-format image floder.
        :para:
            name:  filename. eg. 'dirt.png'
            loc: location of the file. eg. "input_test\\"
        '''
        #cv.IMREAD_COLOR : BGR layer
        #cv.IMREAD_UNCHANGED : BGR layer + alpha
        input_img = cv.imread(f"{loc}{name}",cv.IMREAD_COLOR)
        img = cv.resize(input_img, (self.SIZE, self.SIZE))
        # cv.imshow(name, img)
        # cv.waitKey(0)
        cv.imwrite(f'output_test\\{name[:name.find(".")]}.png',img)