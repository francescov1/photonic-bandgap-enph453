import numpy as np
import matplotlib.pyplot as plt

folder_list = ['200-380mhz']
num_impurities = [2,4]
combined_x=[]
combined_y=[]
labels = []

plt.figure(1)

for n in num_impurities:
    folder = './Data/200-380mhz'

    #load calibration data
    calibration = np.loadtxt(folder+'/calibration.txt')

    #load frequency calibration data
    f_calibration = np.loadtxt(folder+'/f-calibration.txt')

    #load amplitude data
    data = np.loadtxt(folder+'/6cells-FP-{}cells.txt'.format(n))
    data_calibrated = data[:,1]/calibration[:,1]

    #find fit line for frequency data
    poly_f = np.polyfit(f_calibration[:,0],f_calibration[:,2],1)
    freq_data = poly_f[0]*data[:,0]+poly_f[1] #converts voltage to frequency
    count=0

    plt.plot(freq_data,data_calibrated)
    plt.legend()
    labels.append('Number of Impurities {}'.format(n))

def normalize(arr):
    #normalize 1-d array
    arr = (arr-np.min(arr))/(np.max(arr)-np.min(arr))
    return arr

# combined_y = normalize(combined_y)
plt.legend(labels,bbox_to_anchor=(1.04,1), loc="upper left")
plt.xlabel('Frequency [MHz]')
plt.ylabel('Amplitude')
plt.show()