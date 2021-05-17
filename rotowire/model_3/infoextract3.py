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

	#[[w1,w2,w3,.,[pts1,pt2],[ast1,ast2],[reb1,reb2]]
    player_rows = []
    cur_sent = []
    for tok in old_sum: #for each word in summary
        if tok in game["box_score"]["SECOND_NAME"].values():
            key = get_key(tok,game["box_score"]["SECOND_NAME"]) #get id
            player_rows+=key #save id
            tok = "*lastname{}*".format(key[0]) #replace name
        if tok in game["box_score"]["FIRST_NAME"].values():
            key = get_key(tok,game["box_score"]["FIRST_NAME"]) #get id
            tok = "*firstname{}*".format(key[0]) #replace name
        cur_sent.append(tok.lower())
        if tok == ".": #end of sentence
            found = 0
            for i,tok in enumerate(cur_sent): #loop back through sentence to find stats
                tok = alpha2digit(tok, "en") #convert number words to digits
                if tok.isnumeric(): #if number
                    if tok in game["box_score"]["PTS"].values():
                        for k in get_key(tok,game["box_score"]["PTS"]): #get ids
                            if k in player_rows: #match
                                tok = "*ptsval{}*".format(k)
                                found = 1
                                continue
                    if tok in game["box_score"]["AST"].values():
                        for k in get_key(tok,game["box_score"]["AST"]):
                            if k in player_rows:
                                tok = "*astval{}*".format(k)
                                found = 1
                                continue
                    if tok in game["box_score"]["REB"].values():
                        for k in get_key(tok,game["box_score"]["REB"]):
                            if k in player_rows:
                                tok = "*rebval{}*".format(k)
                                found = 1
                cur_sent[i] = tok #replace stat
			#append stat lists
            cur_sent.append([game["box_score"]["PTS"][str(i)] if str(i) in game["box_score"]["PTS"].keys() else "*empty*" for i in range(26)])
            cur_sent.append([game["box_score"]["AST"][str(i)] if str(i) in game["box_score"]["AST"].keys() else "*empty*" for i in range(26)])
            cur_sent.append([game["box_score"]["REB"][str(i)] if str(i) in game["box_score"]["REB"].keys() else "*empty*" for i in range(26)])
            cur_sent.append([game["box_score"]["FIRST_NAME"][str(i)].lower() if str(i) in game["box_score"]["FIRST_NAME"].keys() else "*empty*" for i in range(26)])
            cur_sent.append([game["box_score"]["SECOND_NAME"][str(i)].lower() if str(i) in game["box_score"]["SECOND_NAME"].keys() else "*empty*" for i in range(26)])

            if found:
                new_sum.append(cur_sent) #only append if found a stat

            player_rows = []
            cur_sent = []

with open('tagged_summaries_noname_dicts.txt','w') as fw:
   sum_json = json.dump(new_sum,fw)
