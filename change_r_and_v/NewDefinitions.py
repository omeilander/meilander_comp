# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 21:48:43 2020

@author: omeil
"""
import numpy as np

"""
NEED TO FIGURE OUT THE FOLLOWING:
1. How to calc the lhat vector for quat
2. How to get d/dt of tensor? 
    Is is just replacing x, y, and z with their dots (just omega component)??
    Chain rule on xy, xz, yz??
"""


def calcTensor(panes, CM):
    xx = 0
    yy = 0
    zz = 0
    xy = 0
    xz = 0
    yz = 0
    
    for i in len(range(panes)):
        r = panes[i].CM - CM
        
        xx += panes[i].mass * (np.square(r[1]) + np.square(r[2]))
        yy += panes[i].mass * (np.square(r[0]) + np.square(r[2]))
        zz += panes[i].mass * (np.square(r[0]) + np.square(r[1]))
        xy += panes[i].mass * r[0] * r[1]
        xz += panes[i].mass * r[0] * r[2]
        yz += panes[i].mass * r[1] * r[2]
    
    return(np.array(((xx, -xy, -xz)
                     (-xy, yy, -yz)
                     (-xz, -yz, zz))))
        
def calcDTensor(panes, CM, omega):
    xx = 0
    yy = 0
    zz = 0
    xy = 0
    xz = 0
    yz = 0
    
    for i in len(range(panes)):
        r = panes[i].CM - CM
        v = np.cross(omega, r)
        
        xx += panes[i].mass * (np.square(v[1]) + np.square(v[2]))
        yy += panes[i].mass * (np.square(v[0]) + np.square(v[2]))
        zz += panes[i].mass * (np.square(v[0]) + np.square(v[1]))
        xy += panes[i].mass * v[0] * v[1]
        xz += panes[i].mass * v[0] * v[2]
        yz += panes[i].mass * v[1] * v[2]
        """
        xy += panes[i].mass * (r[0] * v[1] + v[0] * r[1])
        xz += panes[i].mass * (r[0] * v[2] + v[0] * r[2])
        yz += panes[i].mass * (r[1] * v[2] + v[1] * r[2])
        """
                
    
def calcAlpha(panes, CM, torque, omega):
    ten = calcTensor(panes, CM)
    tenInv = invert3by3(ten)
    dTen = calcDTensor(panes, CM, omega)
    return(matrixMult(tenInv, torque) - matrixMult(matrix3by3Mult(tenInv, dTen), omega))
    
def invert3by3(a):
    return(np.linalg.inv(a))
    
def matrixMult(A, x):
    y0 = A[0, 0] * x[0] + A[0, 1] * x[1] + A[0, 2] * x[2]
    y1 = A[1, 0] * x[0] + A[1, 1] * x[1] + A[1, 2] * x[2]
    y2 = A[2, 0] * x[0] + A[2, 1] * x[1] + A[2, 2] * x[2]
    
    return(np.array((y0, y1, y2)))
    
def matrix3by3Mult(A, B):
    y00 = A[0, 0] * B[0, 0] + A[0, 1] * B[1, 0] + A[0, 2] * B[2, 0]
    y10 = A[1, 0] * B[0, 0] + A[1, 1] * B[1, 0] + A[1, 2] * B[2, 0]
    y20 = A[2, 0] * B[0, 0] + A[2, 1] * B[1, 0] + A[2, 2] * B[2, 0]
    y01 = A[0, 0] * B[0, 1] + A[0, 1] * B[1, 1] + A[0, 2] * B[2, 1]
    y11 = A[1, 0] * B[0, 1] + A[1, 1] * B[1, 1] + A[1, 2] * B[2, 1]
    y21 = A[2, 0] * B[0, 1] + A[2, 1] * B[1, 1] + A[2, 2] * B[2, 1]
    y02 = A[0, 0] * B[0, 2] + A[0, 1] * B[1, 2] + A[0, 2] * B[2, 2]
    y12 = A[1, 0] * B[0, 2] + A[1, 1] * B[1, 2] + A[1, 2] * B[2, 2]
    y22 = A[2, 0] * B[0, 2] + A[2, 1] * B[1, 2] + A[2, 2] * B[2, 2]
    
    return (np.array(((y00, y01, y02), (y10, y11, y12), (y20, y21, y22))))

"""from Object"""    
def dvals_dt(self, t, vals):
    ders = np.empty(12)
    ders[0:3] = vals[3:6]
    ders[6:9] = vals[9:]
    l = calcL()
    self.quat = quat.create_quaternion(vals[6:9], l)

    force = self.forceTot(vals[3:6], vals[6])
    ders[3:6] = force / self.mTot()
    
    torque = T = self.torResistiveTot(vals[3:6])
    
    alpha = calcAlpha(self.panes, self.CM, torque, vals[9:])
    
    ders[9:] = alpha
    if (self.verbose == True):
        print("theta = {:.3g} and omega = {:.3g} T = {:.3g}\n".format(vals[6:9], vals[9:], T,))
    
    return ders

"""from Object"""
def torResistiveTot(self, v):
    torTot = np.array((0., 0., 0.))
    for i in range(len(self.panes)):
        r = self.rotate(self.panes[i].CM - self.CMTot, self.quat)
        f = self.panes[i].calcForceResistive(v, self.air.denAir(self.CMTot[1]), 
                  self.air.mAir)
        tor = np.cross(r, f)
        torTot += tor
        if (self.verbose == True):
            print("pane {}: CM = {}  CMTot = {}".format(i, self.panes[i].CM, self.CMTot))
            print("pane {}: r = {}, f = {}, tor = {}, torTot = {}\n".format(i, r, f, tor, torTot))
    return torTot    
    
"""from Object"""
def forceResistiveTot(self, v):
    fTot = np.zeros(3)
    
    for i in range(len(self.panes)):
        f = self.panes[i].calcForceResistive(v, 
                          self.air.denAir(self.CMTot[1]), self.air.mAir, self.quat)
        fTot += f
        if (self.verbose == True):
            print("f resistive Tot = {} on pane {}".format(f, i))
    return fTot     

"""from Pane"""    
def calcForceResistive(self, vel, denAir, mAir, quat):
    nHat = self.rotate(self.nHat, quat)
    
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
    