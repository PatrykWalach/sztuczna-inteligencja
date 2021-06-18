# %%
from sklearn import metrics
import gensim
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.layers import Embedding
from tensorflow.keras.layers import Dense, Dropout, Activation, LSTM
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.text import Tokenizer
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd

np.random.seed(7)
#from pickle import dump


def wynik(y_test, predictions):
    print(metrics.classification_report(y_test, predictions))
    print(metrics.accuracy_score(y_test, predictions))
    print(metrics.confusion_matrix(y_test, predictions))


word2vec_model = gensim.models.KeyedVectors.load_word2vec_format(
    'enwiki_20180420_100d.txt', binary=False)

print('Model loaded')
# %%

df = pd.read_csv('train-amazon.tsv', sep='\t')
X = df['review']
z = df['label']
y = []
for i in z:
    if i == 'pos':
        k = 0
    else:
        k = 1
    y.append(k)


y = to_categorical(y)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

X_train, X_val, y_train, y_val = train_test_split(
    X_train, y_train, test_size=0.2, random_state=42)


print(dir(word2vec_model))
embedding_matrix = word2vec_model.vectors


top_words = embedding_matrix.shape[0]
mxlen = 100


tokenizer = Tokenizer(num_words=top_words)
tokenizer.fit_on_texts(X_train)
sequences_train = tokenizer.texts_to_sequences(X_train)
sequences_test = tokenizer.texts_to_sequences(X_test)
sequences_val = tokenizer.texts_to_sequences(X_val)

word_index = tokenizer.word_index
print('Found %s unique tokens.' % len(word_index))


X_train_padded = sequence.pad_sequences(sequences_train, maxlen=mxlen)
X_test_padded = sequence.pad_sequences(sequences_test, maxlen=mxlen)
X_val_padded = sequence.pad_sequences(sequences_val, maxlen=mxlen)

batch_size = 32
nb_epoch = 100

embedding_layer = Embedding(embedding_matrix.shape[0],
                            embedding_matrix.shape[1],
                            weights=[embedding_matrix],
                            trainable=False)

model = Sequential()
model.add(embedding_layer)
model.add(LSTM(128, dropout=0.3, recurrent_dropout=0.2))
model.add(Dropout(0.2))
model.add(Dense(20, input_dim=129, activation='relu', use_bias=True))
model.add(Dense(2, use_bias=True))
model.add(Activation('softmax'))
model.summary()


model.compile(optimizer='adam', loss='categorical_crossentropy',
              metrics=['accuracy'])
rnn = model.fit(X_train_padded, y_train, epochs=nb_epoch, batch_size=batch_size,
                shuffle=True, validation_data=(X_val_padded, y_val))

# model.save('model-eng-embed-nn.h5')
#dump(tokenizer, open('tokeny-embedd-en', 'wb'))

# testy
print('testowe')
predykcje = model.predict(X_test_padded)

predictions = predykcje.round()

igrek = len(predictions)*[0]
zet = len(y_test)*[0]
print(metrics.classification_report(y_test, predictions))
print(metrics.accuracy_score(y_test, predictions))
for i in range(len(y_test)):

    a = (predykcje[i][1]-predykcje[i][0])

    if(a > 0):
        igrek[i] = 1
    if(y_test[i][1] == 1):
        zet[i] = 1


print(metrics.confusion_matrix(zet, igrek))

# %%
