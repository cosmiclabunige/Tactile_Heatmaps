import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def _print(x, ind=None, title=None, th=None):
    fig, axs = plt.subplots(4,2)
    j = 0
    k = 0
    for i in range(8):
        if ind is not None: 
            y = [x[n,i] for n in ind]
            axs[k, j].scatter(ind, y, s=30, c='r', marker='X')
        axs[k, j].plot(x[:,i])
        if th is not None:
            axs[k,j].axhline(y = th[i], color = 'r', linestyle = '-')
        if i==3:
            k = 0
            j = 1
        else:
            k=k+1
    if title is not None:
        fig.suptitle(title)
    

def _printloadcell(x, title): 
    plt.figure()
    plt.plot(x)
    if title is not None:
        plt.title(title)


class DetectEventsClass():
    def __init__(self, window, x, loadcell=None, title=None, verbose=False):
        self.__w = window
        self.__loadcell = loadcell
        self.__x = x
        self.__save = False
        self.__verbose = verbose
        self.__title = title
        self.__ind = self.__extract_events()
        
    def __extract_events(self):
        x = self.__x
        w = self.__w
        t = self.__title
        N = len(x[:,0])

        #### Normalize signals to have 0 median in each channel
        med = np.median(x, axis=0)
        x_norm = x - med
        
        #### Compute the cumulative sum
        cum_sum = np.cumsum(np.abs(x_norm), axis=0)
        

        #### Compute the variance on the windowed cumulative sum
        var = []
        i = 0
        while i < len(cum_sum[:,0])-w+1:
            mv = np.var(cum_sum[i:i+w,:], axis=0)
            var.append(mv) 
            i += int(w/2)
        # for i in range(0, N-w, w):
        #     var.append(np.var(cum_sum[i:i+w,:], axis=0))
        var = np.asarray(var)
        ma = np.max(var, axis=0) # find the maximum variance peak along all the channel
        th = 0.3*ma # compute the threshold to detect the events

        #### Find the indexes for all the sensors where the variance exceeds the threshold
        ind= []
        for i in range(8):
            if not (i == 0 or i==1 or i==3):
                continue
            ind.extend(np.where(var[:,i]>th[i])[0])
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
        while(len(indexes)<3): # loop until the procedure does not find three events
            #### Extract the indexes of the variances based on the greates frequencies
            
            for i in ind_freq:
                tmp = ind[i]
                di = []
                dist = 10
                if indexes:
                    di = [abs(j-tmp) for j in indexes]
                    if np.all(np.asarray(di)>dist):
                        indexes.append(tmp)
                    # else:
                    #     i_tmp = np.where(np.asarray(di)<=dist)[0]
                    #     for ii in i_tmp:
                    #         if np.all(var[tmp] > var[indexes[ii]]):
                    #             indexes[ii] = ind[ii]
                else:
                    indexes.append(tmp)
            indexes.sort()
            
            #### Find the indexes for the subsequent highest frequency 
            iii -= 1
            try:
                ind_freq = np.where(np.asarray(freq)==new_freq[iii])[0]
            except:
                break
        #### The trial should be saved only if the procedure has found three events
        if len(indexes)>=2:
            self.__save = True
        else:
            self.__save = False
        ii = [i*int(w/2) for i in indexes]
        if self.__verbose:
            # ii = [i*self.__w for i in indexes]
            _print(x_norm, ii, t)
        if self.__verbose:
            # ii = [i*self.__w for i in indexes]
            _print(cum_sum, ii, t)
        if self.__verbose:
            _print(var, indexes, t, th=th)
        if self.__verbose and self.__loadcell is not None:
            # ii = [i*self.__w for i in indexes]
            _printloadcell(self.__loadcell, t)
        if self.__verbose:
            
            plt.show()
        return indexes
        
    def get_indexes(self):
        return self.__ind
    
    def get_save(self):
        return self.__save
    


    