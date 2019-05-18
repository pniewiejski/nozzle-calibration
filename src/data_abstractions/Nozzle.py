import pandas as pd 
import matplotlib.pyplot as plt

from data_abstractions.DataSet import DataSet

class Nozzle(DataSet):
    def __init__(self):
        super()
        self.data = pd.read_csv(
            self.get_file_path(1, "nozzle"),
            sep = ";",
            names=["timestamp", "locationID", "nozzleID", "tankID", "literCounter",
                    "totalCounter", "status"],
            parse_dates=[0],
            decimal=",",
            usecols=["timestamp", "nozzleID", "tankID", "literCounter", "totalCounter", "status"]
        )
