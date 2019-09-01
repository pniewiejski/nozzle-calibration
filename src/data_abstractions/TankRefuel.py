import pandas as pd

from data_abstractions.Refuel import Refuel


class TankRefuel:
    def __init__(self, tankID: int):
        refueling_data = Refuel()
        # reseting index !
        self.data = refueling_data.get_by_tank_id(tankID).reset_index(inplace=True)

    def _get_last_index(self):
        """
        get index of the last element in `self.data`
        """
        return self.data.tail(1).index

    def _get_pumping_rate_by_index(self, index):
        return self.data.iloc[index]["pumpingRate"]

    def _get_closest_refuel_start(self, timestamp):
        """
        get a refueling entry with the closest timestamp to provided
        `timestamp` argument. `timestamp` must be in the future relative to 
        selected row's timestamp.
        """
        nearest_index = abs(self.data["timestamp"] - timestamp).idxmin()

        if self.data.iloc[nearest_index]["timestamp"] < timestamp:
            return nearest_index
        elif nearest_index > 0:
            # if nearest_index does not refer to the first entry
            return nearest_index - 1
        else:
            # This is the case where `timestamp` argument is before every
            # refueling that occured
            return None

    def _get_predicted_refueling_end(self, index):
        """
        get timestamp of the predicted refueling end

        `index` - index of refueling entry in `self.data`
        """
        single_refuel_data = self.data.iloc[index]
        refuel_start_timestamp = single_refuel_data["timestamp"]
        refueling_rate = single_refuel_data["pumpingRate"]
        declared_volume = single_refuel_data["declaredVolume"]

        # refueling time in seconds (I hope it's seconds xD)
        refueling_time_seconds = (declared_volume / refueling_rate) * 60
        refueling_timedelta = pd.to_timedelta(refueling_time_seconds, unit="seconds")
        return refuel_start_timestamp + refueling_timedelta

    def get_refueling_delta(self, t1, t2):
        """
        Get the amount of fuel that has been added to a tank in a refueling process 
        between `t1` and `t2`
        """

        def calculate_timedelta(a, b):
            return pd.Timedelta(a - b).seconds / 60

        refueling_start_index = self._get_closest_refuel_start(t1)

        if refueling_start_index is None:
            return 0
        else:
            predicted_refueling_end_timestamp = self._get_predicted_refueling_end(
                refueling_start_index
            )
            refueling_rate = self._get_pumping_rate_by_index(refueling_start_index)

            if predicted_refueling_end_timestamp < t1:
                # predicted end is before t1
                return 0
            elif predicted_refueling_end_timestamp < t2:
                # refueling will end before t2
                return (
                    calculate_timedelta(predicted_refueling_end_timestamp, t1)
                    * refueling_rate
                )
            else:
                return calculate_timedelta(t2, t1) * refueling_rate
