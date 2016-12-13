# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 14:24:30 2016

@author: Ethan
"""

from dylan.payoff import VanillaPayoff, call_payoff, put_payoff
from dylan.engine import BinomialPricingEngine, AmericanBinomialPricer
from dylan.marketdata import MarketData
from dylan.option import Option


spot = 41.0
strike = 40.0
rate = 0.08
volatility = 0.30
expiry = 1.0
steps = 3
dividend = 0.0

the_call = VanillaPayoff(expiry, strike, call_payoff)
the_put = VanillaPayoff(expiry, strike, put_payoff) 
the_bopm = BinomialPricingEngine(steps, AmericanBinomialPricer)
the_data = MarketData(rate, spot, volatility, dividend)
   
    
amc_option = Option(the_call, the_bopm, the_data)
cprice = amc_option.price()
print("The American Binomial call option price is {0:.3f}".format(cprice))

    
amp_option = Option(the_put, the_bopm, the_data)
pprice = amp_option.price()
print("The American Binomial put option price is {0:.3f}".format(pprice))






