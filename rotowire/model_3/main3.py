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
with open('tagged_summaries_noname_dicts.txt','r') as fr:
	lines =json.load(fr)
#pts_list = ["*ptsval{}*".format(i) for i in range(26)]
#ast_list = ["*astval{}*".format(i) for i in range(26)]
#reb_list = ["*rebval{}*".format(i) for i in range(26)]
#first_list = ["*firstname{}*".format(i) for i in range(26)]
#last_list = ["*lastname{}*".format(i) for i in range(26)]
print(lines[115])
sent = lines[115]
sequences = []
for sent in lines:
    max_len = 15 + 1
    cur_len = len(sent)-5
    stats_list = []
    for stat in sent[-5:]:
        stats_list+=stat
    #stats_list = pts_list+ast_list+reb_list+first_list+last_list
    #lower??? #num2word??
    # start = 0
    for last_index in range(cur_len):
        words = ["*empty*"]*(max_len)
        offset = max(last_index-max_len+1,0)
        for i in range(min(last_index,max_len)):
            words[i]=sent[i+offset].lower()
        words[max_len-1]=sent[min(last_index,max_len+offset-1)].lower()
        seq = stats_list+words
        sequences.append(seq)
#while True:
#    for i in range(start,cur_len+start):
#        words[i]=sent[i]
#    seq = words+stats_list
#    sequences.append(seq)
#    if cur_len-start<max_len:
#        break

print(sequences[:40])



# integer encode sequences of words
tokenizer = Tokenizer()
tokenizer.fit_on_texts(sequences)
sequences = tokenizer.texts_to_sequences(sequences)
#print(sequences)
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
model.save('datafullmodel.h5')
dump(tokenizer, open('datatokenizer.pkl', 'wb'))
