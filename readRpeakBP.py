import numpy as np
from matplotlib import pyplot as plt

# Data Import
path_folder = 'C:/Users/SNUBH/Desktop/20230717_SNUBH/'
file_name = '10012055_220715_010955.npy'
Data = np.load(path_folder + file_name)
Wave = Data[0:3,:]
BP = Data[3,:]

# Decode for BP & Rpeak
idx_Rpeak = np.array(np.where(BP > 500)[0])
BP[idx_Rpeak] = BP[idx_Rpeak] - 1000
BP[0] = 0 # ... Can't distinguish MAP & SBP at first
idx_DBP = np.array(np.where(BP < 0)[0])
idx_MAP = idx_DBP + 1
if idx_MAP[-1] > len(BP): idx_MAP = np.delete(idx_MAP,-1) # Check OutOfBound
idx_SBP = np.setdiff1d(np.array(np.where(BP > 0)[0]), idx_MAP)
DBP, MAP, SBP = -BP[idx_DBP], BP[idx_MAP], BP[idx_SBP]

# Display
fig, axs = plt.subplots(nrows=3, ncols=1,figsize=(9,9))
fig.suptitle(file_name)
axs[0].plot(Wave[0,:])
axs[0].plot(idx_Rpeak,Wave[0,idx_Rpeak],'rv')
axs[0].set_title('ECG')
axs[1].plot(Wave[1,:])
axs[1].set_title('PPG')
axs[2].plot(Wave[2,:])
axs[2].plot(idx_SBP,SBP,'rv')
axs[2].plot(idx_DBP,DBP,'g^')
axs[2].plot(idx_MAP,MAP,'p-')
axs[2].set_title('ABP')
fig.show()

for ax in axs:
    ax.set_xlim([1000,6000])
