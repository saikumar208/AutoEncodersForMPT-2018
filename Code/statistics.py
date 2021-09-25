import numpy as np
import scipy
from scipy import stats
import math

def calculate_LSE(row,t):  #t is target 
	x = 0.0

	for i in range(0,len(row)):
		x = x + (row[i] - t)*(row[i] - t)
	return x


def calculate_mean(row):
	x = 0.0
	for i in range(0,len(row)):
		x = x + row[i]
	
	x = x/len(row)
	return x


def calculate_sd(row):
	mean = calculate_mean(row)
	x = 0.0
	
	for i in range(0, len(row)):
		x = x + (row[i] - mean)*(row[i] - mean)		
    
	x = x/len(row)
	x = math.sqrt(x)
	return x
