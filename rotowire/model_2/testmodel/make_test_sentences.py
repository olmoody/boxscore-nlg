import json
with open('../../model_1/tagged_test_summaries.txt','r') as fr:
        d = fr.read()
        full_dict = json.loads(d)

stat_sums = []
for s in full_dict:
    if s[-3] or s[-2] or s[-1]:
        stat_sums.append(s[:-3])

with open('stat_sentences_test.txt','w') as fw: 
	sum_json = json.dump(stat_sums,fw)
