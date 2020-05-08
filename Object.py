# -*- coding: utf-8 -*-
"""
This file is a part of mei_comp_2020

This file is the workhorse of the project. It is passed a list 
of pane objects along with the air, fuel, dt, and the initial angle 
information (a list of angle and d angle/ dt). It is currently only 
able to be used with an object with all of the center of masses of 
their panes on the x-y axis with a 2D rotation. It includes a 
dvals_dt function for use with an RK4 integrator. 

Requires the use of numpy and physvis.
"""
#==============================================================================
import numpy as np

class Object(object):
    
    def __init__(self, panes, air, fuel, dt, ang, verbose = 0, init_quat = np.array((0., 0., 0., 1.))):
        self.panes = panes
        self.air = air
        self.fuel = fuel
        xy = np.concatenate((self.air.r, self.air.v))
        self.initvals = np.concatenate((xy, ang))
        self.mTotPane = 0
        self.dt = dt
        for i in range(len(self.panes)):
            self.mTotPane += panes[i].mass
        
        self.CMTotPanes = self.calcCMTotPane()
        self.CMTot = self.calcCMTot()
        
        print("mpanes = {} and CMtot = {}".format(self.mTotPane, self.CMTot))
        
        self.quat = np.copy(init_quat)
        
        self.verbose = verbose

#=============================================================================        

    """these definitions are for use in the init statement to find needed values"""
    
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
               
    """This dvals_dt statement is for use by a RK4 program"""
    
    def dvals_dt(self, t, vals):
        ders = np.empty(8)
        ders[0:3] = vals[3:6]

        force = self.forceTot(vals[3:6], vals[6])
        ders[3:6] = force / self.mTot()

        ders[6] = vals[7]
        
        I = self.calcITotal()
        Idot = self.calcIdotTotal(vals[3:6])
        
        T = self.torResistiveTot(vals[3:6], vals[6])
        
        ders[7] = T[2] / I - (vals[7] * Idot / I)
        if (self.verbose >= 2):
            print("theta = {:.3g} and omega = {:.3g} T = {:.3g} and I = {:.3g} and Idot = {:.3g}\n".format(vals[6], vals[7], T[2], I, Idot))
        
        return ders
        
#=============================================================================  
        
    """these definitions are used by the dvals_dt and calls on the Pane.py 
    to calculate the total of the forces on the object"""
    
    def forceTot(self, v, theta, g = 9.8):
        Fg = np.array((0, -(self.mTot()) * g, 0))
        Fr = self.forceResistiveTot(v, theta)

        # Not rotating thrust twice because self.quat is always the identity quaternion
        # thrust = self.rotate(theta, self.fuel.thrust(self.quat))
        # For now, force thrust to be down, which isn't completely realistic 
        # I chose to think about this as what the gimble on the engins
        thrust = self.rotate(theta, self.fuel.thrust(self.quat))
        if (self.verbose >= 2):
            print("\nv = [{:.3g}, {:.3g}, {:.3g}]".format(v[0], v[1], v[2]))
            tmptot = thrust + Fg + Fr
            print("thrust = [{:.3g}, {:.3g}, {:.3g}], "
                  "Fg = [{:.3g}, {:.3g}, {:.3g}], "
                  "Fr = [{:.3g}, {:.3g}, {:.3g}], "
                  "tot = [{:.3g}, {:.3g}, {:.3g}]"
                  .format(thrust[0], thrust[1], thrust[2], Fg[0], Fg[1], Fg[2],
                          Fr[0], Fr[1], Fr[2], tmptot[0], tmptot[1], tmptot[2]))
            print("=========================================================\n")
        return (thrust + Fg + Fr)
        #return (Fg)
    
    def forceResistiveTot(self, v, theta):
        fTot = np.zeros(3)
        
        for i in range(len(self.panes)):
#            print("fR on pain {} which has point 0 {}".format(i, self.panes[i].points[0]))
            f = self.panes[i].calcForceResistive(v, 
                              self.air.denAir(self.CMTot[1]), self.air.mAir, theta)
            fTot += f
            if (self.verbose >= 2):
                print("   f resistive Tot = [{:.3g}, {:.3g}, {:.3g}] on pane {}"
                      .format(f[0], f[1], f[2], i))
        return fTot 
    
#=============================================================================
        
    """these definitions are used by the dvals_dt and calls on the Pane.py 
    to calculate the total of the torques on the object"""
    
    def torResistiveTot(self, v, theta):
        if (self.verbose >= 2):
            print("\ntheta = {}".format(theta))
        torTot = np.array((0., 0., 0.))
        if (self.verbose >= 3):
            print("\nCalculating Torque:")
        for i in range(len(self.panes)):
            r = self.rotate(theta, self.panes[i].CM - self.CMTot)
            f = self.panes[i].calcForceResistive(v,self.air.denAir(self.CMTot[1]), 
                      self.air.mAir, theta)
            tor = np.cross(r, f)
            torTot += tor
            if (self.verbose >= 3):
                print("Torque result:")
                print("  pane {}: CM = [{:.3g}, {:.3g}, {:.3g}]  CMTot = [{:.3g}, {:.3g}, {:.3g}]"
                      .format(i, self.panes[i].CM[0], self.panes[i].CM[1], self.panes[i].CM[2],
                              self.CMTot[0], self.CMTot[1], self.CMTot[2]))
                print("  pane {}: r = [{:.3g}, {:.3g}, {:.3g}], f = [{:.3g}, {:.3g}, {:.3g}], "
                      "tor = [{:.3g}, {:.3g}, {:.3g}], torTot = [{:.3g}, {:.3g}, {:.3g}]\n"
                      .format(i, r[0], r[1], r[2], f[0], f[1], f[2], tor[0], tor[1], tor[2],
                              torTot[0], torTot[1], torTot[2]))
        if (self.verbose >= 2):
            print("v=[{:.3g}, {:.3g}, {:.3g}], θ={:.3g}, torTot=[{:.3g}, {:.3g}, {:.3g}]\n"
                  .format(v[0], v[1], v[2], theta, torTot[0], torTot[1], torTot[2]))
        
        return torTot
    
    def calcITotal(self):
        ITot = 0
        for i in range(len(self.panes)):
            r = self.mag(self.panes[i].CM - self.CMTot)
            ITot += self.panes[i].mass * np.square(r)
            if (self.verbose >= 3):
                print("pane {}: r = {:.3g}, m = {:.3g}, I = {:.3g}, ITot = {:.3g}"
                      .format(i, r, self.panes[i].mass, self.panes[i].mass * np.square(r), ITot))
        return ITot    
    
    def calcIdotTotal(self, v):
        """This will be seful for 3D rotations"""
        IdotTot = 0
#        rdot = self.mag(v)
#        for i in range(len(self.panes)):
#            r = self.panes[i].CM - self.CMTot
#            IdotTot += 2 * self.panes[i].mass * self.mag(r) * (rdot)
#            if (self.verbose == True):
#                print("pane {}: r = {}, Idot = {}, IdotTot = {}".format(i, r, 2 * self.panes[i].mass * self.mag(r) * (rdot), IdotTot))
        return IdotTot   
        

#==============================================================================
        
    """these definitions rotate vectors. the first is 3d and uses quaternions 
    and the second is for current use for 2D rotations"""
    
#     def rotate(self, alpha):
#         self.quat = calcQuat(alpha)
#         for i in range(len(self.panes)):
#             #does it matter that I rotate the actual points or could i just rotate the Nhats
#             self.panes[i].rotateNHat(q)
      
    def rotate(self, theta, xy):
        """This rotates the vector by theta about the +z axis"""
        return (np.array((((xy[0] * np.cos(theta)) - (xy[1] * np.sin(theta))), 
                         ((xy[0] * np.sin(theta)) + (xy[1] * np.cos(theta))), 0)))
        
#=============================================================================    

        
    """These are definitions to be used within this file for ease of use"""
    
    def mag(self, r):
        R = 0
        for i in range(len(r)):
            R += np.square(r[i])
        return np.sqrt(R)
    

            
    
