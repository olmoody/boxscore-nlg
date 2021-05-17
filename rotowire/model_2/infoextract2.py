import json
from text_to_num import alpha2digit

with open('../train.json','r') as fr:
	d = fr.read()
	full_dict = json.loads(d)

## get key from value in specific dictionary
def get_key(val,my_dict):
    keys = []
    for key, value in my_dict.items():
         if val == value:
             keys.append(key)
    return keys


new_sum = [] #return list
hi = 0 #max length
for game in full_dict:
	#split summary into sentences
    old_sum = game["summary"]

	#[[w1,w2,w3,.,]]
    player_rows = []
    cur_sent = []
    for tok in old_sum: #for each word in summary
        if tok in game["box_score"]["SECOND_NAME"].values():
            player_rows+=get_key(tok,game["box_score"]["SECOND_NAME"]) #get id
            tok = "*lastname*" #replace name
        if tok in game["box_score"]["FIRST_NAME"].values():
            tok = "*firsttname*" #replace name
        cur_sent.append(tok.lower())
        if tok == ".":
            found = 0
            for i,tok in enumerate(cur_sent): #loop back through sentence to find stats
                tok = alpha2digit(tok, "en") #convert number words to digits
                if tok.isnumeric(): #if number
                    if tok in game["box_score"]["PTS"].values():
                        for k in get_key(tok,game["box_score"]["PTS"]): #get ids
                            if k in player_rows: #match
                                tok = "*ptsval*"
                                found = 1
                                continue
                    if tok in game["box_score"]["AST"].values():
                        for k in get_key(tok,game["box_score"]["AST"]): #get ids
                            if k in player_rows: #match
                                tok = "*astval*"
                                found = 1
                                continue
                    if tok in game["box_score"]["REB"].values():
                        for k in get_key(tok,game["box_score"]["REB"]): #get ids
                            if k in player_rows: #match
                                tok = "*rebval*"
                                found = 1

                cur_sent[i] = tok #replace stat
            cur_sent.append("*end*")

            if found:
                new_sum.append(cur_sent) #only append if found a stat

            player_rows = []
            cur_sent = []

with open('tagged_summaries_no_names.txt','w') as fw:
   sum_json = json.dump(new_sum,fw)
