import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
# import re

from tensorflow.keras.layers import Dense, LSTM, Input, Dropout, Embedding
from tensorflow.keras.models import Sequential
# from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.text import Tokenizer, text_to_word_sequence
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow import keras
# import keras

lessons = [["Backend Developer"], ["Game Developer"], ["Designer"], ["trader"], ["musician"]]

with open('./AI/Stroitel.txt', 'r', encoding='utf-8') as f:
    Stroitel = f.readlines()
    Stroitel[0] = Stroitel[0].replace('\ufeff', '') #убираем первый невидимый символ

with open('./AI/Prog.txt', 'r', encoding='utf-8') as f:
    Prog = f.readlines()
    Prog[0] = Prog[0].replace('\ufeff', '') #убираем первый невидимый символ

with open('./AI/design.txt', 'r', encoding='utf-8') as f:
    Design = f.readlines()
    Design[0] = Design[0].replace('\ufeff', '') #убираем первый невидимый символ

with open('./AI/cryptograph.txt', 'r', encoding='utf-8') as f:
    cryptograph = f.readlines()
    cryptograph[0] = cryptograph[0].replace('\ufeff', '') #убираем первый невидимый символ

with open('./AI/letchick.txt', 'r', encoding='utf-8') as f:
    letchick = f.readlines()
    letchick[0] = letchick[0].replace('\ufeff', '') #убираем первый невидимый символ


texts = Stroitel + Prog + Design + cryptograph + letchick #Stroitel + Prog + Design + cryptograph + letchick
count_Stroitel = len(Stroitel)
count_Prog = len(Prog)
count_Design = len(Design)
count_cryptograph = len(cryptograph)
count_letchick = len(letchick)

total_lines = count_Prog + count_Stroitel + count_Design + count_letchick + count_cryptograph #count_Prog + count_Stroitel + count_Design + count_letchick + count_cryptograph


maxWordsCount = 1000
tokenizer = Tokenizer(num_words=maxWordsCount, filters='!–"—#$%&amp;()*+,-./:;<=>?@[\\]^_`{|}~\t\n\r«»', lower=True, split=' ', char_level=False)
tokenizer.fit_on_texts(texts)

dist = list(tokenizer.word_counts.items())


max_text_len = 5
data = tokenizer.texts_to_sequences(texts)
data_pad = pad_sequences(data, maxlen=max_text_len)


X = data_pad
# Y = np.array([[1, 0]]*count_Prog + [[0, 1]]*count_Design)
Y = np.array([[1, 0, 0, 0, 0]]*count_Stroitel + [[0, 1, 0, 0, 0]]*count_Prog + [[0, 0, 1, 0, 0]]*count_Design + [[0, 0, 0, 1, 0]]*count_cryptograph + [[0, 0, 0, 0, 1]]*count_letchick)

indeces = np.random.choice(X.shape[0], size=X.shape[0], replace=False)
X = X[indeces]
Y = Y[indeces]

model_loaded = keras.models.load_model('./16_model')

# model = Sequential()
# model.add(Embedding(maxWordsCount, 128, input_length = max_text_len))
# model.add(LSTM(128, return_sequences=True))
# model.add(LSTM(64))
# model.add(Dense(5, activation='softmax'))
# model.summary()

# model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer=Adam(0.0001))

# history = model.fit(X, Y, batch_size=32, epochs=200)

# model.save('16_model')

reverse_word_map = dict(map(reversed, tokenizer.word_index.items()))

def sequence_to_text(list_of_indices):
    words = [reverse_word_map.get(letter) for letter in list_of_indices]
    return(words)

def whichLesson(t):
    t = t.lower()
    data = tokenizer.texts_to_sequences([t])
    data_pad = pad_sequences(data, maxlen=max_text_len)

    res = model_loaded.predict(data_pad)
    return {"procent":int(res[0][np.argmax(res)]*100), "prof":lessons[np.argmax(res)]}#np.argmax(res),