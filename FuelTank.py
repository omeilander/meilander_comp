# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 14:18:21 2020

@author: omeil
"""
import numpy as np
import quat

class FuelTank(object):
    def __init__(self, fuelCM, fuelMass, burnTime, _thrust):
        self.CM = np.array(fuelCM)
        self.mfi = fuelMass
        self.mf = self.mfi
        self.bT = burnTime
        self.bTLeft = burnTime
        self._thrust = _thrust
        
    def iterate(self, dt):
        self.mf -= (self.mfi / (self.bT / dt))
        self.bTLeft -= dt
        
    def thrust(self, q):
        if (self.bTLeft > 0):
            thr = np.array((0, self._thrust, 0))
            return(quat.quaternion_rotate(thr, q))
        else:
            return 0