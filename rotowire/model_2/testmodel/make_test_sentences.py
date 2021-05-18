import json
with open('../../model_1/tagged_test_summaries.txt','r') as fr: #get tagged summaries
        d = fr.read()
        full_dict = json.loads(d)

stat_sums = []
for s in full_dict:
    if s[-3] or s[-2] or s[-1]: #if they have a stat
        stat_sums.append(s[:-3]) #include without dict

with open('stat_sentences_test.txt','w') as fw: #dump
	sum_json = json.dump(stat_sums,fw)
