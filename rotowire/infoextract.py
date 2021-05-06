import json
from text_to_num import alpha2digit

with open('train.json','r') as fr:
	d = fr.read()
	full_dict = json.loads(d)
	#print(d[0]["box_score"]["SECOND_NAME"].values())
game = full_dict[0]
#print(game["box_score"]["SECOND_NAME"],game["box_score"]["PTS"])
#print(game["summary"])
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
		tok = alpha2digit(tok, "en")
		if tok in game["box_score"]["SECOND_NAME"].values():
			name = tok
			player_rows+=get_key(name,game["box_score"]["SECOND_NAME"])
		elif tok.isnumeric():
			if tok in game["box_score"]["PTS"].values():
				pts = tok
				pts_rows += get_key(pts,game["box_score"]["PTS"])
			if tok in game["box_score"]["AST"].values():
	                        ast = tok
	                        ast_rows += get_key(ast,game["box_score"]["AST"])
			if tok in game["box_score"]["REB"].values():
	                        reb = tok
	                        reb_rows += get_key(pts,game["box_score"]["REB"])
		cur_sent.append(tok)
		if tok == ".":
			pts_dict = {}
			ast_dict = {}
			reb_dict = {}
			for player in player_rows:
				for pts in pts_rows:
					if player==pts:
						#print(game["box_score"]["SECOND_NAME"][player],game["box_score"]["PTS"][pts])
						pts_dict[game["box_score"]["SECOND_NAME"][player]]=game["box_score"]["PTS"][pts]
				for ast in ast_rows:
					if player==ast:
						ast_dict[game["box_score"]["SECOND_NAME"][player]]=game["box_score"]["AST"][ast]
				for reb in reb_rows:
	                                if player==reb:
	                                        reb_dict[game["box_score"]["SECOND_NAME"][player]]=game["box_score"]["REB"][reb]
			cur_sent.append(pts_dict)
			cur_sent.append(ast_dict)
			cur_sent.append(reb_dict)
			player_rows,pts_rows,ast_rows,reb_rows = [],[],[],[]
			new_sum.append(cur_sent)
			hi = max(len(cur_sent),hi)
			cur_sent = []
#print(new_sum[0])
print(hi)
# with open('tagged_summaries.txt','w') as fw:
# 	sum_json = json.dump(new_sum,fw)
	#fw.write(sum_json)

#for each sentence
