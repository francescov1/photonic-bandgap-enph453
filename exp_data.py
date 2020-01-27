import numpy as np
import matplotlib.pyplot as plt

folder_list = ['50-100mhz','100-200mhz','200-380mhz']
data_of_interest = '6cells-pure.txt'
plot_x=[]
plot_y=[]
for name in folder_list:
    folder = './Data/'+name
    calibration = np.loadtxt(folder+'/calibration.txt')
    f_calibration = np.loadtxt(folder+'/f-calibration.txt')
    data = np.loadtxt(folder+data_of_interest)

     #find best fit line of voltage calibration curve
    num_steps_calibration = 11
    num_steps_run = 101
    minV = 0
    maxV = 15
    x = np.linspace(minV,maxV,num_steps_calibration)
    poly_calib = np.polyfit(x,calibration[:,1],1)
    poly_f = np.polyfit(x,f_calibration,1)



    new_baseline = poly_calib[0]*data[:,0]+poly_calib[1]
    freq_data = poly_f[0]*data[:,0]+poly_f[1]
    plot_x = np.concatenate([plot_x,freq_data])
    plot_y = np.concatenate([plot_y,data[:,1]-new_baseline])
    # plt.plot(data[:,0],data[:,1]-new_baseline)
    # plt.plot(data[:,0],data[:,1],'r')
    # plt.plot(data[:,0],data[:,1])

plt.plot(plot_x,plot_y)
plt.show()

# folder = '/Users/MyComputer/Desktop/Lab1Data/100-200mhz'
# calibration = np.loadtxt(folder+'/calibration-new.txt')
# f_calibration = np.loadtxt(folder+'/f-calibration.txt')
# data = np.loadtxt(folder+'/4cells-pure.txt')

# #find best fit line of voltage calibration curve
# num_steps_calibration = 11
# num_steps_run = 101
# minV = 0
# maxV = 15
# x = np.linspace(minV,maxV,num_steps_calibration)
# poly_calib = np.polyfit(x,calibration[:,1],1)
# poly_f = np.polyfit(x,f_calibration,1)



# new_baseline = poly_calib[0]*data[:,0]+poly_calib[1]
# freq_data = poly_f[0]*data[:,0]+poly_f[1]
# plt.plot(data[:,0],data[:,1]-new_baseline)
# plt.plot(data[:,0],data[:,1],'r')
# plt.show()
# plt.plot(data[:,0],data[:,1])

# plt.show()