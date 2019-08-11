# This routine is only a proof of concept. It's intended for testing new ideas 

# Select a tank 
# Get nozzles which are connected to the seleted tank
# 
# For each entry in tank data (logged every 5 minutes) -> t0, t1
#   Check the amount of fuel between t0 and t1 both in:
#       1. Refueling
#       2. Nozzles 
#   Check balance
# --------------------------------------------------------------

import pandas as pd

from data_abstractions.NozzlesData import NozzlesData
from data_abstractions.Tanks import Tanks
from data_abstractions.TankRefuel import TankRefuel
from data_exploring.TransactionsExtractor import TransactionsExtractor


tanks = Tanks()
# select a tank on which we want to operate
tank = tanks.get_tank_by_id(1)

nozzles = NozzlesData()
# get nozzles associated with selected tank
selected_nozzles = [TransactionsExtractor(nozzles.get_nozzle(nozzle_id)).extract_to_column() for nozzle_id in [13, 17, 21]]
# concat and sort by timestamp
selected_nozzles = pd.concat(selected_nozzles)
selected_nozzles.sort_values(by="timestamp", inplace=True)
selected_nozzles.reset_index(inplace=True)

print(selected_nozzles)

# Go through tanks table - get t0, t1: 
# TankRefuel.get_refueling_delta(t0, t1)
# Get 