# TODO: This could be (most likely) removed

import pandas as pd


class TransactionsExtractor:
    """
    TransactionsExtractor is responsible for extracting transactions from 
    continous data set
    """

    def __init__(self, nozzle: pd.DataFrame):
        """
        `nozzle` :  pandas.DataFrame 
            data from single nozzle
        `error_rate` : float
        """
        self.nozzle = nozzle

    def get_uniq_total_counter_values(self) -> pd.DataFrame:
        """get only rows with uniq values in totalCounter column"""
        return self.nozzle.drop_duplicates("totalCounter", keep="first")

    def extract_as_list(self) -> list:
        """
        Extracts values of single transactions as elemants of `list`

        Single transaction is the amount of fuel purchased in a single refuling
        """
        nozzle_uniq = self.get_uniq_total_counter_values()
        single_transactions = nozzle_uniq.diff()["totalCounter"].tolist()

        # Omit the first element!
        # The first single transaction with 0 value does not bring any useful information.
        # It also allowed to fixed the issue of single transactions being shifted
        # relative to correct timestamps. (This is important later on,
        # when we inject list of single transactions to DataFrame.)
        single_transactions = single_transactions[1:]
        return single_transactions

    def extract_to_column(self) -> pd.DataFrame:
        """
        Inject the output of `self.extract_as_list()` to a DataFrame
        obtained from `self.get_uniq_total_counter_values()`
        """
        nozzle_uniq = self.get_uniq_total_counter_values()
        single_transactions = self.extract_as_list()

        # remove last row
        nozzle_uniq.drop(nozzle_uniq.tail(1).index, inplace=True)

        nozzle_uniq["singleTransaction"] = single_transactions
        return nozzle_uniq
