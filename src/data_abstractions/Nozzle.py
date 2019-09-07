import pandas as pd


class Nozzle:
    def __init__(self, nozzle: pd.DataFrame):
        self.data = nozzle

    def get_dataframe(self):
        return self.data

    def has_finished_transactions(self):
        """
        Check if nozzle dataframe contains finished transactions.
        This is done by checking if the value of the total counter has changed. 
        """
        return self.data.drop_duplicates("totalCounter", keep="first").shape[0] > 1

    def has_ongoing_transactions(self):
        """nozzle dataframe contains non-zero values in literCounter in the analysed time window"""
        return not self.data[self.data["literCounter"] > 0].empty

    def countains_transaction_start(self):
        # TODO: check if this works corectly!
        nozzle_status = self.data["status"].tolist()
        print(nozzle_status)
        previous_status = nozzle_status[0]
        for status in nozzle_status[1:]:
            if previous_status > status:
                return True
            previous_status = status

    def get_liter_counter_at_timestamp(self, timestamp):
        nozzle_at_timestamp = self.data[self.data["timestamp"] == timestamp]
        assert nozzle_at_timestamp.empty == False, "No iternet connection!"

        return nozzle_at_timestamp["literCounter"].values[0]

    def get_column_as_list(self, column_name: str):
        return self.data[column_name].tolist()

    def get_total_counter_as_list(self):
        return self.get_column_as_list("totalCounter")
