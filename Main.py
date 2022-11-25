import zipfile

from Processor import Processor


loc = "input_test\\"
filename = "stone.jpg"

p = Processor(64)
p.process(filename, loc)