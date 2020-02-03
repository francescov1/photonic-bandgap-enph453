import numpy as np
import matplotlib.pyplot as plt

# folder_list = ['200-380mhz']
# num_impurities = [2,4]



folder = './Data/200-380mhz'
combined_x=[]
combined_y=[]
labels = []

def normalize(arr):
    #normalize 1-d array
    arr = (arr-np.min(arr))/(np.max(arr)-np.min(arr))
    return arr

def plot_fb(n):
    assert(n==2 or n==4), "Valid values for n are 2 and 4"

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
    freq_data *= 1000000

    plt.plot(freq_data,1-normalize(data_calibrated))
    # plt.legend()
    # labels.append('Number of Impurities {}'.format(n))


# combined_y = normalize(combined_y)
# plt.legend(labels,bbox_to_anchor=(1.04,1), loc="upper left")
# plt.xlabel('Frequency [MHz]')
# plt.ylabel('Amplitude')
# plt.show()