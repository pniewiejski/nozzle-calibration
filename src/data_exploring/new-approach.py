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
import numpy as np

from data_abstractions.NozzlesData import NozzlesData
from data_abstractions.Tanks import Tanks
from data_abstractions.TankRefuel import TankRefuel

tanks = Tanks()
# select a tank on which we want to operate
tank = tanks.get_tank_by_id(1)

nozzles = NozzlesData()


def compute_nozzles_throughput(nozzles, t0, t1):
    NOZZLES_IDs = [13, 17, 21]
    # select subset of all nozzles between t0 and t1
    mask = (nozzles["timestamp"] >= t0) & (nozzles["timestamp"] <= t1)
    nozzles_subset = nozzles.loc[mask]

    # iterate over nozzles associated with a given tank
    # TODO: refactor it so it is not hardcoded :p

    nozzle_throughput = {i: 0 for i in NOZZLES_IDs}

    for nozzleID in NOZZLES_IDs:
        nozzle_throughput[nozzleID] = compute_throughput(nozzles_subset[nozzles_subset["nozzleID"] == nozzleID], t0, t1)
    print("Nozzle throughput {} between {} and {}".format(nozzle_throughput, t0, t1))
    return nozzle_throughput


# TODO: change this name
def compute_throughput(single_nozzle_subset, t0, t1):
    def has_finished_transactions(nozzle):
        """
        Check if nozzle dataframe contains finished transactions.
        This is done by checking if the value of the total counter has changed. 
        """
        return nozzle.drop_duplicates("totalCounter", keep="first").shape[0] > 1

    def has_ongoing_transactions(nozzle):
        """nozzle contains non-zero values in literCounter in the analysed time window"""
        return not nozzle[nozzle["literCounter"] > 0].empty

    def countains_transaction_start(nozzle):
        # problems possible here, pls fix when convenient.
        nozzle_status = nozzle["status"].tolist()
        print(nozzle_status)
        previous_status = nozzle_status[0]
        for status in nozzle_status[1:]:
            if previous_status > status:
                return True
            previous_status = status

    def get_liter_counter_at_timestamp(nozzle, timestamp):
        nozzle_at_timestamp = nozzle[nozzle["timestamp"] == timestamp]
        # print(nozzle, timestamp)
        # print(nozzle_at_timestamp)
        assert nozzle_at_timestamp.empty == False, "No iternet connection!"
        # print(nozzle_at_timestamp["literCounter"].values[0], type(nozzle_at_timestamp["literCounter"]))
        return nozzle_at_timestamp["literCounter"].values[0]

    nozzle_throughput_sum = 0

    if has_ongoing_transactions(single_nozzle_subset) or has_finished_transactions(single_nozzle_subset):
        MSG = "Should return non-zero value; "
        # things will happen here!

        # check if it contains beginning of transactions
        if countains_transaction_start(single_nozzle_subset):
            MSG += "Contains T start; "
            total_counter = single_nozzle_subset["totalCounter"].tolist()
            if get_liter_counter_at_timestamp(single_nozzle_subset, t1) == 0:
                MSG += "lC at t1 is 0; "
                nozzle_throughput_sum += (
                    max(total_counter) - min(total_counter) + get_liter_counter_at_timestamp(single_nozzle_subset, t0)
                )
            else:
                nozzle_throughput_sum += (
                    get_liter_counter_at_timestamp(single_nozzle_subset, t1)
                    + max(total_counter)
                    - min(total_counter)
                    - get_liter_counter_at_timestamp(single_nozzle_subset, t0)
                )
            # else:
            #     MSG += "lC at t1 is NOT 0; "
            #     nozzle_throughput_sum += get_liter_counter_at_timestamp(
            #         single_nozzle_subset, t1
            #     )

        else:
            MSG += "Does not contain T start; "
            if get_liter_counter_at_timestamp(single_nozzle_subset, t1) != 0:
                MSG += "lC at t1 is NOT 0; "
                nozzle_throughput_sum += get_liter_counter_at_timestamp(
                    single_nozzle_subset, t1
                ) - get_liter_counter_at_timestamp(single_nozzle_subset, t0)
            else:
                MSG += "lC at t1 is 0; "
                liter_counter = single_nozzle_subset["totalCounter"].tolist()
                nozzle_throughput_sum += (
                    max(liter_counter) - min(liter_counter) - get_liter_counter_at_timestamp(single_nozzle_subset, t0)
                )
        print(MSG)
    assert nozzle_throughput_sum >= 0, "Agata się pomyliła :p - Nozzle throughput cannot be smaller than 0!"
    return nozzle_throughput_sum


# tank last element index
tank_last_entry_index = tank.index[-1]

for index in range(1, tank_last_entry_index + 1):
    # iterate over tank table - each time take two entires and use their timestamps to create
    # a "time window" used in nozzles analysis
    tank_entry_t0 = tank.iloc[index - 1]
    tank_entry_t1 = tank.iloc[index]

    tank_entry_t0_timestamp = tank_entry_t0["timestamp"]
    tank_entry_t1_timestamp = tank_entry_t1["timestamp"]

    tank_entry_t0_volume = tank_entry_t0["fuelVolume"]
    tank_entry_t1_volume = tank_entry_t1["fuelVolume"]
    tank_delta = tank_entry_t0_volume - tank_entry_t1_volume

    nozzles_throughput = compute_nozzles_throughput(nozzles.data, tank_entry_t0_timestamp, tank_entry_t1_timestamp)

    balance = tank_delta - sum(nozzles_throughput.values())
    ERR_RATE = 1
    if np.abs(balance) > ERR_RATE:
        print("Inbalance {} - detected at {} : {}".format(balance, tank_entry_t0_timestamp, tank_entry_t1_timestamp))
