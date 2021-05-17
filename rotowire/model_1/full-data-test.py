from tensorflow.keras.preprocessing.sequence import pad_sequences
from pickle import load
import numpy as np
import json
import random
from tensorflow.keras.models import load_model

model = load_model('model.h5')
tokenizer = load(open('tokenizer.pkl', 'rb'))
with open('tagged_test_summaries.txt','r') as fr: #read in summaries
        d = fr.read()
        full_dict = json.loads(d)


random.shuffle(full_dict) #randomize order
seq_length = 15
total_names = 0
total = 0
match = 0
names_match = 0

print(len(full_dict))

for sent in full_dict[:500]: #try 500 sentences
    result = list()
    in_text = ["*EMPTY*"]*18
    index = 0
    if not sent[-3] and not sent[-2] and not sent[-1]: #if no stats then skip
        continue
    ## fill in stats list
    for k in sent[-3]:
        in_text[index]=k
        in_text[index+1]=sent[-3][k]
        index+=2
    index=6
    for k in sent[-2]:
        in_text[index]=k
        in_text[index+1]=sent[-2][k]
        index+=2
    index=12
    for k in sent[-1]:
        in_text[index]=k
        in_text[index+1]=sent[-1][k]
        index+=2

    in_text = [i.lower() for i in in_text] #make sure all lowercase
    orig_in_text = in_text[:] #save copy to write
    out_word = ''
    count = 0
    while out_word!="." and count<101: #while not at end of sentence
            # encode the text as integer
            encodedp = tokenizer.texts_to_sequences([in_text])[0]
            words = encodedp[18:] #separate words and stats
            # truncate sequences to a fixed length
            stats_encoded = pad_sequences([encodedp], maxlen=18, truncating='post')
            words_encoded = pad_sequences([words], maxlen=seq_length, truncating='pre',value=1,padding='post')
            # predict probabilities for each word
            encoded = np.concatenate((stats_encoded, words_encoded), axis=1)
            pred = model.predict(encoded)
            yhat = np.random.choice(len(pred[0]), p=pred[0]) #pick by distribution
            #yhat = np.argmax(pred, axis=-1) #if you want max
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

    with open('results-stats.txt','a') as fw: #write output and orig input
       fw.write(' '.join(orig_in_text))
       fw.write(' '.join(result)+ " \r\n")
    if orig_in_text[0]!="*empty*" and orig_in_text[0] in result: #name matches
        names_match+=1
    for word in orig_in_text: #count total matches
        if word !="*empty*":
            total+=1
            if word in result:
                match+=1
    total_names+=1

print(names_match,match,total_names,total,names_match/total_names,match/total)
