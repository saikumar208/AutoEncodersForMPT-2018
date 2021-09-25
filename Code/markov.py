import numpy as np
import matplotlib.pyplot as plt
import pylab
import cvxopt as opt
from cvxopt import blas, solvers
import pandas as pd
import portfolioopt as pfopt

solvers.options['show_progress'] = False
n_assets = 4
n_obs = 240

return_vec = np.random.randn(n_assets, n_obs)


np.random.seed(123)
"""

## NUMBER OF OBSERVATIONS

#print(return_vec)
plt.plot(return_vec.T, alpha=.4);
plt.xlabel('time')
plt.ylabel('returns')
"""


def rand_weights(n):
    ''' Produces n random weights that sum to 1 '''
    k = np.random.rand(n)
    return k / sum(k)

def random_portfolio(returns):
    '''
    Returns the mean and standard deviation of returns for a random portfolio
    '''

    p = np.asmatrix(np.mean(returns, axis=1))
    w = np.asmatrix(rand_weights(returns.shape[0]))
    C = np.asmatrix(np.cov(returns))

    mu = w * p.T
    sigma = np.sqrt(w * C * w.T)

    # This recursion reduces outliers to keep plots pretty
    if sigma > 2:
        return random_portfolio(returns)
    return mu, sigma

def call_pf_opt(returns, t_r, no_time):
    b = list()
    a = []
    for i in range(0, no_time):
    	b = list()
    	for j in range(0,30):
    		b.append(returns[j][i])
    	a.append(b)
    dates = pd.date_range('1/1/2000', periods=no_time, freq='M', tz='UTC')
    assets = ["Stock"]*30
    returns = pd.DataFrame(a, columns=assets, index=dates)
    avg_rets = returns.mean()
    cov_mat = returns.cov()
    #print(cov_mat)
    #print(avg_rets)
    target_ret = t_r
    calc_weights = pfopt.markowitz_portfolio(cov_mat, avg_rets, target_ret).values
    return calc_weights

def optimal_portfolio(returns, no_time):
    portfolios = []
    previous_wts = [1/30]*30
    for x in range(1,10):
        try:
            temp = call_pf_opt(returns, float(x/1000), no_time)
            previous_wts = temp
        except:
            temp = previous_wts
        portfolios.append(temp)
    return portfolios

    """n = len(returns)
    returns = np.asmatrix(returns)
    mus = [(t*0.001) for t in range(10,20)]
    #print(mus)
    S = opt.matrix(np.cov(returns))
    pbar = opt.matrix(np.mean(returns, axis=1))
    G = -opt.matrix(np.eye(n))   #identity matrix
    h = opt.matrix(0.0, (n ,1))
    A = opt.matrix(1.0, (1, n))
    b = opt.matrix(1.0)

    #Calculate efficient frontier weights using quadratic programming
    portfolios = [solvers.qp(mu*S, -pbar, G, h, A, b)['x']
                  for mu in mus]
"""
    #portfolios = []

    #for x in mus:
    #    portfolios.append(solvers.qp(x*S, -pbar, G, h, A, b)['x'])
    """print(x)
        print(portfolios)
        s = 0
        for x in portfolios:
            s = s + x
        print(s)
        print()
        print()
	"""
    return portfolios
    ## CALCULATE RISKS AND RETURNS FOR FRONTIER
    #returns = [blas.dot(pbar, x) for x in portfolios]
    #risks = [np.sqrt(blas.dot(x, S*x)) for x in portfolios]
    ## CALCULATE THE 2ND DEGREE POLYNOMIAL OF THE FRONTIER CURVE
    #m1 = np.polyfit(returns, risks, 2)
    #x1 = np.sqrt(m1[2] / m1[0])
    #print(m1)
    # CALCULATE THE OPTIMAL PORTFOLIO
    #wt = solvers.qp(opt.matrix(x1 * S), -pbar, G, h, A, b)['x']
    #return np.asarray(wt), returns, risks

#weights, returns, risks = optimal_portfolio(return_vec)
def do():
	return_vec = np.random.randn(n_assets, n_obs)
	t = optimal_portfolio(return_vec)
	for x in t:
		print(x)
