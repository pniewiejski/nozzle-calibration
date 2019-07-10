import pandas as pd 
import matplotlib.pyplot as plt

from data_abstractions.DataSet import DataSet

class Tanks(DataSet):
    def __init__(self):
        super().__init__()
        self.data = pd.read_csv(
            self.get_file_path(1, "tank"),
            sep = ";",
            names=["timestamp", "locationID", "meterID", "tankID",
                    "fuelHeight", "fuelVolume", "fuelTemperature"],
            parse_dates=[0],
            decimal=",",
            usecols=["timestamp", "tankID", "fuelHeight", "fuelVolume"],
        )
    
    def get_tank_by_id(self, id: int) -> pd.DataFrame:
        return self.data[self.data["tankID"] == id]
    
    def plot_4by4(self):
        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12,8))
        for _tankID, axis in enumerate(axes.flat):
            self.data[self.data["tankID"] == _tankID + 1].plot(x="timestamp", y="fuelVolume", ax=axis)
            axis.set_title(f"tank {_tankID + 1}")
        return self

