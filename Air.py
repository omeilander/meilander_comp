# -*- coding: utf-8 -*-
"""
This file is a part of mei_comp_2020

This file creates the air that the object is moving through. 
The starting position and the velocity of the air is passed to 
create the model of air. It is called by Object.py in its 
dvals_dt function and uses the y-position to determine the 
density of air and passes the information back to calculate the
air resistance.

Requires the use of numpy.
"""
#==============================================================================
import numpy as np

class Air(object):
    
    def __init__(self, vo, r, mAir = (0.02897/6.022e23)):
        self.vo = np.array((vo))
        self.v = np.copy((vo))
        self.ro = np.array((r))
        self.r = np.copy((r))
        self.mAir = mAir
        
    def denAir(self, y):
        if (y < 11000):
            return (self.calcP1(y) / (0.2869 * (self.calcT1(y) + 273.1))) * (1 / self.mAir)
        
        elif (y > 25000):
            return (self.calcP3(y) / (0.2869 * (self.calcT3(y) + 273.1))) * (1 / self.mAir)
        
        else:
            return (self.calcP2(y) / (0.2869 * (self.calcT2(y) + 273.1))) * (1 / self.mAir)

        
#=============================================================================        
    #found at https://www.grc.nasa.gov/WWW/K-12/airplane/atmosmet.html
    def calcT1(self, y):
        return (15.04 - (.00649 * y))
    
    def calcP1(self, y):
        return 101.29 * ((self.calcT1(y) + 273.1) / 288.08)
    
    def calcT2(self, y):
        return (-56.46)
    
    def calcP2(self, y):
        return 22.65 * np.exp(1.73 - .000157 * y)
    
    def calcT3(self, y):
        return (-131.27 + .00299 * y)
    
    def calcP3(self, y):
        return 2.48 * ((self.calcT3(y) + 273.1) / 288.08) ** (-11.388)
    
    
    
    