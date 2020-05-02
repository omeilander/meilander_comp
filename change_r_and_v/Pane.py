# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 14:16:10 2020

@author: omeil
"""
import numpy as np
#import quat

s = 0

class Pane(object):
    def __init__(self, location, density, thickness, dt, verbose = False):
        self.points = np.array(location)
        self.den = density
        self.thick = thickness
        self.dt = dt
        self.verbose = verbose
        
        self.area = self.calcArea()
        self.mass = self.calcMass()
        self.CM = self.calcCM()
        self.nHat = self.calcNHat()
        
    def calcArea(self):
        return(.5 * self.mag(np.cross((self.points[1] - self.points[0]), (self.points[2] - self.points[0]))))
        
    def calcMass(self):
        return(self.area * self.thick *self.den)

    def calcCM(self):
        return np.array(((self.points[0,0] + self.points[1,0] + self.points[2,0])/3,
                         (self.points[0,1] + self.points[1,1] + self.points[2,1])/3,
                         (self.points[0,2] + self.points[1,2] + self.points[2,2])/3))
 
    def calcNHat(self):
        n = np.cross((self.points[1] - self.points[0]), (self.points[2] - self.points[0]))
        magN = np.sqrt(np.square(n[0]) + np.square(n[1]) + np.square(n[2]))
        return(n / magN)
    
#    def rotateNHat(self, q):
#        self.nHat = quat.quaternion_rotate(self.nHat, q)
    
    def calcForceResistive(self, vel, denAir, mAir, theta):
#        vel = -vel
        nHat = self.rotate(theta, self.nHat)

        velMag = np.sqrt(np.square(vel[0]) + np.square(vel[1]) + np.square(vel[2]))
        #think about this small number
        if (velMag <= 1e-8):
            velHat = np.array((0., 0., 0.))
        else:    
            velHat = vel / velMag
        dot = np.dot(velHat, nHat)
        
        if (self.verbose == True):
            print("In calcForceResistive, vel={}, nHat={}".format(vel, nHat))
        
        if dot <= 0:
            return np.zeros(3)
        
        useableArea = (self.area * dot)
        numParticles = useableArea * (self.dt * velMag) * denAir
        dpp = -2 * velMag * np.dot(velHat, nHat) * nHat * mAir * numParticles
        


        
        return (dpp / self.dt)
    
    
    def rotate(self, theta, xy):
        return (np.array((((xy[0] * np.cos(theta)) - (xy[1] * np.sin(theta))), 
                         ((xy[0] * np.sin(theta)) + (xy[1] * np.cos(theta))), 0)))
    
    def mag(self, r):
        R = 0
        for i in range(len(r)):
            R += np.square(r[i])
        return np.sqrt(R)