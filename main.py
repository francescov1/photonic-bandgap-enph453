import numpy as np

############# Values #############

# NOTE: '1' denotes the 75 ohm wire, '2' denotes the 50 ohm wire

c = 3.0 * (10**8) # speed of light
eps = np.finfo(float).eps # epsilon

num_cells = 2 # number of cells (combination of two wires)

# TODO: measure
l_1 = 1 # length of 75 ohm wire
# TODO: measure
l_2 = 1 # length of 50 ohm wire

# Z_n = electrical impedance for n wire => replaces index of refraction n
Z_1 = 75
Z_2 = 50

# phase_vel in wires
v = v_1 = v_2 = 0.66 * c

f_rf = 100 # MHz
f_rf *= 1000000 # convert to Hz

f_0 = v / (2 * (l_1 + l_2))
print("Band gap frequency: " + str(f_0/1000000) + "MHz")

# get frequency response of total reflection
def get_frequency_response(M_cell):
    R = (abs(M_cell[1, 0])**2) / (abs(M_cell[0, 0])**2)
    return R

def get_transfer_mat(Z_a, Z_b):
    r_ab = (Z_a - Z_b)/(Z_a + Z_b)
    t_ab = (2 * Z_a)/(Z_a + Z_b)

    # transfer matrix
    # magnitudes at interface: [[a_2], [b_2]] = T_12 * [[a_1], [b_1]]

    T_ab = np.multiply(1/t_ab, np.array([[1, r_ab], [r_ab, 1]]))
    return T_ab

def get_phase_mat(f_rf, l, v):
    phi = (2 * np.pi * f_rf * l) / v

    # P_i = [[e^(i*phi), 0], [0, e^(i*phi)]] - i in equation is complex i, not i in P_i
    P = np.array([[eps**complex(0, phi), 0], [0, eps**complex(0, phi)]])
    return P

# for a specific f - we will need to generalize this
# f_rf = frequency of rf signal
def get_matrix_model(T_ab, T_ba, P_a, P_b):
    # model unit cell of coaxial cable by multiply transfer and propagation matrices
    # M_cell = T_21 * P_2 * T_12 * P_1
    M_cell = np.matmul(T_ba, P_b)
    M_cell = np.matmul(M_cell, T_ab)
    M_cell = np.matmul(M_cell, P_a)

    return M_cell;

T_12 = get_transfer_mat(Z_1, Z_2)
T_21 = get_transfer_mat(Z_2, Z_1)
P_1 = get_phase_mat(f_rf, l_1, v_1)
P_2 = get_phase_mat(f_rf, l_2, v_2)

M_cell = get_matrix_model(T_12, T_21, P_1, P_2)

#print("\n")
#print(M_cell)
R = get_frequency_response(M_cell)

print("frequency response: " + str(R))
print("transmission: " + str(1-R))
