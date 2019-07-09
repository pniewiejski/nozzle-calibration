# This class is responsible for extracting transactions from continous data set

class TransactionsExtractor: 

    def __init__(self, nozzle: pd.DataFrame):
    """
    `nozzle` :  pandas.DataFrame 
        data from single nozzle
    `error_rate` : float
    """
    self.nozzle = nozzle

    def _get_uniq_total_counter_values(self):
        # get only rows with uniq values in totalCounter column
        return self.nozzle.drop_duplicates("totalCounter", keep="last")

    def extract_as_list(self): 
        nozzle_uniq = self._get_uniq_total_counter_values()
        # single transaction is the amount of fuel purchased in a single refuling
        single_transactions = nozzle_uniq.diff()["totalCounter"].tolist()
        single_transactions[0] = 0 # explicitly assing 0 to the first element
        return single_transactions

    def extract_to_column(self):
        nozzle_uniq = self._get_uniq_total_counter_values()
        single_transactions = self.extract_as_list()
        
        nozzle_uniq["singleTransactions"] = single_transactions
        return nozzle_uniq
