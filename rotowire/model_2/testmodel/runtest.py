import json
import random

with open('stat_sentences_test.txt','r') as fr:
	d = fr.read()
	real = json.loads(d)

with open('../results.txt','r') as fr:
	generated = fr.readlines()
real = [[i.lower() for i in sent] for sent in real]
generated = [i.lower().split() for i in generated]

random.shuffle(real)
random.shuffle(generated)

# print(real[:2],generated[:2])
correct = 0
for i in range(25):
	sents = [" ".join(real[i]), " ".join(generated[i])]
	#print(sents)
	real_ind = 1
	if random.randint(0,1)==1:
		sents = sents[::-1]
		real_ind = 2
	print(sents)
	s= input("{}. Guess the real sentence (1 or 2) ".format(i+1))
	if s==str(real_ind):
		correct+=1
print("You guessed",correct,"out of 25")
