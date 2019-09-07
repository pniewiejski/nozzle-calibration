import pandas as pd
import numpy as np

from data_abstractions.NozzlesData import NozzlesData
from data_abstractions.Tanks import Tanks
from data_abstractions.TankRefuel import TankRefuel
from data_abstractions.Nozzle import Nozzle
import utils.MapIds as MapIds

from data_exploring.nozzles_throughput import get_nozzles_throughput


def check_balance(tankID=1, NozzlesDataGenerator=NozzlesData):
    """
    For every log from tank check balance betweent tank, nozzle and refueling data. 

    Params:
        tankID - ID of the tank you want to analyse 
        NozzleDataGenerator - Source of data about nozzles:
            By default it is set to the originals data provider.
            It can be set to a erroneous data provider.
    """

    # Get the data: tank, nozzles, refueling
    tanks = Tanks()
    tank = tanks.get_by_id(tankID)

    nozzles = NozzlesDataGenerator()

    tank_refuel = TankRefuel(tankID)

    # tank last element index
    TANK_LAST_ENTRY_INDEX = tank.index[-1]

    for index in range(1, TANK_LAST_ENTRY_INDEX + 1):
        # iterate over tank table - each time take two entires and use their timestamps to create
        # a "time window" used in nozzles analysis
        tank_entry_t0 = tank.iloc[index - 1]
        tank_entry_t1 = tank.iloc[index]

        tank_entry_t0_timestamp = tank_entry_t0["timestamp"]
        tank_entry_t1_timestamp = tank_entry_t1["timestamp"]

        tank_entry_t0_volume = tank_entry_t0["fuelVolume"]
        tank_entry_t1_volume = tank_entry_t1["fuelVolume"]
        tank_delta = tank_entry_t0_volume - tank_entry_t1_volume

        nozzles_throughput = get_nozzles_throughput(
            nozzles, MapIds.get_nozzles_from_tank(tankID), tank_entry_t0_timestamp, tank_entry_t1_timestamp
        )

        tank_refueling_delta = tank_refuel.get_refueling_delta(tank_entry_t0_timestamp, tank_entry_t1_timestamp)

        balance = tank_delta - sum(nozzles_throughput.values()) + tank_refueling_delta

        ERR_RATE = 1
        if np.abs(balance) > ERR_RATE:
            print("Inbalance {} - detected at {} : {}".format(balance, tank_entry_t0_timestamp, tank_entry_t1_timestamp))


# This is just a test
check_balance(1)
