import numpy as np
import matplotlib.pyplot as plt

folder_list = ['50-100mhz','100-200mhz','200-380mhz','400-850mhz']
# folder_list = ['100-200mhz']
combined_x=[]
combined_y=[]

def normalize(arr):
    #normalize 1-d array
    arr = (arr-np.min(arr))/(np.max(arr)-np.min(arr))
    return arr

def plot_exp_data(n_cells):
    #n cells can be 2, 4 or 6
    data_of_interest = '/{}cells.txt'.format(n_cells)

    for name in folder_list:
        folder = './Data/'+name

        #load calibration data
        calibration = np.loadtxt(folder+'/calibration.txt')


        #load frequency calibration data
        f_calibration = np.loadtxt(folder+'/f-calibration.txt')

        #load amplitude data
        data = np.loadtxt(folder+data_of_interest)
        data_calibrated = data[:,1]/calibration[:,1]

        #find fit line for frequency data
        poly_f = np.polyfit(f_calibration[:,0],f_calibration[:,2],1)
        freq_data = poly_f[0]*data[:,0]+poly_f[1] #converts voltage to frequency
        count=0

        #get rid of overlapping data
        if(len(combined_x)>0):
            while(combined_x[-1]>freq_data[0]):
                freq_data = np.delete(freq_data,0)
                data_calibrated = np.delete(data_calibrated,0)

        #combine data sets
        combined_x = np.concatenate([combined_x,freq_data])
        combined_y = np.concatenate([combined_y,data_calibrated])

    combined_y = normalize(combined_y)
    combined_x *=1000000
    plt.plot(combined_x,1-combined_y)
# plt.xlabel('Frequency [MHz]')
# plt.ylabel('Transmittance')
# plt.show()