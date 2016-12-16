import numpy as np
from scipy.stats import norm
from math import log2, sqrt
import time

def CallPayoff(S, K):
    return np.maximum(S - K, 0.0)


def WienerBridge(T, steps, endval = 0.0):
    num_bisect = int(log2(steps))
    tjump = T
    ijump = int(steps - 1)
    
    if endval == 0.0: 
        endval = np.random.normal(scale=sqrt(T), size=1)

    z = np.random.normal(size=steps+1)
    w = np.zeros(steps+1)
    w[steps] = endval

    for k in range(num_bisect):
        left = 0
        i = ijump // 2 + 1
        right = ijump + 1
        limit = 2 ** k

        for j in range(limit):
            a = 0.5 * (w[left] + w[right])
            b = 0.5 * sqrt(tjump)
            w[i] = a + b * z[i]
            right += ijump + 1
            left += ijump + 1
            i += ijump + 1

        ijump //= 2
        tjump /= 2

    return w
  


def StratifiedUniformSample(m = 100):
    u = np.random.uniform(size=m)
    i = np.arange(m)
    uhat = (i + u) / m
    return uhat


def GeometricBrownianMotionBridge(S, r, q, v, H, T, steps, reps):
    dt = T / steps
    nudt = (r - q - 0.5 * v * v)*dt
    spaths = np.zeros((reps, steps+1))
    spaths[:,0] = S
    uhat = StratifiedUniformSample(reps)
    endval = norm.ppf(uhat)
    sigsdt = v * np.sqrt(dt)
    
    for i in range(reps):
        barrierCrossed = False
        w = WienerBridge(T, steps)
        z = nudt + v * np.diff(w)
        lpath = np.cumsum(np.insert(z, 0, np.log(S)))
        spaths[i] = np.exp(lpath)
        
        #for j in range(1, steps):
            #spaths[i,j] = spaths[i,j-1] * np.exp(nudt + sigsdt * z[i,j])
            
            #if spaths[i,j] <= H: 
             #   barrierCrossed = True
              #  break
            
    return spaths
    

def StratifiedMonteCarloPricer(S, K, r, v, q, T, H, reps, steps):
    
    start = time.time()
    spotT = GeometricBrownianMotionBridge(S, r, q, v, H, T, steps, reps)
    callT = CallPayoff(spotT.T[-1], K)
    callPrc = callT.mean() * np.exp(-r * T)
    callSE = callT.std(ddof=1) / np.sqrt(reps)
    end = time.time()
    stime = end - start
    MC = (callPrc, callSE, stime)
    return MC

