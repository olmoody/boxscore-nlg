import json
import random
from tensorflow.keras.preprocessing.sequence import pad_sequences
from pickle import load
import numpy as np
from tensorflow.keras.models import load_model

#Load model and tokenizer
model = load_model('datafullmodel.h5')
tokenizer = load(open('datatokenizer.pkl', 'rb'))

with open('../test.json','r') as fr:
        d = fr.read()
        full_dict = json.loads(d)

game_index = random.randint(0,len(full_dict)-1) #get random game
game = full_dict[game_index]


#generate sentence
seq_length = 15
result = list()

#set input as stat lists
in_text = []
in_text+=[game["box_score"]["PTS"][str(i)] if str(i) in game["box_score"]["PTS"].keys() else "*empty*" for i in range(26)]
in_text+=[game["box_score"]["AST"][str(i)] if str(i) in game["box_score"]["AST"].keys() else "*empty*" for i in range(26)]
in_text+=[game["box_score"]["REB"][str(i)] if str(i) in game["box_score"]["REB"].keys() else "*empty*" for i in range(26)]
in_text+=[game["box_score"]["FIRST_NAME"][str(i)].lower() if str(i) in game["box_score"]["FIRST_NAME"].keys() else "*empty*" for i in range(26)]
in_text+=[game["box_score"]["SECOND_NAME"][str(i)].lower() if str(i) in game["box_score"]["SECOND_NAME"].keys() else "*empty*" for i in range(26)]
in_text = [i.lower() for i in in_text]
print(in_text)
out_word = ''
count = 0

while out_word!="." and count<101: #while not at end of sentence
		# encode the text as integer
        encodedp = tokenizer.texts_to_sequences([in_text])[0]
        words = encodedp[130:]
		# truncate sequences to a fixed length
        stats_encoded = pad_sequences([encodedp], maxlen=130, truncating='post')
        words_encoded = pad_sequences([words], maxlen=seq_length, truncating='pre',value=tokenizer.word_index["*empty*"],padding='post')
		# predict probabilities for each word
        encoded = np.concatenate((stats_encoded, words_encoded), axis=1)
        pred = model.predict(encoded)
        yhat = np.random.choice(len(pred[0]), p=pred[0])  #pick by distribution
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
print(' '.join(result))
