#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 13:31:28 2020

@author: tomaszzurek
"""

# %%

import pandas as pd
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn import metrics
import numpy as np

df = pd.read_csv('weather_madrid_LEMD_1997_2015.csv',
                 parse_dates=['CET'], index_col='CET')


def wynik(y_test, predictions):
    print(metrics.confusion_matrix(y_test, predictions))
    print(metrics.classification_report(y_test, predictions))
    print(metrics.accuracy_score(y_test, predictions))


cols = ['Max TemperatureC', 'Mean TemperatureC', 'Min TemperatureC', 'Dew PointC', 'MeanDew PointC', 'Min DewpointC', 'Max Humidity', ' Mean Humidity', ' Min Humidity', ' Max Sea Level PressurehPa', ' Mean Sea Level PressurehPa', ' Min Sea Level PressurehPa',
        # ' Max VisibilityKm', ' Mean VisibilityKm', ' Min VisibilitykM',' Max Gust SpeedKm/h',' CloudCover',
        ' Max Wind SpeedKm/h', ' Mean Wind SpeedKm/h', 'Precipitationmm', 'WindDirDegrees']


df[' Events'] = df[' Events'].fillna('')

df.ffill(axis=0, inplace=True)


df[df[cols] < df[cols].quantile(.95)]

for col in cols:
    df[col] = df[col] / df[col].abs().max()



# %%
X = df[cols]

z = df[' Events']


events = set(filter(len, sum([f.split('-')
                              for f in df[' Events'].unique()], [])))


y = np.array([[int(e in i) for e in events] for i in z])


print(y)


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.33, random_state=42)
skaler = MinMaxScaler()
skaler.fit(X_train)
X_train_scal = skaler.transform(X_train)
X_test_scal = skaler.transform(X_test)
model = Sequential([
    Dense(12, input_dim=len(cols), activation='relu'),
    Dense(len(events), activation='sigmoid')
])

model.compile(loss='categorical_crossentropy',
              optimizer='adam', metrics=['accuracy'])
model.fit(X_train_scal, y_train, epochs=50, verbose=1)
predictions = model.predict_classes(X_test_scal)

wynik(y_test.argmax(axis=1), predictions)

# x = [[2.5, 3.2, 1.0, 2.3]]
# x = skaler.transform(x)
# pred = model.predict_classes(x)
# print('przyklad: ' + str(pred))
