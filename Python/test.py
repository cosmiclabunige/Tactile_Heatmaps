import pickle as pkl
from glob import glob
import numpy as np
from DetectEventsClass import DetectEventsClass


with open("events_indexes.pkl","rb") as f:
    ev = pkl.load(f)
    f.close()

w = 20
ind = 29

x = ev["data"][ind]
DetectEventsClass(window=w, x=x, verbose =True)
print("END")