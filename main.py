import numpy as np
import matplotlib.pyplot as plt
from lengths import cells as cell_lengths, impurities as impurity_lengths
from cell_model import CellModel

def get_total_M(cells):
    M_total = None
    for cell in cells:
        if (M_total is None):
            M_total = cell.M_cell
        else:
            M_total = np.matmul(M_total, cell.M_cell)

    return M_total

# get frequency response of total reflection
def get_frequency_response(M_cell):
    #R = (abs(M_cell[1, 0])**2) / (abs(M_cell[0, 0])**2)
    T = 1/abs(M_cell[0, 0])**2
    return T

# 2 cells
cell_lengths = cell_lengths[:2]

start_f = 50e6 # MHz
stop_f = 850e6 # MHz
num_points = 100
frequencies = np.linspace(start=start_f, stop=stop_f, num=num_points)

transmission = []
for f_rf in frequencies:
    # This is for different length cells
    '''
    cells = []
    for cell_length in cell_lengths:
        cell = CellModel(cell_length['l_75'], cell_length['l_50'])

        #band_gap_f = cell.get_band_gap_frequency()
        #print("Band gap frequency: " + str(band_gap_f/1000000) + "MHz")
        cell.set_transfer_mats()
        cell.set_phase_mats(f_rf)
        cell.set_matrix_model()
        cells.append(cell)

    M_total = get_total_M(cells)
    '''

    # just take first cell length
    cell = CellModel(cell_lengths[0]['l_75'], cell_lengths[0]['l_50'])
    cell.set_transfer_mats()
    cell.set_phase_mats(f_rf)
    cell.set_matrix_model()

    # 2 cells
    M_total = np.linalg.matrix_power(cell.M_cell, 2)

    T = get_frequency_response(M_total)
    transmission.append(T)

plt.plot(frequencies, transmission)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Response")
plt.show()
