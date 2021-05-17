from tensorflow.keras.preprocessing.sequence import pad_sequences
from pickle import load
import numpy as np
from tensorflow.keras.models import load_model
model = load_model('model.h5')
tokenizer = load(open('tokenizer.pkl', 'rb'))

seq_length = 15
result = list()
in_text = ["*EMPTY*"]*18
in_text = ['Durant', '26', '*EMPTY*', '*EMPTY*', '*EMPTY*', '*EMPTY*', 'Durant', '8', '*EMPTY*', '*EMPTY*', '*EMPTY*', '*EMPTY*', 'Durant', '10', '*EMPTY*', '*EMPTY*', '*EMPTY*', '*EMPTY*']
in_text = [i.lower() for i in in_text] 
out_word = ''
count = 0
while out_word!="." and count<101:
		# encode the text as integer
        encodedp = tokenizer.texts_to_sequences([in_text])[0]
        words = encodedp[18:]
		# truncate sequences to a fixed length
        stats_encoded = pad_sequences([encodedp], maxlen=18, truncating='post')
        words_encoded = pad_sequences([words], maxlen=seq_length, truncating='pre',value=1,padding='post')
		# predict probabilities for each word
        #print(encodedp,[words],stats_encoded,words_encoded)
        print(stats_encoded,words_encoded)
        encoded = np.concatenate((stats_encoded, words_encoded), axis=1)
        pred = model.predict(encoded)
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
