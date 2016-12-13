import abc
import numpy as np
from scipy.stats import binom


class PricingEngine(object, metaclass=abc.ABCMeta):
    """
    An option pricing engine interface.

    """

    @abc.abstractmethod
    def calculate(self):
        """
        A method to implement an option pricing model.

        The pricing method may be either an analytic model (i.e. Black-Scholes or Heston) or
        a numerical method such as lattice methods or Monte Carlo simulation methods.

        """

        pass


class BinomialPricingEngine(PricingEngine):
    """
    A concrete PricingEngine class that implements the Binomial model.

    Args:
        

    Attributes:


    """

    def __init__(self, steps, pricer):
        self.__steps = steps
        self.__pricer = pricer

    @property
    def steps(self):
        return self.__steps

    @steps.setter
    def steps(self, new_steps):
        self.__steps = new_steps

    def calculate(self, option, data):
        return self.__pricer(self, option, data)


def EuropeanBinomialPricer(pricing_engine, option, data):
    """
    The binomial option pricing model for a plain vanilla European option.

    Args:
        pricing_engine (PricingEngine): a pricing method via the PricingEngine interface
        option (Payoff):                an option payoff via the Payoff interface
        data (MarketData):              a market data variable via the MarketData interface

    """

    expiry = option.expiry
    strike = option.strike
    (spot, rate, volatility, dividend) = data.get_data()
    steps = pricing_engine.steps
    nodes = steps + 1
    dt = expiry / steps 
    u = np.exp((rate * dt) + volatility * np.sqrt(dt)) 
    d = np.exp((rate * dt) - volatility * np.sqrt(dt))
    pu = (np.exp(rate * dt) - d) / (u - d)
    pd = 1 - pu
    disc = np.exp(-rate * expiry)
    spotT = 0.0
    payoffT = 0.0
    
    for i in range(nodes):
        spotT = spot * (u ** (steps - i)) * (d ** (i))
        payoffT += option.payoff(spotT)  * binom.pmf(steps - i, steps, pu)  
    price = disc * payoffT 
     
    return price 
def AmericanBinomialPricer(pricing_engine, option, data):
    T = option.expiry
    K = option.strike
    (spot, rate, volatility, dividend) = data.get_data()
    N = pricing_engine.steps
    nodes = N + 1
    dt = T/N 
    u = np.exp((rate * dt) + volatility * np.sqrt(dt)) 
    d = np.exp((rate * dt) - volatility * np.sqrt(dt))
    pu = (np.exp(rate * dt) - d) / (u - d)
    pd = 1 - pu
    disc = np.exp(-rate * dt)
    dpu = disc * pu
    dpd = disc * pd
    
    Ct = np.zeros(nodes)
    St = np.zeros(nodes)

    for i in range(nodes):
        St[i] = spot * (u ** (N - i)) * (d ** i)
        Ct[i] = option.payoff(St[i])

    for i in range((N - 1),-1,-1):
        for j in range(i+1):
            Ct[j] = dpu * Ct[j] + dpd * Ct[j+1]
            St[j] = St[j] / u
            Ct[j] = np.maximum(Ct[j], option.payoff(St[j]))

    return Ct[0]
