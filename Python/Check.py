import pickle as pkl
import matplotlib.pyplot as plt
from DetectEventsClass import DetectEventsClass

w = 50

with open("events_indexes.pkl","rb") as f:
    ev = pkl.load(f)
    f.close()


for j in range(len(ev["filenames"])):
    f = ev["filenames"][j]
    s = ev["sensorsdata"][j]
    l = ev["loadcelldata"][j]
    i = ev["indexes"][j]
    DetectEventsClass(window=w, x=s, loadcell=l, verbose=1)

