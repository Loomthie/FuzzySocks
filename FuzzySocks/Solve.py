from scipy.misc import derivative
import numpy as np


def newtoninan_solver(tol,f,x0,*args):
    diff = tol+1
    while diff > tol:
        try:
            x = x - f(x,*args)/derivative(f,x,args=args)
        except NameError:
            x = x0
        diff = np.abs(f(x,*args))
    return x


