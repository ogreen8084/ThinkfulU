import pandas as pd
import numpy as np
import math

#read dataframes
spam_df = pd.read_csv('spam.csv', header = 0)
ham_df = pd.read_csv('ham.csv', header = 0)

#delete subject from dataframes, in every e-mail
spam_df = spam_df.drop('subject', axis = 1)
ham_df = ham_df.drop('subject', axis = 1)


#create dictionary of word counts to do calculations
spam_dict = {}
for item5 in spam_df.columns:
	spam_dict[item5] =float(spam_df[item5].sum())

ham_dict = {}
for item6 in ham_df.columns:
	ham_dict[item6] =float(ham_df[item6].sum())


#create dictionary to hold probability that each word is spam
spam_prob = {}
for key, value in spam_dict.iteritems():
	if key in ham_dict:
		spam_prob[key] = (value/(value + ham_dict[key]))
	else:
		spam_prob[key] = 1.0
'''		
#create dictionary to hold probability that each word is ham, not needed
ham_prob = {}
for key, value in ham_dict.iteritems():
	if key in spam_dict:
		ham_prob[key] =  (value/(value + spam_dict[key]))
	else:
		ham_prob[key] = 1.0
'''

#convert dataframes to binary, is word in e-mail or not
ham_df[ham_df >1] = 1
spam_df[spam_df > 1] = 1


'''
For each column(word), if the item is in spam e-mails, convert to the log of the probability.
If not, since 1/0 is undefined, just make the term -7 of which the antilog is equivalent to 
about a probability of .001.
'''
for item in ham_df.columns:
	if item in spam_df.columns:
		ham_df[item] = ham_df[item].replace([0, 1], [np.log(1-spam_prob[item]), np.log(spam_prob[item]/(1-spam_prob[item])) + np.log(1-spam_prob[item])])
	else:
		ham_df[item] = ham_df[item].replace([0, 1], [0, -7])

for item in spam_df.columns:
	if item in ham_df.columns:
		spam_df[item] = spam_df[item].replace([0, 1], [np.log(1-spam_prob[item]), np.log(spam_prob[item]/(1-spam_prob[item])) + np.log(1-spam_prob[item])])
	else:
		spam_df[item] = spam_df[item].replace([0, 1], [0, 0])

#add up log probabilities
spam_df['score'] = spam_df.sum(axis=1)

ham_df['score'] = ham_df.sum(axis=1)

#convert back to regular probability
ham_df['prob_spam'] = 2.71828
ham_df['prob_spam'] = ham_df['prob_spam'].pow(ham_df['score'])
spam_df['prob_spam'] = 2.71828
spam_df['prob_spam'] = spam_df['prob_spam'].pow(spam_df['score'])

print 'Description of the probability of ham e-mails being spam.'
print ham_df['prob_spam'].describe()
print 'Description of the probability of spam e-mails being spam.'
print spam_df['prob_spam'].describe()

print "There is a clear difference between the probability of a Ham e-mail being ham"
print "and a spam e-mail being spam."







