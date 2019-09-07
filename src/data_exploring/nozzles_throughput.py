import pandas as pd
import numpy as np

from data_abstractions.NozzlesData import NozzlesData
from data_abstractions.Tanks import Tanks
from data_abstractions.TankRefuel import TankRefuel
from data_abstractions.Nozzle import Nozzle
import utils.MapIds as MapIds


def get_nozzles_throughput(nozzles: NozzlesData, nozzleIDs: list, t0, t1) -> dict:

    nozzles_subset = nozzles.get_entries_between_timestamps(t0, t1)

    # iterate over nozzles associated with a given tank
    nozzle_throughput = {i: 0 for i in nozzleIDs}

    for nozzleID in nozzleIDs:
        single_nozzle = Nozzle(nozzles_subset[nozzles_subset["nozzleID"] == nozzleID])
        nozzle_throughput[nozzleID] = compute_throughput(single_nozzle, t0, t1)

    print("Nozzle throughput {} between {} and {}".format(nozzle_throughput, t0, t1))

    return nozzle_throughput


def compute_throughput(nozzle: Nozzle, t0, t1):
    """Compute nozzle's throughput between timestamps t0 and t1"""

    nozzle_throughput_sum = 0

    if nozzle.has_ongoing_transactions() or nozzle.has_finished_transactions():
        if nozzle.countains_transaction_start():
            total_counter = nozzle.get_total_counter_as_list()
            if nozzle.get_liter_counter_at_timestamp(t1) == 0:
                nozzle_throughput_sum += max(total_counter) - min(total_counter) + nozzle.get_liter_counter_at_timestamp(t0)
            else:
                nozzle_throughput_sum += (
                    nozzle.get_liter_counter_at_timestamp(t1)
                    + max(total_counter)
                    - min(total_counter)
                    - nozzle.get_liter_counter_at_timestamp(t0)
                )

        else:
            if nozzle.get_liter_counter_at_timestamp(t1) != 0:
                nozzle_throughput_sum += nozzle.get_liter_counter_at_timestamp(t1) - nozzle.get_liter_counter_at_timestamp(
                    t0
                )
            else:
                total_counter = nozzle.get_total_counter_as_list()
                nozzle_throughput_sum += max(total_counter) - min(total_counter) - nozzle.get_liter_counter_at_timestamp(t0)

    assert nozzle_throughput_sum >= 0, "Agata się pomyliła :p - Nozzle throughput cannot be smaller than 0!"

    return nozzle_throughput_sum
