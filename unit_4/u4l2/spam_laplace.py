import pandas as pd
import numpy as np
import math

'''
read dataframes need two sets because one set will be ham probability
format actualvalue_assumed value as, so spam is actual
spam labeled as spam and so on,loaded twice because they were attached in memory
'''
spam = pd.read_csv('spam.csv', header = 0)
ham = pd.read_csv('ham.csv', header = 0)

#delete subject from dataframes, in every e-mail
spam = spam.drop('subject', axis = 1)
ham = ham.drop('subject', axis = 1)


print 'The original number of spam words is: %d'  %(len(spam.columns.values))
print 'The original number of ham words is: %d' %(len(ham.columns.values))

#convert dataframes to binary, is word in e-mail or not
ham[ham >1] = 1
spam[spam > 1] = 1


print '-'*50
print 'Proceed with creating the intersection of spam and ham.'
word_intersection = sorted(list(set(spam) | set(ham)))
ham = ham.reindex(columns = word_intersection, fill_value = 0)
spam = spam.reindex(columns = word_intersection, fill_value = 0)


print 'The union of spam and ham is %d words.' %(len(spam.columns.values))


ham_copy = ham.copy()
spam_copy = spam.copy()



num_spam = len(list(spam_copy.index))
num_ham = len(list(ham_copy.index))
spam_ratio = float(num_spam)/(num_ham + num_spam)
ham_ratio = float(num_ham)/(num_ham + num_spam)



#create dictionary of word counts to do calculations
spam_count = spam.sum( axis = 0)
ham_count = ham.sum(axis = 0)

cond_prob_spam = spam_count/num_spam
cond_prob_ham = ham_count/num_ham

#create dictionary to hold probability that each word is spam
#number of times word is in spam/ total times word is in spam + ham

alpha = 1
beta = 2
spam_prob= (spam_count+ alpha)/(spam_count + ham_count + beta)
ham_prob = 1-spam_prob


spam_prob = cond_prob_spam*spam_prob
ham_prob = cond_prob_ham*ham_prob

spam_prob = spam_prob.transpose()
ham_prob = ham_prob.transpose()
spam_prob.to_csv('spam_probability_laplace.csv', header = ['probability'])
ham_prob.to_csv('ham_probability_laplace.csv', header = ['probability'])


for item in spam.columns:
	spam[item] = spam[item].replace([0, 1], [np.log(1-spam_prob[item]), np.log(spam_prob[item]/(1-spam_prob[item]))+np.log(1-spam_prob[item])])
	ham[item] = ham[item].replace([0, 1], [np.log(1-spam_prob[item]), np.log(spam_prob[item]/(1-spam_prob[item]))+np.log(1-spam_prob[item])])
	spam_copy[item] = spam_copy[item].replace([0, 1], [np.log(1-ham_prob[item]), np.log(ham_prob[item]/(1-ham_prob[item]))+np.log(1-ham_prob[item])])
	ham_copy[item] = ham_copy[item].replace([0, 1], [np.log(1-ham_prob[item]), np.log(ham_prob[item]/(1-ham_prob[item]))+np.log(1-ham_prob[item])])



spam['spam_prob'] = np.exp(spam.sum(axis=1))
spam_copy['ham_prob'] = np.exp(spam_copy.sum(axis=1))
ham['spam_prob'] = np.exp(ham.sum(axis=1))
ham_copy['ham_prob'] = np.exp(ham_copy.sum(axis=1))




spam['probability_spam'] = (spam['spam_prob']*spam_ratio)/(spam['spam_prob']*spam_ratio + spam_copy['ham_prob']*ham_ratio)
spam_copy['probability_ham']  =  (spam_copy['ham_prob']*ham_ratio)/(spam['spam_prob']*spam_ratio + spam_copy['ham_prob']*ham_ratio)

ham['probability_spam'] = (ham['spam_prob']*spam_ratio)/(ham['spam_prob']*spam_ratio + ham_copy['ham_prob']*ham_ratio)
ham_copy['probability_ham']  =  (ham_copy['ham_prob']*ham_ratio)/(ham['spam_prob']*spam_ratio + ham_copy['ham_prob']*ham_ratio)

print '-'*50
print '-'*50
spam_detected = 0
print 'Results on the spam training set:'
for item in spam['probability_spam'].index:
	if spam['probability_spam'].ix[item] > spam_copy['probability_ham'].ix[item]:
		spam_detected +=1
print 'Detected %d spams in a set of %d spam e-mails' %(spam_detected, int(num_spam))
print 'Error rate is %.2f' %(float(1-(spam_detected/float(num_spam))))

print '-'*50
print 'Results on the ham training set'
spam_detected2 = 0
for item in ham['probability_spam'].index:
	if ham['probability_spam'].ix[item] > ham_copy['probability_ham'].ix[item]:
		spam_detected2 +=1
print 'Detected %d spams in a set of %d ham e-mails' %(spam_detected2, int(num_ham))
print 'Error rate is %.2f' %(float(spam_detected2/float(num_ham)))




