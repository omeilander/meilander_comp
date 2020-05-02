# -*- coding: utf-8 -*-c

"""
Created on Wed Jan 29 20:34:22 2020

@author: omeil
"""
import numpy as np
from Pane import Pane as Pain
from Air import Air
from Object import Object
from FuelTank import FuelTank
from RungeKutter import RungeKutter
from matplotlib import pyplot as plt


def main():
    den = 1
    thick = .1
    dt = .01
    r = np.array((0., 0., 0.))
    vo = np.array((0., 0., 0.))
    
    fuelCM = np.array((1., 1., 1.))
    mf = 10.
    burnTime = 60.
    thrust = 112.
    fuel = FuelTank(fuelCM, mf, burnTime, thrust)
    
    points = np.empty((9,3))
    points[0] = np.array((0., 0., 0.))
    points[1] = np.array((2., 0., 0.))
    points[2] = np.array((2., 2., 0.))
    points[3] = np.array((0., 2., 0.))
    points[4] = np.array((0., 0., 2.))
    points[5] = np.array((2., 0., 2.))
    points[6] = np.array((2., 2., 2.))
    points[7] = np.array((0., 2., 2.))
    points[8] = np.array((1., 3., 1.))
    
    '''
    pains = np.empty(14)
    pains[0] = Pain(np.array((points[0], points[1], points[2])), den, thick, dt)
    pains[1] = Pain(np.array((points[1], points[3], points[2])), den, thick, dt)
    pains[2] = Pain(np.array((points[1], points[2], points[5])), den, thick, dt)
    pains[3] = Pain(np.array((points[5], points[6], points[1])), den, thick, dt)
    pains[4] = Pain(np.array((points[5], points[6], points[4])), den, thick, dt)
    pains[5] = Pain(np.array((points[4], points[7], points[6])), den, thick, dt)
    pains[6] = Pain(np.array((points[4], points[7], points[0])), den, thick, dt)
    pains[7] = Pain(np.array((points[0], points[7], points[3])), den, thick, dt)
    pains[8] = Pain(np.array((points[0], points[1], points[5])), den, thick, dt)
    pains[9] = Pain(np.array((points[0], points[5], points[4])), den, thick, dt)
    pains[10] = Pain(np.array((points[8], points[7], points[6])), den, thick, dt)
    pains[11] = Pain(np.array((points[8], points[6], points[2])), den, thick, dt)
    pains[12] = Pain(np.array((points[8], points[2], points[3])), den, thick, dt)
    pains[13] = Pain(np.array((points[8], points[3], points[7])), den, thick, dt)
    '''
    
    pains = []
    pains.append(Pain(np.array((points[0], points[1], points[2])), den, thick, dt))
    pains.append(Pain(np.array((points[1], points[3], points[2])), den, thick, dt))
    pains.append(Pain(np.array((points[1], points[2], points[5])), den, thick, dt))
    pains.append(Pain(np.array((points[5], points[6], points[1])), den, thick, dt))
    pains.append(Pain(np.array((points[5], points[6], points[4])), den, thick, dt))
    pains.append(Pain(np.array((points[4], points[7], points[6])), den, thick, dt))
    pains.append(Pain(np.array((points[4], points[7], points[0])), den, thick, dt))
    pains.append(Pain(np.array((points[0], points[7], points[3])), den, thick, dt))
    pains.append(Pain(np.array((points[0], points[1], points[5])), den, thick, dt))
    pains.append(Pain(np.array((points[0], points[5], points[4])), den, thick, dt))
    pains.append(Pain(np.array((points[8], points[7], points[6])), den, thick, dt))
    pains.append(Pain(np.array((points[8], points[6], points[2])), den, thick, dt))
    pains.append(Pain(np.array((points[8], points[2], points[3])), den, thick, dt))
    pains.append(Pain(np.array((points[8], points[3], points[7])), den, thick, dt))
    
    air = Air(vo, r)
    
    pointy = Object(pains, air, fuel, dt)
    
    rk4 = RungeKutter(pointy)
    sols = rk4.solve(30., nkeep=3000)
    
    #Fr = pointy.fResistive_List
    
    fig, ax = plt.subplots(2,2)
    
    ax[0,0].plot(sols[:,0], -sols[:,2], linestyle="-", marker="",markersize=10, color="red")
    ax[0,1].plot(sols[:,0], -sols[:,5], linestyle="-", marker="",markersize=10, color="red")
    ax[1,0].plot(pointy.tList[:-1], pointy.fResistive_List, linestyle="-", marker="", color="blue" )
    ax[1,1].plot(pointy.tList[:-1], pointy.fTot_List, linestyle="-", marker="", color="black" )

    ax[0,0].set_xlabel("t", fontsize=18)
    ax[0,0].set_ylabel("y", fontsize=18)
    ax[0,1].set_xlabel("t", fontsize=18)
    ax[0,1].set_ylabel("vy", fontsize=18)
    ax[1,0].set_xlabel("t", fontsize=18)
    ax[1,0].set_ylabel("Fresistive", fontsize=18)
    ax[1,1].set_xlabel("t", fontsize=18)
    ax[1,1].set_ylabel("Ftot", fontsize=18)
    fig.set_tight_layout(True)
    #plt.ylim(-2,2)
    #plt.xlim(2600, 2800)
    
#     ax.tick_params(labelsize=14)
#     ax.set_title("phi vs t", fontsize=20)
#     fig.set_tight_layout(True)
    
    fig.show()
    plt.show()


#=========================================================
if __name__== "__main__":
    main() 