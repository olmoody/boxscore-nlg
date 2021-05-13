from numpy import array
import numpy as np
from numpy import array
from pickle import dump, load
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Embedding
from tensorflow.keras.preprocessing.sequence import pad_sequences

import json
with open('tagged_summaries_no_names.txt','r') as fr:
	lines =json.load(fr)
print(lines[115])
sent = lines[115]
sequences = []
for sent in lines:
###    sent = ["0","1","2","3","4"]
    stats_list = []
    max_len = 15 + 1
    cur_len = len(sent)


    #lower??? #num2word??
    # start = 0
    for last_index in range(cur_len):
        words = ["*empty*"]*(max_len)
        offset = max(last_index-max_len+1,0)
        for i in range(min(last_index,max_len)):
            words[i]=sent[i+offset]
        words[max_len-1]=sent[min(last_index,max_len+offset-1)]
        sequences.append(words)
#while True:
#    for i in range(start,cur_len+start):
#        words[i]=sent[i]
#    seq = words+stats_list
#    sequences.append(seq)
#    if cur_len-start<max_len:
#        break
print(len(sequences))    
print(sequences[:45])



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
model.fit(X, y, batch_size=512, epochs=35)
model.save('nonamemodel.h5')
dump(tokenizer, open('nonametokenizer.pkl', 'wb'))
tokenizer = load(open('nonametokenizer.pkl', 'rb'))
#seq_length = 50
result = list()
in_text = ["*empty*"]*15
#in_text = ['Harden', '26', '*EMPTY*', '*EMPTY*', '*EMPTY*', '*EMPTY*', 'Harden', '8', '*EMPTY*', '*EMPTY*', '*EMPTY*', '*EMPTY*', 'Harden', '10', '*EMPTY*', '*EMPTY*', '*EMPTY*', '*EMPTY*']
#in_text[18] = 'harden'
# generate a fixed number of words
out_word = ''
count = 0
while out_word!="*end*" and count<101:
		# encode the text as integer
        encodedp = tokenizer.texts_to_sequences([in_text])[0]
        words = encodedp[18:]
		# truncate sequences to a fixed length
        #stats_encoded = pad_sequences([encodedp], maxlen=15, truncating='post')
        words_encoded = pad_sequences([words], maxlen=seq_length, truncating='pre',value=1,padding='post')
		# predict probabilities for each word
        #print(encodedp,[words],stats_encoded,words_encoded)
        print(words_encoded)
        #encoded = np.concatenate((stats_encoded, words_encoded), axis=1)
        pred = model.predict(words_encoded)
        yhat = np.random.choice(len(pred[0]), p=pred[0]) 
        #yhat = np.argmax(pred, axis=-1)
		#yhat = model.predict_classes(encoded, verbose=0)
		# map predicted word index to word
        #print(in_text,encoded,pred,yhat)
        out_word = ''
        for word, index in tokenizer.word_index.items():
            if index == yhat:
                out_word = word
                break
		# append to input
        in_text.append(out_word)
        result.append(out_word)
        count+=1
print(' '.join(result))
