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

    start = time.time()
    z = np.random.normal(size=(reps, steps))
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
    callPrc = callT.mean() * np.exp(-r * T)
    callSE = callT.std(ddof=1) / np.sqrt(reps)  
    end = time.time()
    mtime = end - start
    MC = (callPrc, callSE, mtime)
    return MC
    
def AntitheticMonteCarloBarrierPricer(S, K, r, v, q, T, H, reps, steps):
   
    start = time.time()
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
    callPrc = callT.mean() * np.exp(-r * T)
    callSE = callT.std(ddof=1) / np.sqrt(reps) 
    end = time.time()
    atime = end - start
    MC = (callPrc, callSE, atime)
    return MC