from markov import *
from sklearn import preprocessing
from keras.models import Sequential
from keras.layers import Input, Dense
from keras.models import Model
import numpy as np
import csv
import scipy
from scipy import stats
from random import random
import math
from pylab import *
import pandas
from datetime import datetime

def autoencode(k,no_time,Traindataset,Testdataset):

    seed = 6
    np.random.seed(seed)

    I=Traindataset[:,k:k+no_time]
    T=Testdataset[:,k:k+no_time]

    I_check=Traindataset[:,k:k+no_time+ no_time + no_time + 1]
    T_check=Testdataset[:,k:k+no_time + no_time + no_time + 1]

    I_N=preprocessing.normalize(I, norm='l2',axis=0) #Normalizes the given training data


    T_N=preprocessing.normalize(T, norm='l2',axis=0) #Normalizes the given test data

    encoding_dim = 250
    input_data=Input(shape=(no_time,))  #doubt what does this do

    encoded = Dense(encoding_dim, activation='relu')(input_data) #relu stands for rectified linear unit f(x) = max(x,0)
    decoded = Dense(no_time, activation='relu')(encoded)

    autoencoder = Model(input=input_data, output=decoded)
    """Encoder"""
    encoder = Model(input=input_data, output=encoded)

    """Decoder"""
    encoded_input = Input(shape=(encoding_dim,))
    decoder_layer = autoencoder.layers[-1]


    decoder = Model(input=encoded_input, output=decoder_layer(encoded_input))
    I = I.reshape((len(I), np.prod(I.shape[1:])))
    T = T.reshape((len(T), np.prod(T.shape[1:])))

    autoencoder.compile(optimizer='adam', loss='mean_squared_error',metrics=['accuracy'])
    autoencoder.fit(I_N,I_N,
                    nb_epoch= 50,
                    batch_size=2000,
                    shuffle=False,
                    validation_data=(T_N,T_N))

    encoded_data = encoder.predict(T_N)
    decoded_data = decoder.predict(encoded_data)
    print("\n")
    scores = autoencoder.evaluate(I_N, I_N)
    scores2 = autoencoder.evaluate(T_N, T_N)


    #print("Train %s: %.2f%%" % (autoencoder.metrics_names[1], scores[1]*100))
    print("\n")
    #print("Test %s: %.2f%%" % (autoencoder.metrics_names[1], scores2[1]*100))

    fl = open('AutoOutput.csv', 'w')
    writer = csv.writer(fl)

    for values in decoded_data:
        writer.writerow(values)
    fl.close()
    f2 = open('AutoInput.csv', 'w')
    writer = csv.writer(f2)

    for values in T_N:
        writer.writerow(values)
    f2.close()

    #Calculation of reconstruction error

    c = len(decoded_data[0])
    r = len(decoded_data)

    #print("The value of r is", r)

    temp = list()
    #Computing the difference of original and decoded data

    for i in range(0 , r):
    	temp.append(decoded_data[i] - T_N[i])

    final_ans = list()
    x = 0.0

    #Computing the sum of square of errors
    for i in range(0 , r):
    	for j in range(0, c):
    		x = x + temp[i][j]*temp[i][j]
    	final_ans.append(x)
    	x = 0.0

    index = list()
    for i in range(0, r):
       index.append(i)

    temporary = 0.0
    temp_index = 0

    #Sorting final_ans array and index array
    for i in range(0, r):
    	for j in range(0,r):

    		if(final_ans[i]<final_ans[j]):
    			temporary = final_ans[i]
    			final_ans[i] = final_ans[j]
    			final_ans[j] = temporary

    			temp_index = index[i]
    			index[i] = index[j]
    			index[j] = temp_index

    n = 30
    actual_recon = list()


    #Instantiating actual_index with those stocks that contain values and figures (-999 indicates no data present)

    for i in range(0, r):
    	flag = 0
    	for j in range(0,2*c + 1):
    		if(I_check[index[i]][j] == -999):
    			flag = 1
    			break;
    	if(flag == 0):
    		actual_recon.append(index[i])
    """
    print("The following are the stocks with least reconstruction error before removal\n")
    for i in range(0,n):
    	print(index[i]+2)

    print("The following are the stocks with least reconstruction error after removal\n")

    for i in range(0,n):
    	print(actual_recon[i]+2)
	"""
    actual_random = list()
    i = 0
    x = 0
    l = 0
    rand_iters = 0
    tried = list()
    seed(datetime.now())
    #Choosing stocks randomly that contain data for the said period
    while i<n-1:
        """
        print("try:" + str(rand_iters))
        print(i)
        x = randint(0,r-1)
        flag = 0
        if (x not in actual_random) and (x not in actual_recon):
        	for j in range(0,2*c):
        		if(I_check[x][j] == -999):
        			flag = 1
        			break;
        	if(flag == 0):
        		actual_random.append(x)
        		i = i + 1
        rand_iters = rand_iters + 1
        """
        x = randint(0,r-1)
        if x not in tried:
        	flag = 0
        	tried.append(x)
        	for i in range(0,len(actual_random)):
        		if(actual_random[i] == x):
        			flag = 1
        			break
        	for j in range(0,2*c + 1):
        		if(I_check[x][j] == -999):
        			flag = 1
        			break;
        	if(flag == 0):
        		actual_random.append(x)
        		i = i + 1
    print(actual_random)

    """
    print("The randomly selected stocks are:\n")

    for i in range(0,len(actual_random)):
    	print(actual_random[i]+2)
    """
    return actual_recon[0:n], actual_random[0:n]

# end of main function
