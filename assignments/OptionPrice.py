import scipy.stats
import sys
import numpy as np
import matplotlib.pyplot as plt

# This function simulates geometric Brownian motion.
# Inputs: S_0        (float),    the initial stock price
#         volatility (float),    the stock volatility
#         T          (int),    the number of time steps to simulate
# Output: the simulated stock price over time (array of size T+1)
def simulate(S_0, volatility, T):
    price = np.zeros(T+1)
    price[0] = S_0
    for t in range(T):
        price[t+1] = price[t] * np.exp(-volatility**2/2.0 + np.random.randn()*volatility)
    return price

# This function smoothes an array of 1-d data using a moving window average
# Inputs:   data          (array), the data to be smoothed
#           W             (int)  , the window size
# Outputs:  the smoothed data (array, same size as data)
def smooth(data, W):
    T = len(data) # a little confusing since the length is T+1 outside the function
    smoothed_data = np.zeros(T)
    for t in range(T):
        count = 0
        for window in range(t-W, t+W+1):
            if window >= 0 and window < T:
                smoothed_data[t] += price[window]
                count += 1
        smoothed_data[t] /= count
        # alternate solution below:
        # smoothed_price[t] = np.mean(price[max(0,t-W):min(T,t+W+1)]) 
    return smoothed_data

# This function computes the price of a stock option using the Black-Scholes formula
# Inputs:   S_0           (float), the initial stock price
#           strike_price  (float), the option's strike price
#           volatility    (int)  , the stock volatility
#           T             (int)  , time until the option expires
# Outputs:  the Black-Scholes option price (float)
def blackScholes(S_0, strike_price, volatility, T):
    d1 = (np.log(S_0/strike_price)+( volatility**2/2.0)*T) / (volatility*np.sqrt(T))
    d2 = (np.log(S_0/strike_price)+(-volatility**2/2.0)*T) / (volatility*np.sqrt(T))
    
    return scipy.stats.norm.cdf(d1)*S_0 - scipy.stats.norm.cdf(d2)*strike_price


"""
START OF PROGRAM
"""

initial_price = float(sys.argv[1])
volatility    = float(sys.argv[2])
T             = int(  sys.argv[3])
strike_price  = float(sys.argv[4])
W             = int(  sys.argv[5])
N_repeats     = int(  sys.argv[6])


price = simulate(initial_price, volatility, T)

plt.plot(price)
smoothed_price = smooth(price, W)

plt.plot(smoothed_price, 'r')

plt.xlabel('time (arbitrary units)')
plt.ylabel('stock price (\$)')
plt.savefig('stockprice.pdf')


simulated_option_prices = np.zeros(N_repeats)
for i in range(N_repeats):
    end_price = simulate(initial_price, volatility, T)[-1]
    if end_price < strike_price:
        simulated_option_prices[i] = 0.0
    else:
        simulated_option_prices[i] = end_price-strike_price
print 'Estimated option price:     $%f' % np.mean(simulated_option_prices)
print 'Black-Scholes option price: $%f' % blackScholes(initial_price, strike_price, volatility, T)

