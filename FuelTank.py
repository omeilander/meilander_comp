# -*- coding: utf-8 -*-
"""
This file is a part of mei_comp_2020

This file creates the fuel tank of the rocket. It needs the CM of 
the fuel, total mass, burn time, and thrust of the fuel tank. It 
can calculate the direction of the thrust along with keeping track 
of how long the engine would continue to run.

Requires the use of numpy.
"""
#==============================================================================
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