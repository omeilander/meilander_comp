#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
This file is a part of mei_comp_2020

This file creates a physvis object to diplay the object, its torques, 
and its velocities.

Requires the use of numpy and physvis.
"""
#==============================================================================
import sys
import math
import numpy
import physvis as vis

class PaneVisualizer(object):
    def __init__(self, panes):
        nfaces = len(panes)
        self.vertices = numpy.empty( [3*nfaces, 3] )
        for i in range(nfaces):
            # import pdb; pdb.set_trace()
            self.vertices[3*i+0, :] = panes[i].points[0]
            self.vertices[3*i+1, :] = panes[i].points[1]
            self.vertices[3*i+2, :] = panes[i].points[2]

    def show(self):
        import physvis as vis
        self.faces = vis.faces(self.vertices, color = [1, 1, 1])

        # Right now I'm depending on the fact that physvis will
        #  still give the user the ability to rotate, etc.
        #  even if we don't do a "rate" statemet.  This works
        #  because the GLUT version of physvis starts up
        #  its own thread.  Pause first, though, because
        #  once the program is going full tilt, the GLUT
        #  thread won't get any time.

        sys.stderr.write("Press ENTER to continue:")
        sys.stderr.flush()
        junk = sys.stdin.readline()

    def vectorify(self, obj, v, theta, omega):

        self.faces.rotate(theta, [0., 0., 1.])
        
        fr = []
        for pain in obj.panes:
            fr.append(pain.calcForceResistive(v, obj.air.denAir(obj.CMTot[1]), obj.air.mAir, theta))
        fr = numpy.array(fr)
        magfr = numpy.sqrt( numpy.square(fr).sum(axis=1) )
        maxmagfr = max(magfr)
        minx = min(self.vertices[:, 0])
        maxx = max(self.vertices[:, 0])
        miny = min(self.vertices[:, 1])
        maxy = max(self.vertices[:, 1])
        minz = min(self.vertices[:, 2])
        maxz = max(self.vertices[:, 2])
        size = max( (maxx-minx), (maxy-miny), (maxz-minz) )
        fr *= 0.2*size/maxmagfr
        magfr *= 0.2*size/maxmagfr

        rotv = obj.rotate(theta, v)
        rotv *= 0.2 * size / math.sqrt( (rotv*rotv).sum() )
        vis.arrow( axis=rotv, color=[0., 1., 0.], fixedwidth=True )
        
        for i in range(len(obj.panes)):
            if magfr[i] > 0.01:
                pos = obj.rotate(theta, obj.panes[i].calcCM())
                vis.arrow( pos=pos - fr[i], axis=fr[i], fixedwidth=True, color=[1., 1., 0.] )

        frtot = obj.forceResistiveTot(v, theta)
        ftot = obj.forceTot(v, theta)
        torque = obj.torResistiveTot(v, theta)

        sys.stderr.write("\nResistive Force: [{:.3g}, {:.3g}, {:.3g}]\n"
                         .format(frtot[0], frtot[1], frtot[2]))
        sys.stderr.write("Total Force: [{:.3g}, {:.3g}, {:.3g}]\n"
                         .format(ftot[0], ftot[1], ftot[2]))
        sys.stderr.write("Torque: [{:.3g}, {:.3g}, {:.3g}]\n"
                         .format(torque[0], torque[1], torque[2]))

                
        sys.stderr.write("Press ENTER to continue:")
        sys.stderr.flush()
        junk = sys.stdin.readline()
        
