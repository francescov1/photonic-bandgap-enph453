import numpy as np
from apparatus_model import ApparatusModel

# TODO: handle impurity at first position

n_cells = 2
# 2, 4, 6 pure
# 6 - impurity at each spot - 93 ohm impurity of length 67.5cm
# 3 cells, impurity, 3 cells - impurity was 2 and 4 50 ohm cables of length 176 cm

start_f = 50e6 # MHz
stop_f = 850e6 # MHz
n_points = 1000

apparatus = ApparatusModel(n_cells, start_f, stop_f, n_points)

# to add impurity, uncomment the lines below and sepcify params
#impurity_type = "bragg" # can be "bragg" or "fp"
#impurity_position = 1
#apparatus.add_impurity(impurity_position, impurity_type)

apparatus.calculate_response()
apparatus.plot_response()
