import numpy as np
import imageio
import matplotlib.pyplot as plt
from math import sqrt
from skimage import feature
import os, xlwt
from xlwt import Workbook
import useability, blob_functions

path = os.path.dirname(os.path.realpath('__file__')) + '/Blob Counter V3/'
pic_in = path + 'Picture Input/'
pic_out = path + 'Picture Output/'
files = os.listdir(pic_in)
files.sort()
config = useability.get_config()        
test_num = 1
print("Picture order:")
print(files)

if config['end_pic'] == 0.0:
    config['end_pic'] = len(files)

start_pic = int(config['start_pic']-1)
if start_pic <0:
    start_pic = 0
stop_pic = int(config['end_pic'])

if config['run_two'] == True:
    for plub in range(start_pic, stop_pic +1):
        print("\ntest " + str(test_num) + " start")
        blob_functions.run_two_detection(plub, files, pic_in, pic_out)
        print("test " + str(test_num) + " complete\n")
        test_num+=1

elif config['run_two'] == False:
    for plub in range(start_pic, stop_pic +1):
        print("\ntest " + str(test_num) + " start")
        blob_functions.run_one_detection(plub, files, pic_in, pic_out)
        print("test " + str(test_num) + " stop\n")
        test_num+=1

output_loc = path + "output.txt"
wb_loc = path + "Data.xls"

with open(output_loc, 'w') as filehandle:
        for listitem in blob_functions.counts:
            filehandle.write('%s\n' % listitem)

wb = blob_functions.wb
wb.save(wb_loc)
print("Analysis complete, press enter to exit")
input()