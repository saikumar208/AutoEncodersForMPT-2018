from markov import *
from Auto import *
from print_stat import *
from sklearn import preprocessing
import numpy as np
import csv
import scipy
from scipy import stats
from random import random
import math
from pylab import *
import pandas
import csv


def create_markovitz_portfolios(no_time,Traindataset,Testdataset):
	print("In Mkt_cap")
	#start = 649
	start = 649
	recon_pf, random_pf = autoencode(start,no_time,Traindataset,Testdataset)
	reconstruct_data = list()
	random_data = list()
	reconstruct_row = list() # contains the returns for the different target rates for a cycle
	random_row = list()
	#mkt_cap_data = np.loadtxt("Market_cap.csv", delimiter=",")
	mkt_cap_data = list()
	
	mkt_cap_file = open("Market_cap.csv", newline = '')
	mkt_reader = csv.reader(mkt_cap_file)
	for mkt_cap_rows in mkt_reader:
		mkt_cap_data.append(mkt_cap_rows)
	
	f = pandas.read_csv("names.csv")
	
	print("Stocks in reconstructed portfolio")
	for x in recon_pf:
		print(f.iloc[x, 1])
	print("\n\n\nStocks in random portfolio")
	for x in random_pf:
		print(f.iloc[x, 1])

	#print(random_pf, "\n")
	#Creating files that store the statistic data for each file
	"""
	print_statistics('recon_training_period_stat.csv',Traindataset,recon_pf,start,no_time)

	print_statistics('random_training_period_stat.csv',Traindataset,random_pf,start,no_time)

	print_statistics('recon_testing_period_stat.csv',Traindataset,recon_pf,start + no_time,no_time)

	print_statistics('random_testing_period_stat.csv',Traindataset,random_pf,start + no_time,no_time)
	"""
	debug_f = open("Test_Rand.csv", "w")
	mkt_cap_list_recon = list()
	mkt_cap_list_random = list()
	debug_writer = csv.writer(debug_f)
	for i in range(0, no_time):
		#recon_pf, random_pf = autoencode(start+ i ,no_time,Traindataset,Testdataset)
		#print(len(recon_pf))
		#	print(recon_pf)
		return_series = list()
		print("I Value :" + str(i))
		for x in recon_pf:
			temp = Traindataset[x,start+i : start+i+no_time]
			for ret_iter in range(len(temp)):
				temp[ret_iter] = float(temp[ret_iter])
			return_series.append(temp)
			debug_writer.writerow(temp)
		rec_wts = optimal_portfolio(return_series, no_time)
		t = 0.0
		rec_ind = 0
		reconstruct_row = list()
		mkt_temp = list([])
		for x in recon_pf:
			mkt_c_check = float(mkt_cap_data[x][start + i + no_time])
			if mkt_c_check != int(-989898):
				mkt_temp.append(mkt_c_check)
			else:
				mkt_temp.append(0)
		mkt_cap_list_recon.append(mkt_temp)
		
		for x in rec_wts:
			t = t + 0.01
			act_return = 0.0
			rec_ind = 0
			for k in x:
				act_return = act_return + k*float(Traindataset[recon_pf[rec_ind], start + i + no_time + 1])
				rec_ind = rec_ind + 1
			reconstruct_row.append(act_return)

		reconstruct_data.append(reconstruct_row)
		return_series = list()
		mkt_temp = list([])
		for x in random_pf:
			mkt_c_temp = float(mkt_cap_data[x][start + i + no_time])
			if mkt_c_temp != (-989898):
				mkt_temp.append(mkt_c_temp)
			else:
				mkt_temp.append(0)
		mkt_cap_list_random.append(mkt_temp)
		
		for x in random_pf:
		    return_series.append(Traindataset[x,start+i : start+i+no_time])
		ran_wts = optimal_portfolio(return_series, no_time)
		t = 0.0
		ran_ind = 0
		random_row = list()
		for x in ran_wts:
			t = t + 0.01
			act_return = 0.0
			ran_ind = 0
			mkt_temp = list()
			#print(ran_ind)
			for k in x:
				#print(random_pf[ran_ind])
				#print(start + i + no_time + 1)
				#print(k)
				act_return = act_return + k*float(Traindataset[random_pf[ran_ind], start + i + no_time + 1])
				ran_ind = ran_ind + 1
			random_row.append(act_return)
		random_data.append(random_row)
	final_reconstruct = list()
	
	
	
	
	for j in range(0,len(reconstruct_data[0])):
		reconstruct_row = list()
		for i in range(0, len(reconstruct_data)):
			reconstruct_row.append(reconstruct_data[i][j])
		final_reconstruct.append(reconstruct_row)

	final_random = list()

	for j in range(0,len(random_data[0])):
		random_row = list()
		for i in range(0, len(random_data)):
			random_row.append(random_data[i][j])
		final_random.append(random_row)


	fl = open('Reconstructed.csv', 'w')
	writer = csv.writer(fl)

	for values in final_reconstruct:
		writer.writerow(values)
	fl.close()
	
	fl = open('Mkt_cap_recon.csv', 'w')
	writer = csv.writer(fl)

	for values in mkt_cap_list_recon:
		writer.writerow(values)
	fl.close()
	
	fl = open('Mkt_cap_random.csv', 'w')
	writer = csv.writer(fl)

	for values in mkt_cap_list_random:
		writer.writerow(values)
	fl.close()



	f2 = open('Random.csv', 'w')
	writer = csv.writer(f2)

	for values in final_random:
		writer.writerow(values)
	f2.close()
	debug_f.close()
	return final_random, final_reconstruct




#end of create_markovitz_portfolios
