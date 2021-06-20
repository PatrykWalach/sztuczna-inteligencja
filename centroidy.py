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
from sklearn.preprocessing import QuantileTransformer, PowerTransformer
from sklearn.impute import SimpleImputer
from sklearn.cluster import FeatureAgglomeration, KMeans
from sklearn.decomposition import PCA
from sklearn.cluster import MiniBatchKMeans
from sklearn.random_projection import GaussianRandomProjection

df = pd.read_csv('weather_madrid_LEMD_1997_2015.csv',
                 parse_dates=['CET'], index_col='CET')


def wynik(y_test, predictions):
    print(metrics.confusion_matrix(y_test, predictions))
    print(metrics.classification_report(y_test, predictions))
    print(metrics.accuracy_score(y_test, predictions))


cols = ['Max TemperatureC', 'Mean TemperatureC', 'Min TemperatureC', 'Dew PointC', 'MeanDew PointC', 'Min DewpointC', 'Max Humidity', ' Mean Humidity', ' Min Humidity', ' Max Sea Level PressurehPa', ' Mean Sea Level PressurehPa',
        ' Min Sea Level PressurehPa',  ' Max VisibilityKm', ' Mean VisibilityKm', ' Min VisibilitykM', ' Max Gust SpeedKm/h',  ' CloudCover',     ' Max Wind SpeedKm/h', ' Mean Wind SpeedKm/h', 'Precipitationmm', 'WindDirDegrees']

df[' Events'] = df[' Events'].fillna('None')

df = df.dropna()

X = df[cols]
y = df[' Events']


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42)


pca = PCA(n_components=15,
          whiten=True, random_state=42)
pca.fit(X_train)

X_train = pca.transform(X_train)
X_test = pca.transform(X_test)

kmeans = KMeans(n_clusters=3, random_state=42, algorithm='full')
pred_y = kmeans.fit(X_train)
print(pred_y.cluster_centers_)


predictions = pred_y.predict(X_test)

y_test = list(y_test)
for i in range(len(y_test)):
    print(str(y_test[i]) + ' ' + str(predictions[i]))

print(df[' Events'].unique())
