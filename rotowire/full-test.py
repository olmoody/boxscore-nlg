from text_to_num import alpha2digit
import json
from tensorflow.keras.preprocessing.sequence import pad_sequences
from pickle import load
import numpy as np
from tensorflow.keras.models import load_model
model = load_model('nonamemodel.h5')
tokenizer = load(open('nonametokenizer.pkl', 'rb'))

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
    
def get_stats(best,box):
    tags_dict = {"FIRST_NAME":[],"SECOND_NAME":[],"PTS":[],"AST":[],"REB":[]}
    for tag in tags_dict:
        for player in best:
            tags_dict[tag].append(box[tag][player])
    return tags_dict
    
with open('test.json','r') as fr:
        d = fr.read()
        full_dict = json.loads(d)
for game in full_dict:

    seq_length = 15
    result = list()
    out_word = ''
    #in_text = ["atlanta", "hawks","orlando", "magic","*end*","*firsttname*","*lastname*"]
    in_text = []
    count = 0
    while not (out_word=="." or out_word=="*end*") and count<101:
            # encode the text as integer
            encodedp = tokenizer.texts_to_sequences([in_text])[0]
            words = encodedp
            #print(words)
            # truncate sequences to a fixed length
            words_encoded = pad_sequences([words], maxlen=seq_length, truncating='pre',value=1,padding='post')
            # predict probabilities for each word
            #print(words_encoded)
            pred = model.predict(words_encoded)
            yhat = np.random.choice(len(pred[0]), p=pred[0])
            #yhat = np.argmax(pred, axis=-1)
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
    #print(' '.join(result))

    #remove *end*

    h = get_high_scores(game["box_score"])
    #print(h)


    stats_dict = get_stats(h,game["box_score"])
    tags = {"*firsttname*":"FIRST_NAME","*lastname*":"SECOND_NAME","*ptsval*":"PTS","*astval*":"AST","*rebval*":"REB"}
    tags_used = {"*firsttname*":0,"*lastname*":0,"*ptsval*":0,"*astval*":0,"*rebval*":0}
    for i,tok in enumerate(result):
        if tok in tags.keys():
            result[i]=stats_dict[tags[tok]][tags_used[tok]]
            tags_used[tok]= (tags_used[tok]+1)%3
    #print(' '.join(result))
    with open('results.txt','a') as fw:
        fw.write(' '.join(result)+ " \r\n")
