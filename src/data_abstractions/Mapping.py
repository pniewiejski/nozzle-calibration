import os
import pandas as pd
import matplotlib.pyplot as plt


class Mapping:
    def __init__(self):
        self.DATA_DIR = "../data/mapping"  # TODO: configure path
        self.DATAFILES = {
            "tank1": "Tank1_10012.csv",
            "tank2": "Tank2_20000.csv",
            "tank3": "Tank3_30000.csv",
            "tank4": "Tank4_40000.csv",
        }
        self.data = {tank: pd.read_csv(self.get_file_path(tank), sep=";") for tank in self.DATAFILES}

    def get_file_path(self, data_file):
        """Evaluate file path"""
        return os.path.join(self.DATA_DIR, self.DATAFILES[data_file])

    def plot_4by4(self):
        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))
        for (key, value), axis in zip(self.data.items(), axes.flat):
            value.plot(y="Volume", x="Height", ax=axis)
            axis.set_title(f"{key}", loc="left")
        return self

    def show(self):
        plt.show()
