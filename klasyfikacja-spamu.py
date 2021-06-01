#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 11:21:05 2020

@author: tomaszzurek
"""


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC, LinearSVR, NuSVC, SVC
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.decomposition import TruncatedSVD
import sklearn as sk


def wynik(y_test, predictions):
    print(metrics.confusion_matrix(y_test, predictions))
    print(metrics.classification_report(y_test, predictions))
    print(metrics.accuracy_score(y_test, predictions))


df = pd.read_csv('train-amazon.tsv', sep='\t')
X = df['review']
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42)
print(X_train.shape)
print(y_train.shape)

text_clf = Pipeline([('count_vec', sk.feature_extraction.text.CountVectorizer(ngram_range=(
    1, 2))), ('tfidf', sk.feature_extraction.text.TfidfTransformer(sublinear_tf=True)),   ('clf', LinearSVC())])
# text_clf = Pipeline([('count_vec', CountVectorizer(stop_words='english', ngram_range = (1,2))), ('clf', LinearSVC())])
# text_clf = Pipeline([('count_vec', CountVectorizer(stop_words='english')), ('clf', LinearSVC())])
# text_clf = Pipeline([('count_vec', CountVectorizer()), ('clf', LinearSVC())])
print(text_clf)
text_clf.fit(X_train, y_train)
predictions = text_clf.predict(X_test)
print(predictions)
wynik(y_test, predictions)
proba = [
    'An Invitation for you to take part in CMSAM as the Reviewer Dear De./Prof., Welcome you to attend the 2019 4th International Conference on Computational Modeling, Simulation and Applied Mathematics (CMSAM2019) It will be held in Guangzhou, China from December 27-29, 2019.']
predictions = text_clf.predict(proba)
print(predictions)
