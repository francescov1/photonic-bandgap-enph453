import numpy as np
from apparatus_model import ApparatusModel
import fabry_perot as fb
import impurity as imp
import exp_data as ed

n_cells = 6 # number of normal unit cells
ed.plot_exp_data(n_cells)
# n_fb_cells = 2 # can be 2 or 4
# fb.plot_fb(n_fb_cells)
# imp_pos = -1 # can be between -1 and 6
# imp.plot_imp(imp_pos)

# 2, 4, 6 pure
# 6 - impurity at each spot - 93 ohm impurity of length 67.5cm
# 3 cells, impurity, 3 cells - impurity was 2 and 4 50 ohm cables of length 176 cm

start_f = 50e6 # MHz
stop_f = 850e6 # MHz
n_points = 1000

apparatus = ApparatusModel(n_cells, start_f, stop_f, n_points)

# - to add impurity, uncomment the lines below and sepcify params
# - impurity is always added to the end of the cell at specified position,
#   expect for @ position -1, where its added at the very front
# - can be one of two types:
#     - "fp":
#         - impedance: 50ohm
#         - position: set to middle of cells automatically
#         - number of cables: specify one of following: 2,4
#     - "impure" (93ohm impurity, set @ position )
#         - impedance: 93ohm
#         - position: specify one of following: -1,0,1,2,3,4,5
#         - number of cables: set to 1 automatically

'''
impurity_type = "fp"
impurity_position = 2
impurity_cable_length = 2
apparatus.add_impurity(
    type=impurity_type,
    cell_position=impurity_position,
    n_cables=impurity_cable_length
)
'''

apparatus.calculate_response()

# pass show_band_gaps=True to have band gaps marked on plot
apparatus.plot_response(show_band_gaps=True)
