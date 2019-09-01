# This routine is only a proof of concept. It's intended for testing new ideas
import pandas as pd

from data_abstractions.NozzlesData import NozzlesData
from data_exploring.ErroneousTransactionGenerator import ErroneousTransactionGenerator
from data_exploring.TransactionsExtractor import TransactionsExtractor
from data_abstractions.Tanks import Tanks


def find_nearest_tank_entry_index(tranaction_timestamp, tank):
    """
    Get the index of row in tank DataFrame which timestamp is 
    closest to `tranaction_timestamp`. 
    """
    return abs(tank["timestamp"] - transaction_timestamp).idxmin()


tanks = Tanks()
# select a tank on which we want to operate
tank = tanks.get_tank_by_id(1)
# reset index !
tank.reset_index(inplace=True)

nozzles = NozzlesData()
# get nozzles associated with selected tank
selected_nozzles = [
    TransactionsExtractor(nozzles.get_nozzle(nozzle_id)).extract_to_column()
    for nozzle_id in [13, 17, 21]
]
# concat and sort by timestamp
selected_nozzles = pd.concat(selected_nozzles)
selected_nozzles.sort_values(by="timestamp", inplace=True)

print(selected_nozzles)

for nozzle_transaction in selected_nozzles.iterrows():

    transaction_timestamp = nozzle_transaction[1]["timestamp"]
    single_transaction = nozzle_transaction[1]["singleTransaction"]
    nozzleID = nozzle_transaction[1]["nozzleID"]

    min_time_diff_index = find_nearest_tank_entry_index(transaction_timestamp, tank)
    nearest_tank_entry = tank.iloc[min_time_diff_index]

    tank_t0 = None
    tank_t1 = None
    if transaction_timestamp > nearest_tank_entry["timestamp"]:
        tank_t0 = nearest_tank_entry
        tank_t1 = tank.iloc[min_time_diff_index + 1]  # this could be problematic
    else:
        tank_t0 = tank.iloc[
            min_time_diff_index - 1
        ]  # this could be problematic as well :/
        tank_t1 = nearest_tank_entry

    diff = tank_t1["fuelVolume"] - (tank_t0["fuelVolume"] - single_transaction)

    print(
        "diff: {}, transaction={}, transaction_time={}, nozzleID={} t0={}, t1={}".format(
            diff,
            single_transaction,
            transaction_timestamp,
            nozzleID,
            str(tank_t0),
            str(tank_t1),
        )
    )
