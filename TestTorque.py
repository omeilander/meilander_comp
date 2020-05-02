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
    verbose = 0
    
    den = 1
    thick = .1
    dt = .01
    r = np.array((0., 0., 0.))
    vo = np.array((0., 0., 0.))
    ang = np.array((.5, 0.))

    tend = 10.
    burnTime = 60.
    # burnTime = 60.
    # thrust = 118.
    # thrust = 180.
    
    pains, fuelCM, frameCM, framemass = maybegood(den, thick, dt, verbose)
    print("Out of maybegood, fuelCM={}, frameCM={}, framemass={}".format(fuelCM, frameCM, framemass))
    
    mf = 2. * framemass
    thrust = 1.05 * (framemass + mf) * 9.8

    painvis = None
    
    import PainVisualizer
    painvis = PainVisualizer.PaneVisualizer(pains)
    painvis.show()
    
    fuel = FuelTank(fuelCM, mf, burnTime, thrust)

    air = Air(vo, r)
    
    pointy = Object(pains, air, fuel, dt, ang, verbose)

    print("Initialized rocket.  Structure mass = {:.3g}, fuel mass = {:.3g}, tot mass = {:.3g}"
          .format(framemass, fuel.mf, pointy.mTot()))
    CMframe = pointy.calcCMTotPane()
    CMtot = pointy.calcCMTot()
    print("CoM of structure: [{:.3g}, {:.3g}, {:.3g}], overall: [{:.3g}, {:.3g}, {:.3g}]"
          .format(CMframe[0], CMframe[1], CMframe[2], CMtot[0], CMtot[1], CMtot[2]))
    
    rk4 = RungeKutter(pointy, verbose=verbose)
    sols = rk4.solve(tend, nkeep=3000)

    if painvis is not None:
        lastsols = sols[-1]
        v = np.array( lastsols[4:7] )
        theta = lastsols[7]
        omega = lastsols[8]
        painvis.vectorify(pointy, v, theta, omega)
        
    
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
    fuelCM = np.array((0., 1., 0.))
    
    points = np.empty((11,3))
    points[0] = np.array((0., 20., 0.))
    points[1] = np.array((1., 1., 1.))
    points[2] = np.array((1., 1., -1.))
    points[3] = np.array((1., 0., 0.))
    points[4] = np.array((-1., 1., 1.))
    points[5] = np.array((-1., 1., -1.))
    points[6] = np.array((-1., 0., 0.))
    points[7] = np.array((-4., -5., 3.))
    points[8] = np.array((-4., -5., -3.))
    points[9] = np.array((4., -5., 3.))
    points[10] = np.array((4., -5., -3.))
    
        
        
    pains = []
    pains.append(Pain(np.array((points[0], points[1], points[2])), den, thick, dt, verbose))
    pains.append(Pain(np.array((points[1], points[3], points[2])), den, thick, dt, verbose))
    pains.append(Pain(np.array((points[0], points[5], points[4])), den, thick, dt, verbose))
    pains.append(Pain(np.array((points[4], points[5], points[6])), den, thick, dt, verbose))
    pains.append(Pain(np.array((points[6], points[8], points[7])), den, thick, dt, verbose))
    pains.append(Pain(np.array((points[3], points[9], points[10])), den, thick, dt, verbose))

    CM = np.array( [0., 0., 0.] )
    totmass = 0.
    for pain in pains:
        CM += pain.calcCM() * pain.calcMass()
        totmass += pain.calcMass()
    CM /= totmass

    # fuelCM = CM
    fuelCM = np.array( [0., 0., 0.] )
    
    return(pains, fuelCM, CM, totmass)
    
    
    #=========================================================
if __name__== "__main__":
    main() 
    
