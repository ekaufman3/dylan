# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 21:20:17 2016

@author: Ethan
"""

#Monte Carlo
import numpy as np
import time

def CallPayoff(S, K):
    return np.maximum(S - K, 0.0)
def MonteCarloBarrierPricer(S, K, r, v, q, T, H, reps, steps):
    


    z = np.random.normal(size=(reps, steps))
    # uncomment this line below for antithetic sampling
    #z = np.concatenate((z,-z))
    
    M,N = z.shape
    spaths = np.zeros((M, N))
    callT = np.zeros(M)
    

    dt = T / steps
    nudt = (r - q - 0.5 * v * v) * dt
    sigsdt = v * np.sqrt(dt)
    spaths[:,0] = S
    barrierCrossed = False
    start = time.time()
    for i in range(M):
        barrierCrossed = False
        for j in range(1, N):
            spaths[i,j] = spaths[i,j-1] * np.exp(nudt + sigsdt * z[i,j])
            
            if spaths[i,j] <= H: 
                barrierCrossed = True
                break

        callT[i] = CallPayoff(spaths[i,-1],K) if not barrierCrossed else 0.0
    end = time.time()
    print ("Monte Carlo executes in " + str(end - start) + " seconds.")
    return callT   

    
def AntitheticMonteCarloBarrierPricer(S, K, r, v, q, T, H, reps, steps):
    z = np.random.normal(size=(reps, steps))
    z = np.concatenate((z,-z))
    
    M,N = z.shape
    spaths = np.zeros((M, N))
    callT = np.zeros(M)
    

    dt = T / steps
    nudt = (r - q - 0.5 * v * v) * dt
    sigsdt = v * np.sqrt(dt)
    spaths[:,0] = S
    barrierCrossed = False

    for i in range(M):
        barrierCrossed = False
        for j in range(1, N):
            spaths[i,j] = spaths[i,j-1] * np.exp(nudt + sigsdt * z[i,j])
            
            if spaths[i,j] <= H: 
                barrierCrossed = True
                break

        callT[i] = CallPayoff(spaths[i,-1],K) if not barrierCrossed else 0.0

    return callT