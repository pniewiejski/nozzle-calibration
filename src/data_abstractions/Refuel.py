import pandas as pd 
import matplotlib.pyplot as plt

from data_abstractions.DataSet import DataSet

class Refuel(DataSet):
    def __init__(self):
        super()
        self.data = pd.read_csv(
                self.get_file_path(1, "refuel"),
                sep = ";",
                names=["timestamp", "tankID", "declaredVolume", "pumpingRate"],
                decimal=",",
                parse_dates=[0],
            )

    
