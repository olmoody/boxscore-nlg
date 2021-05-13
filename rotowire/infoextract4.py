import json
from text_to_num import alpha2digit

with open('train.json','r') as fr:
	d = fr.read()
	full_dict = json.loads(d)
	#print(d[0]["box_score"]["SECOND_NAME"].values())
game = full_dict[0]
#print(game["box_score"]["SECOND_NAME"],game["box_score"]["PTS"])
#print(game["summary"])
#for key in sorted([int(i) for i in game["box_score"]["PTS"].keys()]):
#    print(key)
def get_key(val,my_dict):
    keys = []
    for key, value in my_dict.items():
         if val == value:
             keys.append(key)

    return keys
new_sum = []
hi =0
for game in full_dict:
	#split summary into sentences
    old_sum = game["summary"]

	#[[w1,w2,w3,.,{player:pts,player:pts},{player:assists},{player:rebounds}],[]]
    player_rows,pts_rows = [],[]
    name,pts = "",0
    cur_sent = []
    for tok in old_sum:
        if tok in game["box_score"]["SECOND_NAME"].values():
            key = get_key(tok,game["box_score"]["SECOND_NAME"])
            player_rows+=key
            #tok = "*lastname{}*".format(key[0])
        if tok in game["box_score"]["FIRST_NAME"].values():
            key = get_key(tok,game["box_score"]["FIRST_NAME"])
            #tok = "*firstname{}*".format(key[0])
        cur_sent.append(tok.lower())
        if tok == ".":
            found = 0
            for i,tok in enumerate(cur_sent):
                tok = alpha2digit(tok, "en")
                if tok.isnumeric():
                    if tok in game["box_score"]["PTS"].values():
                        for k in get_key(tok,game["box_score"]["PTS"]):
                            if k in player_rows:
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
                #cur_sent[i] = tok
            cur_sent.append("*end*")
            cur_sent.append([game["box_score"]["PTS"][str(i)] if str(i) in game["box_score"]["PTS"].keys() else "*empty*" for i in range(26)])
            cur_sent.append([game["box_score"]["AST"][str(i)] if str(i) in game["box_score"]["AST"].keys() else "*empty*" for i in range(26)]) 
            cur_sent.append([game["box_score"]["REB"][str(i)] if str(i) in game["box_score"]["REB"].keys() else "*empty*" for i in range(26)])
            cur_sent.append([game["box_score"]["FIRST_NAME"][str(i)].lower() if str(i) in game["box_score"]["FIRST_NAME"].keys() else "*empty*" for i in range(26)])            
            cur_sent.append([game["box_score"]["SECOND_NAME"][str(i)].lower() if str(i) in game["box_score"]["SECOND_NAME"].keys() else "*empty*" for i in range(26)])


            if found:
                new_sum.append(cur_sent)
#            print(cur_sent)
#            print(player_rows)
            player_rows = []
            cur_sent = []
#print(game["box_score"]["PTS"]["20"],game["box_score"]["SECOND_NAME"]["20"],game["box_score"]["AST"]["20"])
#print(new_sum)
#print(hi)
with open('tagged_summaries_both.txt','w') as fw:
    sum_json = json.dump(new_sum,fw)

#[["All-Star", "*firsttname*", "*lastname*", "once", "again", "led", "Boston", "with", "*ptsval*", "points", ",", "while", "star", "center", "*firsttname*", "*lastname*", "scored", "*ptsval*", "points", "and", "stuffed", "the", "stat", "sheet", "with", "*rebval*", "rebounds", ",", "*astval*", "assists", ",", "*ptsval*", "steals", ",", "and", "*rebval*", "blocks", ".", "*end*"], ["Third-year", "point", "guard", "*firsttname*", "*lastname*", "impressed", "off", "the", "bench", ",", "dishing", "*astval*", "assists", "and", "scoring", "*ptsval*", "points", "including", "the", "game", "-", "winning", "3", "-", "pointer", ".", "*end*"], ["Sophomore", "big", "man", "*firsttname*", "*lastname*", "had", "*ptsval*", "points", "and", "*rebval*", "rebounds", "as", "well", "as", "4", "blocks", ".", "*end*"]]
#for each sentence
