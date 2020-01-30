import numpy as np
import matplotlib.pyplot as plt
from lengths import cells as cell_lengths, impurities as impurity_lengths
from cell_model import CellModel

# get frequency response
def get_frequency_response(M_cell):
    R = (abs(M_cell[1, 0])**2) / (abs(M_cell[0, 0])**2)
    T = 1/abs(M_cell[0, 0])**2
    return R, T

l_50 = cell_lengths['l_50']
l_75 = cell_lengths['l_75']
l_tip = cell_lengths['l_tip']
n_cells = 2

start_f = 50e6 # MHz
stop_f = 850e6 # MHz
num_points = 1000
frequencies = np.linspace(start=start_f, stop=stop_f, num=num_points)

transmission = []
for f_rf in frequencies:
    # This is for different length cells

    # just take first cell length
    cell = CellModel(l_75+l_tip, l_50+l_tip)
    cell.set_transfer_mats()
    cell.set_phase_mats(f_rf)
    cell.set_matrix_model()

    # 2 cells
    M_total = np.linalg.matrix_power(cell.M_cell, n_cells)

    R, T = get_frequency_response(M_total)
    transmission.append(T)

plt.plot(frequencies, transmission)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Transmission")
plt.show()
