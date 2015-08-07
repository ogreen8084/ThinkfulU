import pandas as pd
import numpy as np

import pandas as pd
import numpy as np

'''
read dataframes need two sets because one set will be ham probability
format actualvalue_assumed value as, so spam is actual
spam labeled as spam and so on,loaded twice because they were attached in memory
'''
spam = pd.read_csv('spam_test.csv', header = 0)
ham = pd.read_csv('ham_test.csv', header = 0)

#delete subject from dataframes, in every e-mail
spam = spam.drop('subject', axis = 1)
ham = ham.drop('subject', axis = 1)

#hardcoded probability for a ham vs a spam e-mail
ham_ratio = .71
spam_ratio = .29


#convert dataframes to binary, is word in e-mail or not
ham[ham >1] = 1
spam[spam > 1] = 1





#copy file to make calculations
ham_copy = ham.copy()
spam_copy = spam.copy()

#alter as needed to load different probability file sets
spam_file = 'spam_probability_laplace.csv'
ham_file = 'ham_probability_laplace.csv'


#needed to calculate error rate, number of ham and spam e-mails in set
num_spam = len(list(spam_copy.index))
num_ham = len(list(ham_copy.index))

#import probability of spam and ham from training set
spam_prob = pd.read_csv(spam_file)
ham_prob = pd.read_csv(ham_file)


#manipulate to be able to pull values
spam_prob = spam_prob.set_index(spam_prob['Unnamed: 0'], drop = True)
ham_prob = ham_prob.set_index(spam_prob['Unnamed: 0'], drop = True)

spam_prob = spam_prob.drop('Unnamed: 0', axis = 1)
ham_prob = ham_prob.drop('Unnamed: 0', axis = 1)


spam_prob = spam_prob.transpose()
ham_prob = ham_prob.transpose()

print 'The original number of spam words is: %d'  %(len(spam.columns.values))
print 'The original number of ham words is: %d' %(len(ham.columns.values))


#only include words in training set to determine probability
print '-'*50
print 'Proceed with creating the intersection of spam and ham.'
word_intersection = sorted(list(set(spam) & set(ham) &set(spam_prob)))
ham = ham.reindex(columns = word_intersection)
spam = spam.reindex(columns = word_intersection)


print 'The intersection of spam and ham is %d words.' %(len(spam.columns.values))



'''
formula is x*np.log((prob(spam_or_ham)/(1-prob(spam_or_ham)))) + np.log(1-prob(spam_or_ham))
if x = 0, then formula is simply np.log(1-prob(spam_or_ham))
instead of using multiple loops, since all words are in each data frame we use one loop.

'''
for item in list(spam.columns):
		spam[item] = spam[item].replace([0, 1], [np.log(1-float(spam_prob[item])), np.log(float(spam_prob[item])/(1-float(spam_prob[item])))+np.log(1-float(spam_prob[item]))])
		ham[item] = ham[item].replace([0, 1], [np.log(1-float(spam_prob[item])), np.log(float(spam_prob[item])/(1-float(spam_prob[item])))+np.log(1-float(spam_prob[item]))])
		spam_copy[item] = spam_copy[item].replace([0, 1], [np.log(1-float(ham_prob[item])), np.log(float(ham_prob[item])/(1-float(ham_prob[item])))+np.log(1-float(ham_prob[item]))])
		ham_copy[item] = ham_copy[item].replace([0, 1], [np.log(1-float(ham_prob[item])), np.log(float(ham_prob[item])/(1-float(ham_prob[item])))+np.log(1-float(ham_prob[item]))])

#prob_item = e^(sum of log probablity)
spam['spam_prob'] = np.exp(spam.sum(axis=1))
spam_copy['ham_prob'] = np.exp(spam_copy.sum(axis=1))
ham['spam_prob'] = np.exp(ham.sum(axis=1))
ham_copy['ham_prob'] = np.exp(ham_copy.sum(axis=1))



#bayesian probability of each item respectively
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
print 'Error rate is %.3f' %(float(spam_detected)/num_spam)

print '-'*50
print 'Results on the ham training set'
spam_detected2 = 0
for item in ham['probability_spam'].index:
	if ham['probability_spam'].ix[item] > ham_copy['probability_ham'].ix[item]:
		spam_detected2 +=1
print 'Detected %d spams in a set of %d ham e-mails' %(spam_detected2, int(num_ham))
print 'Error rate is %.3f' %(float(spam_detected2)/num_ham)




