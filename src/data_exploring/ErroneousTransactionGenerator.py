import pandas as pd

from data_exploring.TransactionsExtractor import TransactionsExtractor

class ErroneousTransactionGenerator:
    """
    Generate erroneous transactions for single nozzle
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

    def generate(self) -> pd.DataFrame:
        # # get only rows with uniq values in totalCounter column
        # nozzle_uniq = self.nozzle.drop_duplicates("totalCounter", keep="last")
        # # single transaction is the amount of fuel purchased in a single refuling
        # single_transactions = nozzle_uniq.diff()["totalCounter"].tolist()
        # single_transactions[0] = 0
        # nozzle_uniq = self.extractor.get_uniq_total_counter_values()
        single_transactions = self.extractor.extract_as_list()
        # We use a simple error rate model where 
        # gauge error = fuel from transaction * error rate
        # This model was advised on consultation meeting
        erroneous_transactions = list(map(lambda x : x * (1 + self.error_rate), single_transactions))
        
        single_transactions_df = self.extractor.extract_to_column()
        single_transactions_df["singleTransaction"] = erroneous_transactions
        return single_transactions_df
        
    def compute_erroneous_total_counter(self) -> pd.DataFrame:
        single_transactions_df = self.generate()
        erroneous_total_counter = [sum(erroneous_transactions[0:index+1]) for index in range(len(erroneous_transactions))]
        single_transactions_df["erroneousTotalCounter"] = erroneous_total_counter
        return single_transactions_df
