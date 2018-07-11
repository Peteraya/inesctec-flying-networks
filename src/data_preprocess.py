from sklearn.model_selection import train_test_split
import numpy as np
from load_data import *


abs_path = os.path.abspath(os.path.dirname(__file__))

if platform.system() == "Windows" :
	DATASET_DIRECTORY =  "../DataSet" 
else:
	DATASET_DIRECTORY = os.path.join(abs_path, "../DataSet")


results = read_results(DATASET_DIRECTORY)
scenarios = read_scenarios(DATASET_DIRECTORY)



sparse_matrix = np.zeros((10,10), dtype = 'int')
sparse_matrix = np.matrix(sparse_matrix)



