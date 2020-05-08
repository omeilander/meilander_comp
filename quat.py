#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is a multi-use quaternion manipulation 
program for continuing use for 3D rotations. 

Code sourced from Physvis
"""
#==============================================================================
import numpy
    
def create_quaternion(theta, l):
    theta_mag = numpy.sqrt(numpy.square(theta[0]) + numpy.square(theta[1]) + numpy.square(theta[2]))
    xhat = numpy.array((1, 0, 0))
    yhat = numpy.array((0, 1, 0))
    zhat = numpy.array((0, 0, 1))
    
    a = numpy.cross(l, zhat)
    
    one = numpy.sin(theta_mag / 2) * (numpy.dot(a, xhat))
    two = numpy.sin(theta_mag / 2) * (numpy.dot(a, yhat))
    three = numpy.sin(theta_mag / 2) * (numpy.dot(a, zhat))
    four = numpy.cos(theta_mag / 2)
    return (numpy.array((one, two, three, four)))


def quaternion_multiply(p, q):
    """Multiply a vector or quaternion p by a quaternion q.

    If p is a quaternion, the returned quaternion represents rotation q followed by rotation p
    """

    if len(p) == 3:
        px, py, pz = p
        pr = 0.
    else:
        px, py, pz, pr = p
    qx, qy, qz, qr = q
    return numpy.array( [ pr*qx + px*qr + py*qz - pz*qy,
                          pr*qy - px*qz + py*qr + pz*qx,
                          pr*qz + px*qy - py*qx + pz*qr,
                          pr*qr - px*qx - py*qy - pz*qz ] , dtype=numpy.float32 )

def quaternion_rotate(p, q):
    """Rotate vector p by quaternion q."""
    qinv = q.copy()
    qinv[0:3] *= -1.
    return quaternion_multiply(q, quaternion_multiply(p, qinv))[0:3]

