'''
Creates the MLP network

'''
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import utils.utils as utils

@utils.timeit
def mlp_create(epochs, predict_var, time_steps, filename, normalize_X, optimizer='nadam', testtrainlossgraph=False, batch_size=512, loss_function='mse', metrics=['mse', 'mae', 'mape', 'cosine'], train_split=0.8):
    # 8haverage-merged_2000-2016
    # fix random seed for reproducibility
    np.random.seed(7)
    look_back = 0 # defaulted to 0

    df = utils.read_csvdata(filename)

    col_to_drop = 'target_t+3'
    df.drop(col_to_drop, axis=1, inplace=True)

    # separates into axisX = X and axisY = Y
    axisX, axisY = utils.create_XY_arrays(df, look_back, predict_var, time_steps)

    #saves the minimum and maximum values to normalize the results
    min_value = min(axisY)
    max_value = max(axisY)

    # normalize the datasets
    # only if the input dataset is not normalized, example: when using PCA or Dec Tree they have already been normalized on the X (dataset), thus we only normalize Y/target dataset. However, if it is only a "prepared" dataset, no feature extration method used before, then we normalize it
    if normalize_X:
        scalerX = MinMaxScaler(feature_range=(0, 1))
        axisX = scalerX.fit_transform(axisX)

    # assumes that target is never normalized
    scalerY = MinMaxScaler(feature_range=(0, 1))
    axisY = scalerY.fit_transform(axisY)

    # prepare output arrays
    trainX, testX, trainY, testY = utils.prepare_XY_arrays(axisX, axisY, train_split, look_back)

    # ***
    # Network declaration
    # ***
    model = utils.createnet_mlp1(trainX)

    # compiles the model
    model.compile(loss=loss_function, optimizer=optimizer, metrics=metrics)

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

    # calculates MAE
    utils.calculate_MAE(trainY, trainPredict, testY, testPredict)
    # calculates RMSE
    utils.calculate_RMSE(trainY, trainPredict, testY, testPredict)
    # calculates NRMSE
    utils.calculate_NRMSE(trainY, trainPredict, testY, testPredict, min_value, max_value)

    # creates graph with real test data and the predicted data
    utils.create_realpredict_graph(testY, testPredict)

    # creates graph with new metrics
    utils.plot_metrics(history)


