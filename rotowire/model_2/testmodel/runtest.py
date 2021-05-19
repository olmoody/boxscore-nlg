import json
import random

with open('stat_sentences_test.txt','r') as fr: #get real sentences
	d = fr.read()
	real = json.loads(d)

with open('../results.txt','r') as fr: #get generated sentences
	generated = fr.readlines()

#make both lowercase
real = [[i.lower() for i in sent] for sent in real]
generated = [i.lower().split() for i in generated]

#shuffle
random.shuffle(real)
random.shuffle(generated)

# print(real[:2],generated[:2])

correct = 0
for i in range(25): #do 25 trials
	sents = [" ".join(real[i]), " ".join(generated[i])] #join for readability
	#print(sents)
	real_ind = 1
	if random.randint(0,1)==1: # random order
		sents = sents[::-1]
		real_ind = 2
	print("1.",sents[0])
	print("2.",sents[1])
	s= input("{}. Guess the real sentence (1 or 2) ".format(i+1))
	if s==str(real_ind):
		correct+=1
	print()
print("You guessed",correct,"out of 25") #print results
