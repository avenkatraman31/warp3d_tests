# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 02:10:10 2021

@author: vadit
This python code has two modules
1. one that cvonverts directions and normals to euler angles
2. Converts kocks to bunge and vice-versa

This code is used to read EulerAngles-..txt files spit out by dream-3d and 
convert them into kocks convention and degrees

"""

import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from matplotlib import rc
from mpl_toolkits.mplot3d import Axes3D
from numpy import arctan2, arccos, arctan
b=np.array([1,1,2,0])
n=np.array([0,0,0,1])
def dir_to_euler(b,n,kocks=True):
    b3=np.zeros((3,))
    n3=np.zeros((3,))
    covera=0.495/0.28
    n3[0]=n[0]
    n3[1]=(n[0]+2*n[1])/3**0.5
    n3[2]=n[3]/covera
    b3[0]=3/2*b[0]
    b3[1]=(b[0]/2+1*b[1])*3**0.5
    b3[2]=b[3]*covera
    snm=np.sqrt(n3[0]**2+n3[1]**2+n3[2]**2)
    sdm=np.sqrt(b3[0]**2+b3[1]**2+b3[2]**2) 
    n3[:]=n3[:]/snm
    b3[:]=b3[:]/sdm
    t3=np.cross(b3,n3)
    rotmat=np.array([b3,n3,t3])
    psi=arctan2(rotmat[2,1],rotmat[2,0])*180/np.pi
    phi=arctan2(rotmat[1,2],rotmat[0,2])*180/np.pi
    if psi < 0: psi=psi+360
    if phi <0:phi=phi+360
    theta=arccos(rotmat[2,2])*180/np.pi
    phi1=psi+90
    phiphi=theta
    phi2=90-phi
    if phi1 > 360: phi1=phi1-360
    if phi2 < 0: phi2 = phi2+360
    if(kocks): 
        return np.array([psi,theta,phi])
    else:
        return np.array([phi1,phiphi,phi2])

def conv_switch(euler,kocks=False,degree=True):
    if(degree): 
        pi=180
    else:
        pi=np.pi
    if(kocks):#kocks to bunge
        phi1=euler[0]+pi/2
        phiphi=euler[1]
        phi2=pi/2-euler[2]  
        if phi1 > 2*pi: phi1=phi1- 2*pi
        if phi2 < 0: phi2 = phi2+ 2*pi        
        return np.array([phi1,phiphi,phi2])
    else:#bunge to kocks
        psi=euler[0]-pi/2
        theta=euler[1]
        phi=pi/2-euler[2]
        if psi < 0: psi=psi+360
        if phi <0:phi=phi+360
        return np.array([psi,theta,phi])
eulerfiles=[]

for file in os.listdir(os.getcwd()):
    if file.startswith('EulerAngles') and file.endswith('.txt'): 
        eulerfiles.append(file)
eulerfiles=sorted(eulerfiles)

for file in eulerfiles:
    f=open(file,'r')
    eulers=np.loadtxt(f,delimiter=',')
    eulers=eulers*180/np.pi
    eulers=np.apply_along_axis(conv_switch,0,eulers)
        