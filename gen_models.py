'''
Function to generate parameters and call LSTM model function
use lstm.py
'''
from network_models.lstm import lstm_create
import multiprocessing
from functools import partial
import json

def create_epoch():
    return [1,20,40]

def create_inputnodes():
    return [50, 150]

def create_lookback():
    return [x for x in range(1,31,10)]

def create_leadtime():
    return [x for x in range(1,41,10)]

# target_col_num = 25 # manually set might try to make it the last by default, need the size first, so just inside the function
# # filename = 'datasets/kuwait.csv'
# filename = 'datasets/max-merged_2000-2016.csv'
# optimizer = 'nadam'
# testtrainlossgraph = True
# batch_size = 512
# loss_function = 'mse'
# train_split = 0.8 # test_splt is = 1 - train_split, always.

# pool = multiprocessing.Pool(4)

# for epochs in create_epoch():
#     for input_nodes in create_inputnodes():
#         for look_back in create_lookback():
#             # for lead_time in create_leadtime():
#                 # complexity x^4
#             print epochs, input_nodes, look_back
#             func = partial(lstm_create, epochs, input_nodes, look_back)
#             pool.map(func, create_leadtime())
#                 # lstm_create(epochs, input_nodes, look_back, lead_time, filename=filename)

# pool.close() 
# pool.join() 
configs = json.loads(open('config_lstm.json').read())
epochs = configs['model']['epochs']
inputnodes = configs['model']['input_nodes']
lookback = configs['model']['look_back']
leadtime = configs['data']['lead_time']

# epochs, inputnodes, lookback, leadtime
lstm_create(epochs, inputnodes, lookback, leadtime)