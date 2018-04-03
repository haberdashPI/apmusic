import numpy as np

def ilogit(xs): return 1./(1+np.exp(-xs))
def logit(xs): return np.log(xs/(1.0-xs))
def otop(o): return o/(1+o)
def ptoo(p): return 1/(1/p - 1)

def cilower(xs): return xs.quantile(0.159)
def ciupper(xs): return xs.quantile(1-0.159)
