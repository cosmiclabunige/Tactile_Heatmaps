import os
import shutil
from glob import glob
import pandas as pd
import numpy as np

loadcellpath = './loadcell'
sensorspath = './sensors'
allfiles = glob('./dataset/*/*/*')


def check_folder_path(fo):
    if not os.path.exists(fo):
        os.makedirs(fo)

def read_data(f):
    with open(f) as file:
        a = file.readlines()
        file.close()
    del a[0]
    strlist = [l.split('\t') for l in a]
    x = []
    for str in strlist:
        if len(strlist) == 1:
            x.extend([float(s) for s in str])
        else:
            x.append([float(s) for s in str])
    return np.asarray(x)


for f in allfiles:
    if 'Force' in f:
        path2save = loadcellpath
    else:
        path2save = sensorspath
        
    f_split = f.split('_')
    whichobj = f_split[-2]
    whichvel = f_split[-3]
    whichseq = f_split[-4]
    whichtrial = f_split[-1].split('.')[0]
    f2save = whichobj + '_' + whichseq + '_' + whichvel + '_' + whichtrial + '.npy'
    path2save = os.path.join(path2save, whichobj)
    check_folder_path(path2save)
    x = read_data(f)
    np.save(os.path.join(path2save,f2save), x)
print('END')