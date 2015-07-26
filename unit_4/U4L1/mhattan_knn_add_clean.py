import pandas as pd
sale_data = pd.read_csv('sale_data.csv')

#pull building class info for category purposes
bld_class_new = []
for item in sale_data['BLD_CLASS']:
	bld_class_new.append(int(item[0:2]))
sale_data['BLD_CLASS'] = bld_class_new

#put sale price into ranges
sale_new = []
for item1 in sale_data['SALE_PRICE']:
	if item1 < 250001:
		sale_new.append(250000)
	elif item1 < 500001:
		sale_new.append(500000)
	elif item1 < 750001:
		sale_new.append(750000)
	elif item1 < 1000001:
		sale_new.append(1000000)
	elif item1 < 1500001:
		sale_new.append(1500000)
	elif item1 < 2250001:
		sale_new.append(2250000)
	elif item1 < 3000001:
		sale_new.append(3000000)
	elif item1 < 50000001:
		sale_new.append(5000000)
	elif item1 < 10000001:
		sale_new.append(10000000)
	else:
		sale_new.append(20000000)

sale_data['SALE_PRICE'] = sale_new

#alter tax class for category purposes
txcl_new = []
for item in sale_data['TXCL_NOW']:
	if len(item) == 1:
		txcl_new.append(int(item) * 10)
	elif len(item) == 2 and item[1] == 'C':
		txcl_new.append(int(item[0]) * 10 + 7)
	elif len(item) == 2 and item[1] == 'B':
		txcl_new.append(int(item[0]) * 10 + 4)
	elif len(item) == 2 and item[1] == 'A':
		txcl_new.append(int(item[0]) * 10 + 2)
	else:
		print 'Houston we have a problem'

sale_data['TXCL_NOW'] = txcl_new

sale_data.to_csv('sale_data_knn.csv', header = True)

