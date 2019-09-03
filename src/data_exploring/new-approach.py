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


def do_stuff_for_nozzles(nozzles, t0, t1):

    # select subset of all nozzles between t0 and t1
    mask = (nozzles["timestamp"] >= t0) & (nozzles["timestamp"] <= t1)
    nozzles_subset = nozzles.loc[mask]

    # iterate over nozzles associated with a given tank
    # TODO: refactor it so it is not hardcoded :p
    for nozzleID in [13, 17, 21]:
        print(f"Nozzle: {nozzleID}")
        do_stuff_for_nozzle(
            nozzles_subset[nozzles_subset["nozzleID"] == nozzleID], t0, t1
        )
        print("**********************************")


# TODO: change this name
def do_stuff_for_nozzle(single_nozzle_subset, t0, t1):
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
        liter_counter = nozzle["literCounter"].tolist()
        [i for i, x in enumerate(liter_counter) if x == 0] > [
            i for i, x in enumerate(liter_counter) if x > 0
        ]

    def get_liter_counter_at_timestamp(nozzle, timestamp):
        nozzle_at_timestamp = nozzle[nozzle["timestamp"] == timestamp]
        # print(nozzle, timestamp)
        # print(nozzle_at_timestamp)
        assert nozzle_at_timestamp.empty == False, "No iternet connection!" 
        # print(nozzle_at_timestamp["literCounter"].values[0], type(nozzle_at_timestamp["literCounter"]))
        return nozzle_at_timestamp["literCounter"].values[0]

    nozzle_throughput_sum = 0

    if has_ongoing_transactions(single_nozzle_subset) or has_finished_transactions(
        single_nozzle_subset
    ):
        print("Should return non-zero value :) ")
        # things will happen here!

        # check if it contains beginning of transactions
        if countains_transaction_start(single_nozzle_subset):
            if get_liter_counter_at_timestamp(single_nozzle_subset, t1) == 0:
                liter_counter = single_nozzle_subset["totalCounter"].tolist()
                nozzle_throughput_sum += max(liter_counter) - min(liter_counter)
            else:
                nozzle_throughput_sum += get_liter_counter_at_timestamp(
                    single_nozzle_subset, t1
                )

        else:
            if get_liter_counter_at_timestamp(single_nozzle_subset, t1) != 0:
                nozzle_throughput_sum += get_liter_counter_at_timestamp(
                    single_nozzle_subset, t1
                ) - get_liter_counter_at_timestamp(single_nozzle_subset, t0)
            else:
                liter_counter = single_nozzle_subset["totalCounter"].tolist()
                nozzle_throughput_sum += (
                    max(liter_counter)
                    - min(liter_counter)
                    - get_liter_counter_at_timestamp(single_nozzle_subset, t0)
                )

    print(f"{nozzle_throughput_sum}")

        # calculate deltas
        # cases for: beginning of transactions
        # check graph on trello xD


# tank last element index
tank_last_entry_index = tank.index[-1]

for index in range(1, tank_last_entry_index + 1):
    # iterate over tank table - each time take two entires and use their timestamps to create
    # a "time window" used in nozzles analysis
    tank_entry_t0 = tank.iloc[index - 1]
    tank_entry_t1 = tank.iloc[index]

    tank_entry_t0_timestamp = tank_entry_t0["timestamp"]
    tank_entry_t1_timestamp = tank_entry_t1["timestamp"]

    # TODO: refactor this name later :shrug
    do_stuff_for_nozzles(nozzles.data, tank_entry_t0_timestamp, tank_entry_t1_timestamp)
