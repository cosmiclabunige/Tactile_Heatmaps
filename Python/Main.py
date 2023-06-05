import pickle as pkl
from glob import glob
import numpy as np
from DetectEventsClass import DetectEventsClass

w = 20 # the window length for computing the windowed variance
path = './sensors/'

glob_files = glob(path+'*/*') # list all the files

events_dic = {"file":[], "data":[], "indexes":[]} # create a dictionary to save results
for f in glob_files:
    if "Sp150" in f: # skip the lowest velocity
        continue
    x_tmp = np.load(f) # load the datum
    N = len(x[:,0]) # compute the number of samples
    #### Extract only the central part of the signals taking from the 40% to 60%
    x = []
    for i in range(8):
        x.append(x_tmp[int(4*N/10):int(6*N/10),i])
    x = np.asarray(x).T
    D = DetectEventsClass(window=w, x=x) # create the class object that computes the events
    shouldSave = D.get_save()
    if shouldSave: # save only if the procedure was able to find two events
        event_indexes = D.get_indexes()
        events_dic["file"].append(f)
        events_dic["data"].append(x)
        events_dic["indexes"].append(event_indexes)
    
#### Save the dictionary in a pickle file
with open("events_indexes.pkl","wb") as f:
    pkl.dump(events_dic, f)
    f.close()

print("END")