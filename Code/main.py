from create_markov import *
from graph import *
from statistics import *
from sklearn import preprocessing
import numpy as np
import csv
import scipy
from scipy import stats
from random import random
import math
from pylab import *
import pandas

#This code is for looking into whether autoencoding or other dimensionality reducing techniques can help improve the
#results from Markovitz theoram

#This is the main file that needs to be called for the code to work

Traindataset = np.loadtxt("New_data_send.csv", delimiter=",")
Testdataset = np.loadtxt("New_data_send.csv", delimiter=",")


no_time = 120 #This is the no. of monthes (time interval) the data is to be run for

random_data, reconstructed_data = create_markovitz_portfolios(no_time,Traindataset,Testdataset) #returns the random and reconstructed data

#mus is an array of the expected rates of return we are supposed to calculate the markovitz portfolio for
mus = [(t*0.001) for t in range(10,20)]

recon_statistics = list()
recon_stat_row = list()

random_statistics = list()
random_stat_row = list()


#Used for calculation of the median
recon_sort = list()
random_sort = list()

#for each expected rate of return , we compare the reconstructed_portfolio and the randomly picked portfolio

for i in range(0, len(mus)):
	if(calculate_LSE(reconstructed_data[i],mus[i])>calculate_LSE(random_data[i],mus[i])):
		print("Random portfilio is better for target rate", mus[i], "\n")
	else:
		print("Reconstructed portfolio is better for target rate", mus[i] ,"\n")

	if(calculate_sd(reconstructed_data[i])>calculate_sd(random_data[i])):
		print("Random portfilio has lower risk (standard deviation) target rate", mus[i], "\n")
	else:
		print("Reconstructed portfolio has lower risk(standard deviation) for target rate", mus[i] ,"\n")

	#We calculate the statistics for the reconstructed_portfolio and the randomly picked portfolio

	for j in range(0, len(reconstructed_data[i])):
		recon_sort.append(reconstructed_data[i][j])

	for j in range(0, len(random_data[i])):
		random_sort.append(random_data[i][j])

	index_value = int(len(recon_sort)/2)

	recon_sort.sort()

	random_sort.sort()


	print("The mean, sd ,lse and median for the reconstructed stock portfolio is:", calculate_mean(reconstructed_data[i]), calculate_sd(reconstructed_data[i]), calculate_LSE(reconstructed_data[i],mus[i]),recon_sort[index_value])

	recon_stat_row = list()
	recon_stat_row.append(calculate_mean(reconstructed_data[i]))
	recon_stat_row.append(calculate_sd(reconstructed_data[i]))
	recon_stat_row.append(calculate_LSE(reconstructed_data[i],mus[i]))
	recon_stat_row.append(recon_sort[index_value])

	recon_statistics.append(recon_stat_row)

	print("The mean, sd ,lse and median value for the random stock portfolio is:", calculate_mean(random_data[i]), calculate_sd(random_data[i]), calculate_LSE(random_data[i],mus[i]), recon_sort[index_value])

	random_stat_row = list()
	random_stat_row.append(calculate_mean(random_data[i]))
	random_stat_row.append(calculate_sd(random_data[i]))
	random_stat_row.append(calculate_LSE(random_data[i],mus[i]))
	random_stat_row.append(random_sort[index_value])

	random_statistics.append(random_stat_row)

#Recon_stat contains the statistic values for the Reconstructed portfolio (for each of the expected rate of returns)
f5 = open('Recon_stat.csv', 'w')
writer = csv.writer(f5)
writer.writerow(["Mean", "Standard Deviation", "Least Sq Err", "Median"])
for values in recon_statistics:
	writer.writerow(values)
f5.close()

#Random_stat contains the statistic values for the Random portfolio  (for each of the expected rate of returns)
f6 = open('Random_stat.csv', 'w')
writer = csv.writer(f6)
writer.writerow(["Mean", "Standard Deviation", "Least Sq Err", "Median"])
for values in random_statistics:
	writer.writerow(values)
f6.close()


#Drawing a graph for each target rate

graph_creation(mus,reconstructed_data,random_data,no_time)
