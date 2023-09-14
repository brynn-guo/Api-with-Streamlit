# Author: lizhiyuan  <lizhiyuan@baqis.ac.cn>  2021/01/01

import numpy as np
from qos_tools.fit.fitclass import FitClass
from qos_tools.fit import function, plotscript
from home.hkxu.tools import lookup, get_record_by_id
from scipy.optimize import curve_fit

def exponential(x, A, B, C):
    return A*np.exp(-x/B)+C

def exponential_fit(x,y):
    A  = max(y) - min(y)
    B = x[round(len(x) / 2)]
    C = min(y)
    p0 = [A, B, C]
    popt, pcov = curve_fit(exponential, xdata = x, ydata = y, p0 = p0)
    return [exponential(a, *popt) for a in x]



