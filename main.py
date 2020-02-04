import numpy as np
from apparatus_model import ApparatusModel
import fabry_perot as fb
import impurity as imp
import exp_data as ed

# - to add impurity, uncomment the lines below and sepcify params
# - impurity is always added to the end of the cell at specified position,
#   expect for @ position -1, where its added at the very front
# - can be "fp" (50ohm impurity - position gets set to middle of cells automatically) or
#   "impure" (93ohm impurity, set @ position -1,0,1,2,3,4,5)

#for all configurations
n_cells = 6
start_f = 50e6 # MHz
stop_f = 850e6 # MHz
n_points = 1000


apparatus = ApparatusModel(n_cells, start_f, stop_f, n_points)

#for pure configurations
# ed.plot_exp_data(n_cells)

#for impure option
# impurity_position = 3
# impurity_type = "impure"
# impurity_cable_length = 2
# imp.plot_imp(impurity_position)
# apparatus.add_impurity(type=impurity_type, cell_position=impurity_position,n_cables=impurity_cable_length)

#for fp
# n_fb_cells = 2 # can be 2 or 4
# impurity_position = 0
# impurity_cable_length = 2
# impurity_type = "fp"
# fb.plot_fb(n_fb_cells)
# apparatus.add_impurity(type=impurity_type, cell_position=impurity_position,n_cables=impurity_cable_length)

apparatus.calculate_response()

# pass show_band_gaps=True to have band gaps marked on plot
apparatus.plot_response(show_band_gaps=True)
