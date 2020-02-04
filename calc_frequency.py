import numpy as np
import lengths
import matplotlib.pyplot as plt



l_50 = lengths.cells['l_50']
l_75 = lengths.cells['l_75']
l_tip = lengths.cells['l_tip']
l_conn = lengths.cells['l_conn']


def get_bandgap_freq():

    v = (2*10**8) # 2/3 times the speed of light

    L_mean = l_50+l_75+l_tip*2+l_conn*2
    L_std = 0.1

    n = 100000

    L = np.random.normal(L_mean,L_std,n)
    f_exact = v/(2*L_mean)
    f = v/(2*L)
    err = np.std(f)

    return f_exact, err

