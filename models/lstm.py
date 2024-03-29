'''
LSTM RNN for predicting timeseries
Original code by Brian
Modified by Felipe Ukan
Creates LSTM neural network.

'''
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import utils.utils as utils

@utils.timeit
def lstm_create(epochs, look_back, predict_var, time_steps, filename, normalize_X, optimizer='nadam', testtrainlossgraph=False, batch_size=512, loss_function='mse', train_split=0.8):
    """

    Given an csv file with all parameters and a 
    """
    # fix random seed for reproducibility
    np.random.seed(7)

    # reads csv file and sets index column
    df = utils.read_csvdata(filename)

    col_to_drop = 'target_t+3'
    df.drop(col_to_drop, axis=1, inplace=True)

    # separates into axisX and axisY the input data
    axisX, axisY = utils.create_XY_arrays(df, look_back, predict_var, time_steps)

    #saves the minimum and maximum values to normalize the results
    min_value = min(axisY)
    max_value = max(axisY)


    # normalize the datasets
    if normalize_X:
        scalerX = MinMaxScaler(feature_range=(0, 1))
        axisX = scalerX.fit_transform(axisX)

    scalerY = MinMaxScaler(feature_range=(0, 1))
    axisY = scalerY.fit_transform(axisY)



    # prepare output arrays
    trainX, testX, trainY, testY = utils.prepare_XY_arrays(axisX, axisY, train_split, look_back)

    # Network declaration
    model = utils.createnet_lstm1(trainX)

    # compiles the model
    model.compile(loss=loss_function, optimizer=optimizer)

    # fits the model
    # history = model.fit(trainX, trainY, epochs=epochs, batch_size=batch_size)
    history = model.fit(trainX, trainY, epochs=epochs, batch_size=batch_size, validation_split=0.2, shuffle=False, verbose=0)

    #evaluates the model
    loss = model.evaluate(testX, testY, verbose=0)

    # test loss and training loss graph. It can help understand the optimal epochs size and if the model is overfitting or underfitting.
    utils.create_testtrainingloss_graph(history, loss)

    # make predictions
    trainPredict = model.predict(trainX)
    testPredict = model.predict(testX)

    # invert predictions
    trainPredict = scalerY.inverse_transform(trainPredict)
    trainY = scalerY.inverse_transform(trainY)
    testPredict = scalerY.inverse_transform(testPredict)
    testY = scalerY.inverse_transform(testY)

    print '-----------------------'
    print('Lookback:', look_back)

    # calculates MAE score
    utils.calculate_MAE(trainY, trainPredict, testY, testPredict)

    # calculates RMSE
    utils.calculate_RMSE(trainY, trainPredict, testY, testPredict)
    # calculates NRMSE
    utils.calculate_NRMSE(trainY, trainPredict, testY, testPredict, min_value, max_value)

    # creates graph with real test data and the predicted data
    utils.create_realpredict_graph(testY, testPredict)
    print '-----------------------'

