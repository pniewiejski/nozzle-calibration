import os
import matplotlib.pyplot as plt

class DataSet:

    def __init__(self):
        self.DATA_DIR = "../data/data" # TODO: configure path
        self.DATASETS = {1:"1", 2:"2", 3:"3"} # use only 1st set!!!
        self.DATAFILES = {
            "nozzle": "nozzleMeasures.log",
            "refuel": "refuel.log",
            "tank": "tankMeasures.log"
        }
        self.data = None
    
    def get_file_path(self, data_set, data_file):
        """Evaluate file path"""
        return os.path.join(self.DATA_DIR, self.DATASETS[data_set], self.DATAFILES[data_file])

    def show(self):
        """
        Show plot
        """
        plt.show()    
