# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 22:44:26 2016

@author: Ethan
"""
from dylan.montecarlo import MonteCarloBarrierPricer, AntitheticMonteCarloBarrierPricer
from dylan.bridge import StratifiedMonteCarloPricer
import numpy as np
import pandas as pd

def main():
    K = 100
    T = 1 
    S = 100
    v = 0.2
    r = 0.06
    q = 0.03
    H = 99
    steps = 2**8
    reps = 100

    dobmCallT = MonteCarloBarrierPricer(S, K, r, v, q, T, H, reps, steps)
    dobmPrc = dobmCallT.mean() * np.exp(-r * T)    
    dobmSE = dobmCallT.std(ddof=1) / np.sqrt(reps)
    print(dobmSE)
    
    dobaCallT = AntitheticMonteCarloBarrierPricer(S, K, r, v, q, T, H, reps, steps)
    dobaPrc = dobaCallT.mean() * np.exp(-r * T)    
    dobaSE = dobaCallT.std(ddof=1) / np.sqrt(reps)
    print(dobaSE)

    dobsCallT = StratifiedMonteCarloPricer(S, K, r, v, q, T, H, reps, steps)
    dobsPrc = dobsCallT.mean() * np.exp(-r*T)
    dobsSE = dobsCallT.std(ddof=1) / np.sqrt(reps)

    #dobsaCallT = StratifiedMonteCarloPricer(S, K, r, v, q, T, H, reps, steps)
    #dobsaPrc = dobsaCallT.mean() * np.exp(-r*T)
    #dobsaSE = dobsaCallT.std(ddof=1)/np.sqrt(reps)
    
    df = pd.DataFrame({'Engine': ['SimpleMonteCarlo', 'AntitheticSampling', 'Stratified Sampling', 'Antithetic Stratified'], 'Price':[dobmPrc, dobaPrc, dobsPrc, 0], 'Standard Error':[dobmSE, dobaSE, dobsSE, 0]})   
    print (df)    

if __name__ == "__main__":
    main()