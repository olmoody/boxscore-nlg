from tensorflow.keras.preprocessing.sequence import pad_sequences
from pickle import load
import numpy as np
from tensorflow.keras.models import load_model

#Load model and tokenizer
model = load_model('nonamemodel.h5')
tokenizer = load(open('nonametokenizer.pkl', 'rb'))

seq_length = 15
result = list()
out_word = ''
in_text = []
count = 0
while not (out_word=="." or out_word=="*end*") and count<101: #while not at end of sentence
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
