# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 19:01:52 2020

@author: omeil
"""

import numpy as np
from Pane import Pane as Pain
from Air import Air
from Object import Object
#from imgointtomessup import Object
from FuelTank import FuelTank
from RungeKutterSpecial import RungeKutter
from matplotlib import pyplot as plt


def main():
    verbose = False
#    verbose = True
    
    den = 1
    thick = .1
    dt = .01
    r_air = np.array((0., 0., 0.))
    v_air = np.array((0., 0., 0.))
    v0 = np.array((0., 0., 0.))
    ang = np.array((.1, 0.))
    
    mf = 10.
    burnTime = 60.
    thrust = 118.
    
    pains, fuelCM = maybegood(den, thick, dt, verbose)
    
    fuel = FuelTank(fuelCM, mf, burnTime, thrust)

    air = Air(v_air, r_air)
    
    pointy = Object(pains, air, fuel, v0, dt, ang, verbose)
    
    rk4 = RungeKutter(pointy)
    sols = rk4.solve(10, nkeep=30000)
    
    #Fr = pointy.fResistive_List
    
    fig, ax = plt.subplots(2,2)
    
    ax[0,0].plot(sols[:,0], sols[:,2], linestyle="-", marker="",markersize=10, color="red")
    ax[0,1].plot(sols[:,0], sols[:,5], linestyle="-", marker="",markersize=10, color="red")
    ax[1,0].plot(sols[:,0], sols[:,7], linestyle="-", marker="", color="blue" )
    ax[1,1].plot(sols[:,0], sols[:,8], linestyle="-", marker="", color="black" )
#==============================================================================
#     ax[1,0].plot(pointy.tList[:-1], pointy.fResistive_List, linestyle="-", marker="", color="blue" )
#     ax[1,1].plot(pointy.tList[:-1], pointy.fTot_List, linestyle="-", marker="", color="black" )
#==============================================================================

    ax[0,0].set_xlabel("t", fontsize=18)
    ax[0,0].set_ylabel("y", fontsize=18)
    ax[0,1].set_xlabel("t", fontsize=18)
    ax[0,1].set_ylabel("vy", fontsize=18)
    ax[1,0].set_xlabel("t", fontsize=18)
    ax[1,0].set_ylabel("theta", fontsize=18)
    ax[1,1].set_xlabel("t", fontsize=18)
    ax[1,1].set_ylabel("omega", fontsize=18)
    fig.set_tight_layout(True)
    #plt.ylim(-2,2)
    #plt.xlim(2600, 2800)
    
#     ax.tick_params(labelsize=14)
#     ax.set_title("phi vs t", fontsize=20)
#     fig.set_tight_layout(True)
    
    fig.show()
    plt.show()



    
    
def badstuff(den, thick, dt, verbose):  
    fuelCM = np.array((0., 0.5, 0.))
    points = np.empty((9,3))
    points[0] = np.array((0., 2., 0.))
    points[1] = np.array((1., 1., 1.))
    points[2] = np.array((1., 1., -1.))
    points[3] = np.array((1., 0., 0.))
    points[4] = np.array((-1., 1., 1.))
    points[5] = np.array((-1., 1., -1.))
    points[6] = np.array((-1., 0., 0.))
        
        
    pains = []
    pains.append(Pain(np.array((points[0], points[1], points[2])), den, thick, dt, verbose))
    pains.append(Pain(np.array((points[1], points[3], points[2])), den, thick, dt, verbose))
    pains.append(Pain(np.array((points[0], points[5], points[4])), den, thick, dt, verbose))
    pains.append(Pain(np.array((points[4], points[5], points[6])), den, thick, dt, verbose))
    return(pains, fuelCM)
        
def maybegood(den, thick, dt, verbose):
    fuelCM = np.array((0., 3., 0.))
    
    points = np.empty((11,3))
    points[0] = np.array((0., 4., 0.))
    points[1] = np.array((1., 1., 1.))
    points[2] = np.array((1., 1., -1.))
    points[3] = np.array((1., 0., 0.))
    points[4] = np.array((-1., 1., 1.))
    points[5] = np.array((-1., 1., -1.))
    points[6] = np.array((-1., 0., 0.))
    points[7] = np.array((-2., -1., 3.))
    points[8] = np.array((-2., -1., -3.))
    points[9] = np.array((2., -1., 3.))
    points[10] = np.array((2., -1., -3.))
    
        
        
    pains = []
    pains.append(Pain(np.array((points[0], points[1], points[2])), den, thick, dt, verbose))
    pains.append(Pain(np.array((points[1], points[3], points[2])), den, thick, dt, verbose))
    pains.append(Pain(np.array((points[0], points[5], points[4])), den, thick, dt, verbose))
    pains.append(Pain(np.array((points[4], points[5], points[6])), den, thick, dt, verbose))
    pains.append(Pain(np.array((points[6], points[8], points[7])), den, thick, dt, verbose))
    pains.append(Pain(np.array((points[3], points[9], points[10])), den, thick, dt, verbose))
    return(pains, fuelCM)
    
    
    #=========================================================
if __name__== "__main__":
    main() 
    