from text_to_num import alpha2digit
import json
from tensorflow.keras.preprocessing.sequence import pad_sequences
from pickle import load
import numpy as np
from tensorflow.keras.models import load_model
model = load_model('nonamemodel.h5')
tokenizer = load(open('nonametokenizer.pkl', 'rb'))

#find 3 highest scorers
def get_high_scores(box):
    hi = [0,0,0]
    best=[0,0,0]
    for k in box["PTS"].keys():
        val = box["PTS"][k]
        if val.isnumeric():
            val = int(val)
            for i in range(3):
                if val>=hi[i]:
                    hi.insert(i,val)
                    best.insert(i,k)
                    break
        hi = hi[:3]
        best = best[:3]
    return best

# fill out dictionary with stats of highest scorers
def get_stats(best,box):
    tags_dict = {"FIRST_NAME":[],"SECOND_NAME":[],"PTS":[],"AST":[],"REB":[]}
    for tag in tags_dict:
        for player in best:
            tags_dict[tag].append(box[tag][player])
    return tags_dict

with open('../test.json','r') as fr: #read in test data
        d = fr.read()
        full_dict = json.loads(d)


for game in full_dict: #for game in test
    #generate sentence
    seq_length = 15
    result = list()
    out_word = ''
    in_text = []
    count = 0
    while not (out_word=="." or out_word=="*end*") and count<101:  #while not at end of sentence
            # encode the text as integer
            encodedp = tokenizer.texts_to_sequences([in_text])[0]
            words = encodedp
            # truncate sequences to a fixed length
            words_encoded = pad_sequences([words], maxlen=seq_length, truncating='pre',value=1,padding='post')
            # predict probabilities for each word
            pred = model.predict(words_encoded)
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

    #Get high scorers
    h = get_high_scores(game["box_score"])

    #get stats of high scorers
    stats_dict = get_stats(h,game["box_score"])

    tags = {"*firsttname*":"FIRST_NAME","*lastname*":"SECOND_NAME","*ptsval*":"PTS","*astval*":"AST","*rebval*":"REB"}
    tags_used = {"*firsttname*":0,"*lastname*":0,"*ptsval*":0,"*astval*":0,"*rebval*":0}

    #replace keys
    for i,tok in enumerate(result):
        if tok in tags.keys():
            result[i]=stats_dict[tags[tok]][tags_used[tok]]
            tags_used[tok]= (tags_used[tok]+1)%3 #use next player next time

    with open('results.txt','a') as fw:
        fw.write(' '.join(result)+ " \r\n") #write to file
