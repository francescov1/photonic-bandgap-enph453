import numpy as np
from lengths import cells as cell_lengths
import matplotlib.pyplot as plt
from cell_model import CellModel

l_50 = cell_lengths['l_50']
l_75 = cell_lengths['l_75']
l_tip = cell_lengths['l_tip']

# get frequency response
def get_frequency_response(M_cell):
    R = (abs(M_cell[1, 0])**2) / (abs(M_cell[0, 0])**2)
    T = 1/abs(M_cell[0, 0])**2
    return R, T

class ApparatusModel:

    def __init__(self, n_cells, start_f, stop_f, n_points):
        self.frequencies = np.linspace(start=start_f, stop=stop_f, num=n_points)
        self.n_cells = n_cells

    def add_impurity(self, cell_position, type):
        self.impurity_position = cell_position
        self.impurity_type = type

    def calculate_response(self):
        transmission = []
        reflection = []
        for f_rf in self.frequencies:
            cell = CellModel(l_75+l_tip, l_50+l_tip, f_rf)
            cell.set_transfer_mats()
            cell.set_phase_mats()

            M_total = None
            # pure apparatus - no impurities
            if not hasattr(self, 'impurity_position'):
                M_cell = cell.get_matrix_model()
                M_total = np.linalg.matrix_power(M_cell, self.n_cells)
            # apparatus has an impurity
            else:
                for i in range(self.n_cells):
                    if i == self.impurity_position:
                        M_cell = cell.get_matrix_model(
                            impurity=self.impurity_type,
                            isFirstPosition=self.impurity_position == 0
                        )
                    else:
                        M_cell = cell.get_matrix_model()

                    if M_total is None:
                        M_total = M_cell
                    else:
                        M_total = M_total @ M_cell

            R, T = get_frequency_response(M_total)
            transmission.append(T)
            reflection.append(R)

        self.transmission = transmission
        self.reflection = reflection

    def plot_response(self):
        plt.plot(self.frequencies, self.transmission)
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Transmission")
        plt.show()
