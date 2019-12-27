"""
December 19th 2019
            Author T.Mizumoto
"""
#! python 3
# ver.01.00
# rms_function.py  -  this program calculate RMS

import numpy as np

def fun_rms(data, meandata):
    Xi_Xave  = data - meandata
    square   = np.square(Xi_Xave)   
    SUM      = np.sum(square , axis = 0)
    division = SUM / len(data)
    sqrt     = np.sqrt(division)
    return sqrt