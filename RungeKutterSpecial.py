#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is a multi-use RK4 integrator. It can be used to find the motion 
of an object using only it’s acceleration. An object with a set of 
initial values (first and second derivatives of equations) and a 
dvals_dt(self, t, vals) definition is needed to run. The solve definition 
needs an ending time and an nkeep and will return one of the following:
    
If nkeep = 1 it will only return the last set of values

If nkeep = 0 it will return every set of values calculated

If nkeep = another positive number other than 0 and 1 it will return
that many sets of values
"""
#==============================================================================
import sys
import numpy as np
import matplotlib.pyplot as plt


#NEED AND INIT OF 8 (x,y,z,vx,vy,vz,theta,omega)

class RungeKutter (object):
    def __init__(self, eqs, verbose = 0):
        self.eqs = eqs
        self.ti = 0
        self.verbose = verbose
        self.reset()
        
    def reset(self):
        self.t = self.ti
        self.vals = self.eqs.initvals
    
    def solve(self, t, nkeep=0):
        dt=self.eqs.dt
        #dt = .0001

        if (nkeep==1):
            ret = []
            
            while self.t <= t:
                  c1 = self.eqs.dvals_dt(self.t, self.vals)
                  c2 = self.eqs.dvals_dt(self.t + dt / 2., self.vals + (c1 * (dt / 2.)))
                  c3 = self.eqs.dvals_dt(self.t + dt / 2., self.vals + (c2 * (dt / 2.)))
                  c4 = self.eqs.dvals_dt(self.t + dt, self.vals + (c3 * dt))
                  self.vals[:] += (dt / 6.) * (c1 + 2 * c2 + 2 * c3 + c4)
                  self.t += dt
            
            time = np.array([self.t])
            row = np.concatenate((time, self.vals.copy()))
            return row
        
        elif (nkeep == 0):
            time = [self.t]
            row = [self.vals.copy()]
            
            i=1
            while self.t < t:
                  c1 = self.eqs.dvals_dt(self.t, self.vals)
                  c2 = self.eqs.dvals_dt(self.t + dt / 2., self.vals + (c1 * (dt / 2.)))
                  c3 = self.eqs.dvals_dt(self.t + dt / 2., self.vals + (c2 * (dt / 2.)))
                  c4 = self.eqs.dvals_dt(self.t + dt, self.vals + (c3 * dt))
                  self.vals[:] += (dt / 6.) * (c1 + 2 * c2 + 2 * c3 + c4)
                  self.t += dt
                  time.append(self.t)
                  row.append(self.vals.copy())
                  i += 1
                  
                  
                  
            ret = np.empty((len(time), len(row) + 1))
            ret[:,0] = time
            ret[:,1:] = row
            return np.array(ret)
        
        
        
        else:
            time = [self.t]
            #self.eqs.tList.append(t)
            self.eqs.fuel.iterate(dt)
            
            row = [self.vals.copy()]
            
            timesave = (t - self.t)/nkeep
            
            #save_every = int(t / dt / nkeep +0.5)
            nextsave = timesave
            
            i=1
            while self.t < t:
                
                if self.t == (t - (2*dt)):
                    import pdb; pdb.set_trace()
                    
                c1 = self.eqs.dvals_dt(self.t, self.vals)
                c2 = self.eqs.dvals_dt(self.t + dt / 2., self.vals + (c1 * (dt / 2.)))
                c3 = self.eqs.dvals_dt(self.t + dt / 2., self.vals + (c2 * (dt / 2.)))
                c4 = self.eqs.dvals_dt(self.t + dt, self.vals + (c3 * dt))
                self.vals[:] += (dt / 6.) * (c1 + 2 * c2 + 2 * c3 + c4)
                
                if self.verbose >= 4:
                    sys.stderr.write("==========================================\n")
                    sys.stderr.write("At t={:7.2f}, θ={:.3g} and ω={:.3g}\n"
                                     .format(self.t, self.vals[6], self.vals[7]))
                    sys.stderr.write("==========================================\n\n")

#==============================================================================
#                 ct1 = self.eqs.domega_dt(self.t, self.vals)
#                 ct2 = self.eqs.domega_dt(self.t + dt / 2., self.vals[6:] + (ct1 * (dt / 2.)))
#                 ct3 = self.eqs.domega_dt(self.t + dt / 2., self.vals[6:] + (ct2 * (dt / 2.)))
#                 ct4 = self.eqs.domega_dt(self.t + dt, self.vals[6:] + (ct3 * dt))
#                 self.vals[6:] += (dt / 6.) * (ct1 + 2 * ct2 + 2 * ct3 + ct4)
#==============================================================================
                
                self.t += dt
                if (self.t == 2.):
                    tears = True
                
                
                if timesave <= self.t:
                    time.append(self.t)
                    row.append(self.vals.copy())

                    timesave += nextsave

            dlastT = self.t - row[-1][0]

            if dlastT > .5*nextsave:
                time.append(self.t)
                row.append(self.vals.copy())
                    
            elif dlastT < .5 * nextsave:
                time[-1] = self.t
                row[-1] = self.vals.copy()
                
            ret = np.empty((len(time), len(self.vals) + 1))
            ret[:, 0] = time
            ret[:, 1:] = row
            return np.array(ret)
 
