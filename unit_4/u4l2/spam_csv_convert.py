import textmining
import glob


spam = glob.glob("enron1/spam/*.txt")
ham = glob.glob("enron1/ham/*.txt")



tdm = textmining.TermDocumentMatrix()
tdm1 = textmining.TermDocumentMatrix()

for item in spam[0:100]:
	f = open(item)
	words = f.read()
	tdm.add_doc(words)
tdm.write_csv('spam.csv', cutoff=2)


for item1 in ham[0:100]:
	f = open(item1)
	words = f.read()
	tdm1.add_doc(words)
tdm1.write_csv('ham.csv', cutoff = 2)



