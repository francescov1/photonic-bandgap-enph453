import numpy as np
import matplotlib.pyplot as plt



plot_x=[]
plot_y=[]


plt.figure(1)
nums = [4,8]
labels = []
folder = './Data/200-380mhz'

for i in nums:
    calibration = np.loadtxt(folder+'/calibration_original.txt')
    f_calibration = np.loadtxt(folder+'/f-calibration_original.txt')
    data = np.loadtxt(folder+'/6cells-FB-{}_50Ohm.txt'.format(i))

    #find best fit line of voltage calibration curve
    poly_calib = np.polyfit(calibration[:,0],calibration[:,1],1)
    poly_f = np.polyfit(calibration[:,0],f_calibration,1)
    new_baseline = poly_calib[0]*data[:,0]+poly_calib[1]
    freq_data = poly_f[0]*data[:,0]+poly_f[1]
    data_corrected = data[:,1]/new_baseline
    # plot_y = normalize(plot_y)
    plt.plot(freq_data,data_corrected)
    plt.legend()
    labels.append('Impurity Number {}'.format(i))

def normalize(arr):
    #normalize 1-d array
    arr = (arr-np.min(arr))/(np.max(arr)-np.min(arr))
    return arr

plt.legend(labels)
plt.xlabel('Frequency [MHz]')
plt.ylabel('Amplitude')
plt.show()