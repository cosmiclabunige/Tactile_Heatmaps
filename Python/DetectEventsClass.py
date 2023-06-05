import numpy as np
import matplotlib.pyplot as plt


def _print(x, ind=None):
    fig, axs = plt.subplots(4,2)
    j = 0
    k = 0
    for i in range(8):
        if ind is not None: 
            y = [x[n,i] for n in ind]
            axs[k, j].scatter(ind, y, s=30, c='r', marker='X')
        axs[k, j].plot(x[:,i])
        if i==3:
            k = 0
            j = 1
        else:
            k=k+1
    

class DetectEventsClass():
    def __init__(self, window, x, verbose=False):
        self.__w = window
        self.__x = x
        self.__save = False
        self.__verbose = verbose
        self.__ind = self.__extract_events()
        
    def __extract_events(self):
        x = self.__x
        w = self.__w
        N = len(x[:,0])

        #### Normalize signals to have 0 median in each channel
        med = np.median(x, axis=0)
        x_norm = x - med
        if self.__verbose:
            _print(x_norm)

        #### Compute the cumulative sum
        cum_sum = np.cumsum(np.abs(x_norm), axis=0)
        if self.__verbose:
            _print(cum_sum)

        #### Compute the variance on the windowed cumulative sum
        var = []
        for i in range(0, N-w, w):
            var.append(np.var(x[i:i+w,:], axis=0))
        var = np.asarray(var)
        ma = np.max(var) # find the maximum variance peak along all the channel
        th = 0.05*ma # compute the threshold to detect the events

        #### Find the indexes for all the sensors where the variance exceeds the threshold
        ind= []
        for i in range(8):
            ind.extend(np.where(var[:,i]>th)[0])
        ind.sort()

        #### Compute the frequencies of the indexes
        freq = []
        iii = -1
        for i in ind:
            freq.append(ind.count(i))
        new_freq = list(set(freq))
        new_freq.sort()
        # find the indexes where the frequencies are equal to the highest frequency (since iii=-1)
        ind_freq = np.where(np.asarray(freq)==new_freq[iii])[0] 

        indexes = []
        while(len(indexes)<2): # loop until the procedure does not find two events
            
            #### Extract the indexes of the variances based on the greates frequencies
            indexes = []
            for i in ind_freq:
                indexes.append(ind[i])
            indexes = np.unique(np.asarray(indexes))

            #### Remove indexes that are close meaning that they belong to the same event
            diff = np.diff(indexes)
            indexes_list = list(indexes)
            for i in range(len(diff)-1, -1, -1):
                if diff[i] <5: # the distance has been chosen as 5 points
                    del indexes_list[i+1]
            indexes = np.asarray(indexes_list)

            #### Find the indexes for the subsequent highest frequency 
            iii -= 1
            try:
                ind_freq = np.where(np.asarray(freq)==new_freq[iii])[0]
            except:
                break
        #### The trial should be saved only if the procedure has found two events
        if len(indexes)!=2:
            self.__save = False
        else:
            self.__save = True
        if self.__verbose:
            _print(var, indexes)
            plt.show()
        return indexes

    def get_indexes(self):
        return self.__ind
    
    def get_save(self):
        return self.__save
    


    