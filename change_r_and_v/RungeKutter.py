#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 14:21:13 2019

@author: owen
"""
import numpy as np
import matplotlib.pyplot as plt




class RungeKutter (object):
    def __init__(self, eqs):
        self.eqsi = eqs
        self.ti = 0
        self.reset()
        
    def reset(self):
        self.t = self.ti
        self.eqs = self.eqsi
        self.vals = self.eqsi.initvals
    
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
                  self.vals[0:] += (dt / 6.) * (c1 + 2 * c2 + 2 * c3 + c4)
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
                  self.vals[0:] += (dt / 6.) * (c1 + 2 * c2 + 2 * c3 + c4)
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
            self.eqs.tList.append(t)
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
                try:
                   self.vals[0:] += (dt / 6.) * (c1 + 2 * c2 + 2 * c3 + c4)
                except TypeError as e:
                    import pdb; pdb.set_trace()
                    print("Duuuuuude")
                self.t += dt
                  
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
 