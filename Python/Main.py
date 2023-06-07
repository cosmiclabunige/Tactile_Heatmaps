import os
import pickle as pkl
from glob import glob
from DetectEventsClass import *

w = 50 # the window length for computing the windowed variance
path = './sensors/'
pathloadcell = './loadcell'

glob_files = glob(path+'*/*') # list all the files

events_dic = {"filenames":[], "sensorsdata":[], "loadcelldata":[],  "indexes":[]} # create a dictionary to save results
for f in glob_files:
    if "Sp150" in f: # skip the lowest velocity
        continue
    x_tmp = np.load(f) # load the datum
    N = len(x_tmp[:,0]) # compute the number of samples
    loadcell = np.load(pathloadcell + f.split('./sensors')[-1])
    loadcell = np.asarray(loadcell)
    loadcell = loadcell[int(2*N/10):int(8*N/10)]
    #### Extract only the central part of the signals taking from the 40% to 60%
    x = []
    for i in range(8):
        x.append(x_tmp[int(2*N/10):int(8*N/10),i])
    x = np.asarray(x).T
    title = f.split('\\')[-1]
    D = DetectEventsClass(window=w, x=x, loadcell=loadcell, title=title, verbose=0) # create the class object that computes the events
    shouldSave = D.get_save()
    if shouldSave: # save only if the procedure was able to find two events
        event_indexes = D.get_indexes()
        events_dic["filenames"].append(f)
        events_dic["sensorsdata"].append(x)
        events_dic["loadcelldata"].append(loadcell)
        events_dic["indexes"].append(event_indexes)
    
#### Save the dictionary in a pickle file
with open("events_indexes.pkl","wb") as f:
    pkl.dump(events_dic, f)
    f.close()

print("END")