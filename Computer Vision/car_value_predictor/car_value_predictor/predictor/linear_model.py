import numpy as np
import pandas as pd

from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import pickle


def decode_input(input_):
    input_ = [val.upper() if type(val) == str else val for val in input_]
    data = pd.read_csv('true_car_listings.csv')
    data.drop(labels=['City', 'State', 'Vin'], inplace=True, axis=1)
    data.Model = data.Model.str.upper()
    data.Make = data.Make.str.upper()

    X = data.iloc[:, 1:].values
    y = data.iloc[:, 0].values

    X = np.concatenate((X, [input_]))

    label_encoder = LabelEncoder()

    X[:, 2] = label_encoder.fit_transform(X[:, 2])
    label_encoder = LabelEncoder()
    X[:, 3] = label_encoder.fit_transform(X[:, 3])

    return X[-1]


def save_model(model, filename=f'model.sav'):
    pickle.dump(model, open(filename, 'wb'))


def load_model(filename=f'model.sav'):
    return pickle.load(open(filename, 'rb'))


def train():
    data = pd.read_csv('true_car_listings.csv')
    data.drop(labels=['City', 'State', 'Vin'], inplace=True, axis=1)
    data.Model = data.Model.str.upper()
    data.Make = data.Make.str.upper()
    X = data.iloc[:, 1:].values
    y = data.iloc[:, 0].values

    label_encoder = LabelEncoder()
    X[:, 2] = label_encoder.fit_transform(X[:, 2])
    label_encoder = LabelEncoder()
    X[:, 3] = label_encoder.fit_transform(X[:, 3])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

    regressor = LinearRegression()
    regressor.fit(X_train, y_train)

    save_model(regressor)


def predict(input_):
    regressor = load_model()
    return regressor.predict([decode_input(input_)])


# train()
# print(predict([2014, 34000, "TOYOTA", "yaris"]))
