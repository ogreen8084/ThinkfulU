
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
import numpy as np

sale_data = pd.read_csv('sale_data_knn.csv')


#split data and set up independent and depe
saleTrain, saleTest = train_test_split(sale_data, test_size = 0.2)

saleTrain_ind = saleTrain.drop(['SALE_PRICE'], axis = 1)
saleTrain_dep = saleTrain['SALE_PRICE']

saleTest_ind = saleTest.drop(['SALE_PRICE'], axis = 1)
saleTest_dep = saleTest['SALE_PRICE']

#k-nn classification by k, 1-20
predict_value = 1.0
k_value = 1
for k in range(1,20):
	model = KNeighborsClassifier(n_neighbors=k)
	model.fit(saleTrain_ind, saleTrain_dep)

	expected = saleTest_dep
	predicted = model.predict(saleTest_ind)

	error_rate = (predicted != expected).mean()
	print '\nK is: %s error rate is: %.2f' %(k, error_rate)
	if error_rate < predict_value:
		predict_value = error_rate
		k_value = k

print '\nThe optimal k-value was: %s ' %(k_value)
print 'The error rate was %.2f '  %(predict_value)


#bonus, K-means analysis
model2 = KMeans(n_clusters=10, init='k-means++', n_init=10,
	max_iter=300, tol=0.0001, precompute_distances=True, verbose=0, random_state=None, copy_x=True, n_jobs=1)
model2.fit(np.asmatrix(saleTrain_ind))

print model2.predict(np.asmatrix(saleTest_ind))

print '\nThe K-Means cluster centers are as follows:'
print list(saleTest_ind.columns.values)
print model2.cluster_centers_