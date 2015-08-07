'''
Same as before just added some text so the user
knows what the script is doing.
'''

import textmining
import glob
import random


#reference file, note training set is enron1 folder
test = ['enron6', 'enron2', 'enron3', 'enron4', 'enron5']

folder = random.choice(test)

print 'Selecting random test folder'
print '%s folder was selected.' %(folder)

spam_call = folder + "/spam/*.txt"
ham_call = folder + "/ham/*.txt"
spam = glob.glob(spam_call)
ham = glob.glob(ham_call)


print 'Creating ham and spam files.'

tdm = textmining.TermDocumentMatrix()
tdm1 = textmining.TermDocumentMatrix()

for item in spam[0:120]:
	f = open(item)
	words = f.read()
	tdm.add_doc(words)
tdm.write_csv('spam_test.csv', cutoff=2)


for item1 in ham[0:294]:
	f = open(item1)
	words = f.read()
	tdm1.add_doc(words)
tdm1.write_csv('ham_test.csv', cutoff = 2)



