#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  1 20:35:20 2020

@author: tomaszzurek
"""


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.svm import SVC
from sklearn.preprocessing import QuantileTransformer


df = pd.read_csv('weather_madrid_LEMD_1997_2015.csv',
                 parse_dates=['CET'], index_col='CET')


def wynik(y_test, predictions):
    print(metrics.confusion_matrix(y_test, predictions))
    print(metrics.classification_report(y_test, predictions))
    print(metrics.accuracy_score(y_test, predictions))


cols = ['Max TemperatureC', 'Mean TemperatureC', 'Min TemperatureC', 'Dew PointC', 'MeanDew PointC', 'Min DewpointC', 'Max Humidity', ' Mean Humidity', ' Min Humidity', ' Max Sea Level PressurehPa', ' Mean Sea Level PressurehPa', ' Min Sea Level PressurehPa',
        ' Max VisibilityKm', ' Mean VisibilityKm', ' Min VisibilitykM',
        #  ' Max Gust SpeedKm/h', ' CloudCover',
        ' Max Wind SpeedKm/h', ' Mean Wind SpeedKm/h', 'Precipitationmm', 'WindDirDegrees']

df[' Events'] = df[' Events'].fillna('None')

df.ffill(axis=0, inplace=True)

X = df[cols]
y = df[' Events']


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=0)


scaler = QuantileTransformer(output_distribution='normal', random_state=0)
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)


rf_model = SVC()
rf_model.fit(X_train_scaled, y_train)
predictions = rf_model.predict(X_test_scaled)
wynik(y_test, predictions)


# predictionrf = rf_model.predict([[5,4,2,0.1]])
# predictionnb = nb_model.predict([[5,4,2,0.1]])
# print(predictionrf)
# print(predictionnb)
