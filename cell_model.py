import numpy as np

class CellModel:

    def __init__(self, l_75, l_50):
        self.l_1 = l_75
        self.l_2 = l_50
        self.Z_1 = 75
        self.Z_2 = 50
        self.v = 0.66 * 3.0e8 # 2/3 * speed of light

    def get_band_gap_frequency(self):
        return self.v / (2 * (self.l_1 + self.l_2))

    def set_transfer_mats(self):

        def calc_transfer_mat(Z_a, Z_b):
            r_ab = (Z_a - Z_b)/(Z_a + Z_b)
            t_ab = (2 * Z_a)/(Z_a + Z_b)
            # transfer matrix
            # magnitudes at interface: [[a_2], [b_2]] = T_12 * [[a_1], [b_1]]
            T_ab = np.multiply(1/t_ab, np.array([[1, r_ab], [r_ab, 1]]))
            return T_ab

        self.T_12 = calc_transfer_mat(self.Z_1, self.Z_2)
        self.T_21 = calc_transfer_mat(self.Z_2, self.Z_1)

    def set_phase_mats(self, f_rf):

        eps = np.finfo(float).eps # epsilon

        def calc_phase_mat(f, l, v):
            phi = (2 * np.pi * f * l) / v

            # P_i = [[e^(i*phi), 0], [0, e^(i*phi)]] - i in equation is complex i, not i in P_i
            P = np.array([[eps**complex(0, phi), 0], [0, eps**complex(0, -phi)]])
            return P

        self.P_1 = calc_phase_mat(f_rf, self.l_1, self.v)
        self.P_2 = calc_phase_mat(f_rf, self.l_2, self.v)

    def set_matrix_model(self):
        # equation in lab description
        #M_cell = self.T_21 @ self.P_2 @ self.T_12 @ self.P_1

        # Waleeds order of operations
        M_cell = self.P_2 @ self.T_12 @ self.P_1 @ self.T_21

        self.M_cell = M_cell
