from numpy import array
import numpy as np
from numpy import array
from pickle import dump, load
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Embedding
from tensorflow.keras.preprocessing.sequence import pad_sequences
import json

### Model 3 - Full box score to text model. Input in form of lists of stats. Text tagged with generic values for names and stats with index. ###

with open('tagged_summaries_noname_dicts.txt','r') as fr:
	lines =json.load(fr)


sequences = []
for sent in lines:
    max_len = 15 + 1
    cur_len = len(sent)-5
    stats_list = []

    for stat in sent[-5:]:  #for each stat (pts, ast, reb, firstname, lastname)
        stats_list+=stat #append together

    for last_index in range(cur_len): ##create sequences
        words = ["*empty*"]*(max_len)
        offset = max(last_index-max_len+1,0) #calc offset
        for i in range(min(last_index,max_len)):
            words[i]=sent[i+offset].lower() #fill in words
        words[max_len-1]=sent[min(last_index,max_len+offset-1)].lower() #set target word
        seq = stats_list+words #add stats list
        sequences.append(seq)


# integer encode sequences of words
tokenizer = Tokenizer()
tokenizer.fit_on_texts(sequences)
sequences = tokenizer.texts_to_sequences(sequences)

# vocabulary size
vocab_size = len(tokenizer.word_index) + 1
print(vocab_size)


sequences = array(sequences)
X, y = sequences[:,:-1], sequences[:,-1]
y = to_categorical(y, num_classes=vocab_size)
seq_length = X.shape[1]

print(seq_length)

# define model
model = Sequential()
model.add(Embedding(vocab_size, seq_length, input_length=seq_length))
model.add(LSTM(100, return_sequences=True))
model.add(LSTM(100))
model.add(Dense(100, activation='relu'))
model.add(Dense(vocab_size, activation='softmax'))
print(model.summary())

# compile model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# fit model
model.fit(X, y, batch_size=256, epochs=50)

# save model
model.save('datafullmodel.h5')
dump(tokenizer, open('datatokenizer.pkl', 'wb'))
