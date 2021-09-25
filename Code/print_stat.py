from sklearn import preprocessing
import numpy as np
import csv
import scipy
from scipy import stats
from random import random
import math
from pylab import *
import pandas

def print_statistics(filename,Traindataset,recon_pf,start,no_time):

	f = pandas.read_csv("names.csv")

	f9 = open(filename, 'w')	
	writer = csv.writer(f9)
	write_row = list()
	writer.writerow(["Company Name", "Mean", "Std Dev", "Median", "Kurtosis", "Skew"])
	counter = 0	

	for x in recon_pf:

		training_list = list()	
		training_list.append(Traindataset[x, start: start + no_time])		
		n_t = np.array(training_list[0])
		mean = np.mean(n_t)
		std_dev = np.std(training_list[0])
		kurt = scipy.stats.kurtosis(n_t)
		name = f.iloc[recon_pf[counter],1]
		median = np.median(n_t)
		skew = scipy.stats.skew(n_t)
		write_row = [name, mean, std_dev, median, kurt, skew]
		writer.writerow(write_row)
		counter = counter + 1
		
	f9.close()
