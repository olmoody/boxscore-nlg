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


### Model 2 - Text-to-text model. No original input. Text tagged with generic values for names and stats. Captures essence of summaries then replaces tags with values. ###

with open('tagged_summaries_no_names.txt','r') as fr: #read sentences
	lines =json.load(fr)


sequences = []
for sent in lines:  #for every sentence

    max_len = 15 + 1
    cur_len = len(sent)



    for last_index in range(cur_len): ##create sequences
        words = ["*empty*"]*(max_len)
        offset = max(last_index-max_len+1,0) #calc offset
        for i in range(min(last_index,max_len)):
            words[i]=sent[i+offset] #fill in words
        words[max_len-1]=sent[min(last_index,max_len+offset-1)].lower() #set target word
        sequences.append(words)


# integer encode sequences of words
tokenizer = Tokenizer()
tokenizer.fit_on_texts(sequences)
sequences = tokenizer.texts_to_sequences(sequences)

# vocabulary size
vocab_size = len(tokenizer.word_index) + 1
print(vocab_size)


sequences = array(sequences)
X, y = sequences[:,:-1], sequences[:,-1] #input, output
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
model.save('nonamemodel.h5')
dump(tokenizer, open('nonametokenizer.pkl', 'wb'))

#Test on sample input
result = list()
in_text = ["*empty*"]*15
out_word = ''
count = 0
while out_word!="*end*" and count<101: #while not at end of sentence
		# encode the text as integer
        encodedp = tokenizer.texts_to_sequences([in_text])[0]
        words = encodedp
		# truncate sequences to a fixed length
        words_encoded = pad_sequences([words], maxlen=seq_length, truncating='pre',value=1,padding='post')
		# predict probabilities for each word
        pred = model.predict(words_encoded)
        yhat = np.random.choice(len(pred[0]), p=pred[0]) #pick by distribution
        #yhat = np.argmax(pred, axis=-1) # if you want max
		# map predicted word index to word
        out_word = ''
        for word, index in tokenizer.word_index.items():
            if index == yhat:
                out_word = word
                break
		# append to input
        in_text.append(out_word)
        result.append(out_word)
        count+=1
print(' '.join(result)) #print result
