from data_abstractions.Nozzles import Nozzles
from data_exploring.ErrorneousTransactionGenerator import ErrorneousTransactionGenerator

nozzles = Nozzles()

generator = ErrorneousTransactionGenerator(nozzles.get_nozzle(14), 0.1)

errorneous_data = generator.generate()
print(errorneous_data)