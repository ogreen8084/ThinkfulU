import pandas as pd
import numpy as np

#read dataframes need two because one set will be ham probability
#actual_label, so spam_spam is actual spam labeled as spam and so on
spam_spam = pd.read_csv('spam.csv', header = 0)
ham_spam = pd.read_csv('ham.csv', header = 0)
ham_ham = pd.read_csv('ham.csv', header = 0)
spam_ham = pd.read_csv('spam.csv', header = 0)


#delete subject from dataframes, in every e-mail
spam_spam = spam_spam.drop('subject', axis = 1)
ham_spam = ham_spam.drop('subject', axis = 1)
ham_ham = ham_ham.drop('subject', axis = 1)
spam_ham = spam_ham.drop('subject', axis = 1)



#create dictionary of word counts to do calculations
spam_dict = {}
for item5 in spam_spam.columns:
	spam_dict[item5] =float(spam_spam[item5].sum())

ham_dict = {}
for item6 in ham_spam.columns:
	ham_dict[item6] =float(ham_spam[item6].sum())


#create dictionary to hold probability that each word is spam
#number of times word is in spam/ total times word is in spam + ham
spam_prob = {}
for key, value in spam_dict.iteritems():
	if key in ham_dict:
		spam_prob[key] = (value/(value + ham_dict[key]))
	else:
		spam_prob[key] = 1.0
		
#create dictionary to hold probability that each word is ham, not needed
ham_prob = {}
for key, value in ham_dict.iteritems():
	if key in spam_dict:
		ham_prob[key] =  (value/(value + spam_dict[key]))
	else:
		ham_prob[key] = 1.0



#convert dataframes to binary, is word in e-mail or not
ham_spam[ham_spam >1] = 1
spam_spam[spam_spam > 1] = 1
spam_ham[spam_ham > 1] = 1
ham_ham[ham_ham > 1] = 1


'''
Pseudocode behind these for loops: 
If the word is in ham but not in spam or vice versa, assume that means there is a .001 probability
that the word would be in a spam e-mail and so on. e^-7 = .001 (approximately).
This eliminates division by zero error.  

'''


for item in ham_spam.columns:
	if item in spam_spam.columns:
		ham_spam[item] = ham_spam[item].replace([0, 1], [np.log(spam_prob[item]), 
			np.log((1-spam_prob[item])/(spam_prob[item])) + np.log(spam_prob[item])])
	else:
		ham_spam[item] = ham_spam[item].replace([0, 1], [0, np.log(ham_prob[item])])


for item in spam_spam.columns:
	if item in ham_spam.columns:
		spam_spam[item] = spam_spam[item].replace([0, 1], [np.log(1-spam_prob[item]), 
			np.log(spam_prob[item]/(1-spam_prob[item])) + np.log(1-spam_prob[item])])
	else:
		spam_spam[item] = spam_spam[item].replace([0, 1], [0, 0])



for item in ham_ham.columns:
	if item in spam_spam.columns:
		ham_ham[item] = ham_ham[item].replace([0, 1], [np.log(1-ham_prob[item]), 
			np.log(ham_prob[item]/(1-ham_prob[item])) + np.log(1-ham_prob[item])])
	else:
		ham_ham[item] = ham_ham[item].replace([0, 1], [0, 0])

for item in spam_ham.columns:
	if item in ham_spam.columns:
		spam_ham[item] = spam_ham[item].replace([0, 1], [np.log(1-ham_prob[item]), 
			np.log(ham_prob[item]/(1-ham_prob[item])) + np.log(1-ham_prob[item])])
	else:
		spam_ham[item] = spam_ham[item].replace([0, 1], [0, 0])


#sum log probabilities
#log(p(x|c)) = sum(x*wj +wo)
ham_ham['score'] = ham_ham.sum(axis=1)
spam_ham['score'] = spam_ham.sum(axis=1)
spam_spam['score'] = spam_spam.sum(axis=1)
ham_spam['score'] = ham_spam.sum(axis=1)



#now that log probs calculated convert back to regular probability using the exponential
#formula x = e^(log(x))
ham_spam['prob_spam'] = 2.71828
ham_spam['prob_spam'] = ham_spam['prob_spam'].pow(ham_spam['score'])


spam_spam['prob_spam'] = 2.71828
spam_spam['prob_spam'] = spam_spam['prob_spam'].pow(spam_spam['score'])

spam_ham['prob_ham'] = 2.71828
spam_ham['prob_ham'] = spam_ham['prob_ham'].pow(spam_ham['score'])

ham_ham['prob_ham'] = 2.71828
ham_ham['prob_ham'] = ham_ham['prob_ham'].pow(ham_ham['score'])



#convert p(x|c) to p(c|x), p(c|x) = p(x|c)*p(c)/p(x) 
ham_ham['final_prob_ham'] = (ham_ham['prob_ham']*.71)/(ham_ham['prob_ham']*.71 + ham_spam['prob_spam']*.29)

spam_ham['final_prob_ham'] = (spam_ham['prob_ham']*.71)/(spam_ham['prob_ham']*.71 + spam_spam['prob_spam']*.29)

spam_spam['final_prob_spam'] = (spam_spam['prob_spam']*.29)/(spam_spam['prob_spam']*.29 + spam_ham['prob_ham']*.71)

ham_spam['final_prob_spam'] = (ham_spam['prob_spam']*.29)/(ham_spam['prob_spam']*.29 +ham_ham['prob_ham']*.71)


#print statistics
print 'Description of the probability of ham e-mails being spam.'
print ham_spam['final_prob_spam'].describe()
print '\nDescription of the probability of spam e-mails being spam.'
print spam_spam['final_prob_spam'].describe()
print '\nDescription of the probability of ham e-mail being ham'
print ham_ham['final_prob_ham'].describe()
print '\nDescription of the probability of spam e-mail being ham'
print spam_ham['final_prob_ham'].describe()

#threshold is 50% probability, tweak as needed
spam_spam_counter = 0.0
for item in spam_spam['final_prob_spam']:
	if item < .5:
		spam_spam_counter +=1.0
spam_spam_ratio = (spam_spam['final_prob_spam'].count() -spam_spam_counter)/spam_spam['final_prob_spam'].count()
print '\nThe probability of a spam e-mail being labeled as spam is %.2f' %(spam_spam_ratio*100)

'''
technically don't need but helps check that the math is 
right since percentages add to 1 and they are separate
'''
spam_ham_counter = 0.0
for item in spam_ham['final_prob_ham']:
	if item < .5:
		spam_ham_counter +=1.0
spam_ham_ratio = (spam_ham['final_prob_ham'].count() -spam_ham_counter)/spam_ham['final_prob_ham'].count()
print '\nThe probability of a spam e-mail being labeled as ham is %.2f' %(spam_ham_ratio*100)



ham_ham_counter = 0.0
for item in ham_ham['final_prob_ham']:
	if item < .5:
		ham_ham_counter +=1.0
ham_ham_ratio = (ham_ham['final_prob_ham'].count() -ham_ham_counter)/ham_ham['final_prob_ham'].count()
print '\nThe probability of a ham e-mail being labeled as ham is %.2f' %(ham_ham_ratio*100)


'''
technically don't need but helps check that the math is 
right since percentages add to 1 and they are separate
'''
ham_spam_counter = 0.0
for item in ham_spam['final_prob_spam']:
	if item < .5:
		ham_spam_counter +=1.0
ham_spam_ratio = (ham_spam['final_prob_spam'].count() -ham_spam_counter)/ham_spam['final_prob_spam'].count()
print '\nThe probability of a ham e-mail being labeled as spam is %.2f' %(ham_spam_ratio*100)



