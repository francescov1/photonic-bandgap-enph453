import numpy as np
from lengths import impurities

def calc_phase_mat(f, l, v):
    phi = (2 * np.pi * f * l) / v

    # P_i = [[e^(i*phi), 0], [0, e^(i*phi)]] - i in equation is complex i, not i in P_i
    P = np.array([[np.exp(complex(0, phi)), 0], [0, np.exp(complex(0, -phi))]])
    return P

def calc_transfer_mat(Z_a, Z_b):
    r_ab = (Z_a - Z_b)/(Z_a + Z_b)
    t_ab = (2 * Z_a)/(Z_a + Z_b)
    # transfer matrix
    # magnitudes at interface: [[a_2], [b_2]] = T_12 * [[a_1], [b_1]]
    T_ab = np.multiply(1/t_ab, np.array([[1, r_ab], [r_ab, 1]]))
    return T_ab

class CellModel:

    def __init__(self, l_75, l_50, f_rf):
        self.l_1 = l_75
        self.l_2 = l_50
        self.l_conn = 0.05
        self.Z_conn = 50
        self.Z_1 = 75
        self.Z_2 = 50
        self.f_rf = f_rf
        self.v = 0.66 * 3.0e8 # 2/3 * speed of light

    def get_band_gap_frequency(self):
        return self.v / (2 * (self.l_1 + self.l_2))

    def set_transfer_mats(self):
        self.T_12 = calc_transfer_mat(self.Z_1, self.Z_conn)
        self.T_conn12 = calc_transfer_mat(self.Z_conn,self.Z_2)
        self.T_21 = calc_transfer_mat(self.Z_2, self.Z_conn)
        self.T_conn21 = calc_transfer_mat(self.Z_conn,self.Z_1)

    def set_phase_mats(self):
        self.P_1 = calc_phase_mat(self.f_rf, self.l_1, self.v)
        self.P_conn = calc_phase_mat(self.f_rf, self.l_conn, self.v)
        self.P_2 = calc_phase_mat(self.f_rf, self.l_2, self.v)

    # model impurities at the end of cell - but need to handle impurity is first position
    def get_matrix_model(self, impurity = None, isFirstPosition = False):
        # Waleeds order of operations - seems to give the same thing
        #M_cell = self.P_2 @ self.T_12 @ self.P_1 @ self.T_21

        M_cell = self.T_conn21 @ self.P_conn @ self.T_21 @ self.P_2 @ self.T_conn12 @ self.P_conn @ self.T_12 @ self.P_1

        if impurity is not None:
            impurity_info = impurities[impurity]

            # these calcs add the impurity on the end of the unit cell
            if isFirstPosition == False:
                Z_3 = impurity_info['impedance']
                l_3 = impurity_info['length']
                v_3 = impurity_info['phase_vel']

                T_23 = calc_transfer_mat(self.Z_2, Z_3)
                T_32 = calc_transfer_mat(Z_3, self.Z_2)
                P_3 = calc_phase_mat(self.f_rf, l_3, v_3)
                M_cell = T_32 @ P_3 @ T_23 @ M_cell
            # if the impurity is at the first position of the apparatus,
            # it needs to be added to the beginning of the cell instead
            else:
                Z_0 = impurity_info['impedance']
                l_0 = impurity_info['length']
                v_0 = impurity_info['phase_vel']

                T_01 = calc_transfer_mat(Z_0, self.Z_1)
                T_10 = calc_transfer_mat(self.Z_1, Z_0)
                P_0 = calc_phase_mat(self.f_rf, l_0, v_0)
                M_cell = M_cell @ T_01 @ P_0 @ T_10

        return M_cell
