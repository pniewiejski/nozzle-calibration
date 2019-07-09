import pandas as pd

from data_exploring.TransactionsExtractor import TransactionsExtractor

class ErrorneousTransactionGenerator:
    """
    Generate errorneus transactions for single nozzle
    """

    def __init__(self, nozzle: pd.DataFrame, error_rate: float):
        """
        `nozzle` :  pandas.DataFrame 
            data from single nozzle
        `error_rate` : float
        """
        self.nozzle = nozzle
        self.error_rate = error_rate
        self.extractor = TransactionsExtractor(nozzle)

    def generate(self):
        # # get only rows with uniq values in totalCounter column
        # nozzle_uniq = self.nozzle.drop_duplicates("totalCounter", keep="last")
        # # single transaction is the amount of fuel purchased in a single refuling
        # single_transactions = nozzle_uniq.diff()["totalCounter"].tolist()
        # single_transactions[0] = 0
        nozzle_uniq = self.extractor.get_uniq_total_counter_values()
        single_transactions = self.extractor.extract_as_list()
        # We use a simple error rate model where 
        # gauge error = fuel from transaction * error rate
        # This model was advised on consultation meeting
        errorneus_transactions = list(map(lambda x : x * (1 + self.error_rate), single_transactions))
        errorneus_total_counter = [sum(errorneus_transactions[0:index+1]) for index in range(len(errorneus_transactions))]
        nozzle_uniq["errorneousTotalCounter"] = errorneus_total_counter
        return nozzle_uniq

