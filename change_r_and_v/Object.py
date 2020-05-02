# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 14:17:07 2020

@author: omeil
"""
import numpy as np
from Pane import Pane
from Air import Air
from FuelTank import FuelTank
#import quat

class Object(object):
    
    def __init__(self, panes, air, fuel, v0, dt, ang, verbose = False, init_quat = np.array((0., 0., 0., 1.))):
        self.panes = panes
        self.air = air
        self.fuel = fuel
        
        self.mTotPane = 0
        self.dt = dt
        for i in range(len(self.panes)):
            self.mTotPane += panes[i].mass
        
        self.CMTotPanes = self.calcCMTotPane()
        self.CMTot = self.calcCMTot()
        
        print("mpanes = {} and CMtot = {}".format(self.mTotPane, self.CMTot))
        
        self.quat = np.copy(init_quat)
        
        # self.fTot_List = []
        self.fResistive_List = []
        # self.tList = []
        
        xy = np.concatenate((self.CMTot, v0))
        self.initvals = np.concatenate((xy, ang))
        
        self.verbose = verbose
#=============================================================================        
    def mTot(self):
        return (self.mTotPane + self.fuel.mf)
      
    def calcCMTotPane(self):
        CMTotPanes = np.zeros(3)
        
        for i in range(len(self.panes)):
            CMTotPanes += self.panes[i].CM * self.panes[i].mass
            
        return(CMTotPanes / self.mTotPane)
        
    def calcCMTot(self):
        return(self.CMTotPanes + (self.fuel.CM * self.fuel.mf) / self.mTot())
    
    
#=============================================================================                
    def forceTot(self, v, theta, g = 9.8):
        Fg = np.array((0, -(self.mTot()) * g, 0))
        Fr = self.forceResistiveTot(v, theta)
        #Fr = [0, 0, 0]
        self.fResistive_List.append(np.sqrt(np.square(Fr[0]) + np.square(Fr[1] + np.square(Fr[2]))))
        
        thrust = self.rotate(theta, self.fuel.thrust(self.quat))
        if (self.verbose == True):
            print("v = {}".format(v))
            print("thrust = {}, Fg = {}, Fr = {}, tot = {}".format(thrust, Fg, Fr, thrust + Fg + Fr))
        return (thrust + Fg + Fr)
        #return (Fg)
    
    def forceResistiveTot(self, v, theta):
        vel = v + self.air.v
        fTot = np.zeros(3)
        
        for i in range(len(self.panes)):
#            print("fR on pain {} which has point 0 {}".format(i, self.panes[i].points[0]))
            f = self.panes[i].calcForceResistive(v, 
                              self.air.denAir(self.CMTot[1]), self.air.mAir, theta)
            fTot += f
            if (self.verbose == True):
                print("f resistive Tot = {} on pane {}".format(f, i))
        return fTot 
    
#=============================================================================
    def torResistiveTot(self, v, theta):
        if (self.verbose == True):
            print("\ntheta = {}".format(theta))
        torTot = np.array((0., 0., 0.))
        for i in range(len(self.panes)):
            r = self.rotate(theta, self.panes[i].CM - self.CMTot)
            f = self.panes[i].calcForceResistive(v,self.air.denAir(self.CMTot[1]), 
                      self.air.mAir, theta)
            tor = np.cross(r, f)
            torTot += tor
            if (self.verbose == True):
                print("pane {}: CM = {}  CMTot = {}".format(i, self.panes[i].CM, self.CMTot))
                print("pane {}: r = {}, f = {}, tor = {}, torTot = {}\n".format(i, r, f, tor, torTot))
        return torTot
    
    def calcITotal(self):
        ITot = 0
        for i in range(len(self.panes)):
            r = self.mag(self.panes[i].CM - self.CMTot)
            ITot += self.panes[i].mass * np.square(r)
            if (self.verbose == True):
                print("pane {}: r = {}, m = {}, I = {}, ITot = {}".format(i, r, self.panes[i].mass, self.panes[i].mass * np.square(r), ITot))
        return ITot    
    
    def calcIdotTotal(self, v):
        IdotTot = 0
#        rdot = self.mag(v)
#        for i in range(len(self.panes)):
#            r = self.panes[i].CM - self.CMTot
#            IdotTot += 2 * self.panes[i].mass * self.mag(r) * (rdot)
#            if (self.verbose == True):
#                print("pane {}: r = {}, Idot = {}, IdotTot = {}".format(i, r, 2 * self.panes[i].mass * self.mag(r) * (rdot), IdotTot))
        return IdotTot   
        

#==============================================================================
#     def rotate(self, alpha):
#         self.quat = calcQuat(alpha)
#         for i in range(len(self.panes)):
#             #does it matter that I rotate the actual points or could i just rotate the Nhats
#             self.panes[i].rotateNHat(q)
      
    def rotate(self, theta, xy):
        return (np.array((((xy[0] * np.cos(theta)) - (xy[1] * np.sin(theta))), 
                         ((xy[0] * np.sin(theta)) + (xy[1] * np.cos(theta))), 0)))
        
#=============================================================================    
    def dvals_dt(self, t, vals):
        ders = np.empty(8)
        ders[0:3] = vals[3:6]

        force = self.forceTot(vals[3:6], vals[6])
        # self.fTot_List.append(np.sqrt(np.square(force[0]) + np.square(force[1]) + np.square(force[2])))
        # self.tList.append(self.tList[-1] + self.dt)
        ders[3:6] = force / self.mTot()

        ders[6] = vals[7]
        
        I = self.calcITotal()
        Idot = self.calcIdotTotal(vals[3:6])
        
        T = self.torResistiveTot(vals[3:6], vals[6])
        
        ders[7] = T[2] / I - (vals[7] * Idot / I)
        if (self.verbose == True):
            print("theta = {:.3g} and omega = {:.3g} T = {:.3g} and I = {:.3g} and Idot = {:.3g}\n".format(vals[6], vals[7], T[2], I, Idot))
        
        return ders
        
#==============================================================================
#     def domega_dt(self, t, vals):
#         derst = np.empty(2)
#         ders[0] = vals[7]
#         
#         I = self.calcITotal()
#         Idot = self.calcIdotTotal(vals[3:6])
#         
#         T = self.torResistiveTot(vals[3:6])
#         
#         ders[1] = self.mag((T / I) - (vals[7] * Idot / I))
#         
#         return ders
#==============================================================================
    
#=============================================================================  
    def mag(self, r):
        R = 0
        for i in range(len(r)):
            R += np.square(r[i])
        return np.sqrt(R)
    

            
    