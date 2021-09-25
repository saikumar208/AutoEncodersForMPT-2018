#graph creation

#from create_markov import *
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



def graph_creation(mus,reconstructed_data,random_data,no_time):


	t = arange(0, no_time, 1)

	#print(len(t), " The length is ", len(reconstructed_data[0]))


	s = list()

	for i in range(0, len(t)):
		s.append(1)

	for i in range(0, len(reconstructed_data)):
		recon_ini = 1
		random_ini = 1
		expected = 1
		
		for j in range(0,len(t)):
			s[j] = mus[i]

		plot(t, reconstructed_data[i])	== plot(t, s)
		name = "individual_graphs/reconstruct_" + str(mus[i]) + ".png"
		savefig(name)

		clf()

		plot(t, random_data[i])
		plot(t, s)
		name = "individual_graphs/random_" + str(mus[i]) + ".png"
		savefig(name)
		print(scipy.stats.ttest_ind(reconstructed_data[i], random_data[i], equal_var = False))

		clf()
		gca().set_color_cycle(['Red','Blue','Yellow'])
		plot(t, random_data[i])
		plot(t, reconstructed_data[i])
		plot(t, s)
		name = "consolidated_graphs/consolidated_" + str(mus[i]) + ".png"
		savefig(name)
		clf()
		
				
		r_d = sorted(reconstructed_data[i])
		fit = stats.norm.pdf(r_d, np.mean(r_d), np.std(r_d))
		plot(r_d, fit)
		
		r_d = sorted(random_data[i])
		fit = stats.norm.pdf(r_d, np.mean(r_d), np.std(r_d))
		plot(r_d, fit)

		name = "consolidated_graphs/consolidated_pdf" + str(mus[i]) + ".png"
		savefig(name)
		clf()
		
		
		recon_dd = list()
		random_dd = list()
		expect_dd = list()
		for ret_iter in range(len(reconstructed_data[i])):
			recon_dd.append(recon_ini)
			random_dd.append(random_ini)
			expect_dd.append(expected)
			recon_ini = recon_ini*(1+reconstructed_data[i][ret_iter])
			random_ini = random_ini*(1+random_data[i][ret_iter])
			expected = expected*(1 + float(mus[i]))
		name = "consolidated_graphs/consolidated_compounded_" + str(mus[i]) + ".png"
		gca().set_color_cycle(['Red','Blue','Yellow'])
		plot(t, random_dd)
		plot(t, recon_dd)
		plot(t, expect_dd)
		savefig(name)
		clf()
