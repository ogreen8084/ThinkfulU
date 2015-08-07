import textmining
import glob


'''
Same as before just added text letting user know
what the file is doing.
'''


spam_call = "enron1/spam/*.txt"
ham_call = "enron1/ham/*.txt"
spam = glob.glob(spam_call)
ham = glob.glob(ham_call)



tdm = textmining.TermDocumentMatrix()
tdm1 = textmining.TermDocumentMatrix()

print 'Making spam and ham csv for enron1 folder'

for item in spam[0:120]:
	f = open(item)
	words = f.read()
	tdm.add_doc(words)
tdm.write_csv('spam.csv', cutoff=2)


for item1 in ham[0:294]:
	f = open(item1)
	words = f.read()
	tdm1.add_doc(words)
tdm1.write_csv('ham.csv', cutoff = 2)



