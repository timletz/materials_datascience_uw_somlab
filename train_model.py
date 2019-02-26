import tensorflow
import tensorflow.keras.models
import tensorflow.keras.layers
import tensorflow.keras.wrappers.scikit_learn as sk_keras

import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from typing import List
import functools

def model(input_dim: int, hidden_layers: List[int]):
    model = models.Sequential()
    output_dimensions = 1
    model.add(layers.Dense(input_dim, input_dim=input_dim, kernel_initializer='normal', activation='relu'))
    for node_count in hidden_layers:
        model.add(layers.Dense(node_count, kernel_initializer='normal', activation='relu'))
    model.add(layers.Dense(output_dimensions, kernel_initializer='normal'))
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model

def prediction(data_total: pd.DataFrame, new_data: pd.DataFrame, x_indices: List[str], y_index: str):
    """
    Build a NN to train on the given `x_indices` to estimate a `y_index`.
    """
    seed = 21899
    df5 = new_data.loc[0:1]
    X = data_total[x_indices].values
    Y = data_total[[y_index]].values
    X1 = df5[x_indices].values
    X_train_pn, X_test_pn, y_train, y_test1 = train_test_split(X, Y, test_size=0.2, random_state=seed)
    X_train_scaler = StandardScaler().fit(X_train_pn)
    X_train = X_train_scaler.transform(X_train_pn)
    np.random.seed(seed)
    # This creates a model function with the desired structure
    model_function = functools.partial(model, input_dim=len(x_indices), hidden_layers=[12])
    estimator = sk_keras.KerasRegressor(build_fn=model_function, epochs=500, batch_size=1e5, verbose=0)
    # What is "history" used for?
    history = estimator.fit(X_train, y_train, validation_split=0.33, epochs=500,
            batch_size=5000, verbose=0)
    X2 = X_train_scaler.transform(X1)
    return estimator.model.predict(X2, batch_size=3e5)
