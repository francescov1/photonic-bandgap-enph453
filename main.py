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
    # this is what the textbook says
    #R = (abs(M_cell[1, 0])**2) / (abs(M_cell[0, 0])**2)

    # this looks a bit more accurate tho
    R = (abs(M_cell[0, 1])**2) / (abs(M_cell[1, 0])**2)
    return R

cell_lengths = cell_lengths[:2]

start_f = 50 # MHz
stop_f = 850 # MHz
num_points = 100
frequencies = np.linspace(start=start_f*1000000, stop=stop_f*1000000, num=num_points)

f_responses = []
transmission = []
for f_rf in frequencies:
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

    R = get_frequency_response(M_total)
    f_responses.append(R)
    transmission.append(1-R)

#print(f_responses)
plt.plot(frequencies, f_responses)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Response")
plt.show()

# for multiple cells
#M_cell = np.linalg.matrix_power(M_cell, num_cells)
