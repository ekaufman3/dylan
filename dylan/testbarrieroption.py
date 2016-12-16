# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 22:44:26 2016

@author: Ethan
"""
from montecarlo import MonteCarloBarrierPricer, AntitheticMonteCarloBarrierPricer
from bridge import StratifiedMonteCarloPricer
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

    #dobmCallT = MonteCarloBarrierPricer(S, K, r, v, q, T, H, reps, steps)
    #dobmPrc = dobmCallT.mean() * np.exp(-r * T)
    #dobmSE = dobmCallT.std(ddof=1) / np.sqrt(reps)
    
    dobmcall = MonteCarloBarrierPricer(S, K, r, v, q, T, H, reps, steps)
    dobmPrc = dobmcall[0]
    dobmSE = dobmcall[1]
    dobmtime = dobmcall[2]
    
    dobacall = AntitheticMonteCarloBarrierPricer(S, K, r, v, q, T, H, reps, steps)
    dobaPrc = dobacall[0]
    dobaSE = dobacall[1]
    dobatime = dobacall[2]

    dobscall = StratifiedMonteCarloPricer(S, K, r, v, q, T, H, reps, steps)
    dobsPrc = dobscall[0]
    dobsSE = dobscall[1]
    dobstime = dobscall[2]

    #dobsacall = StratifiedMonteCarloPricer(S, K, r, v, q, T, H, reps, steps)
    #dobsaPrc = dobsacall[0]
    #dobsaSE = dobsacall[1]
    #dobsatime = dobsacall[2]
    
    df = pd.DataFrame({'Engine': ['SimpleMonteCarlo', 'AntitheticSampling', 'Stratified Sampling', 'Antithetic Stratified'], 'Price':[dobmPrc, dobaPrc, dobsPrc, 0], 'Standard Error':[dobmSE, dobaSE, dobsSE, 0], 'Computational Time':[dobmtime, dobatime, dobstime, 0]})   
    print (df)    
    print ("As the table above shows, there is a consistent trade-off between the computational time and the variance reduction costs, as the lower the standard error goes and the more precise the price output becomes, the greater resources and therefore time is required to achieve the improved results.")
if __name__ == "__main__":
    main()