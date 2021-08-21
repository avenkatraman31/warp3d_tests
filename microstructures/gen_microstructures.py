# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 21:34:53 2020

@author: vadit
"""
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
if __name__=="__main__":
    import tables 
    import subprocess
    from subprocess import call,run
    import os
    import numpy as np
    from scipy.ndimage import gaussian_filter
    import scipy.io as sio
    import dask.array as da
    from dask.distributed import Client,wait
    import platform
    
    nsample=10
    FNULL = open(os.devnull, 'w')
    pipe=os.getcwd()+os.sep+"hcp.json"
    file='EulerAngles.txt'
    for j in range(nsample):
        
        if(platform.system()=='Windows'): pipe="hcp.json"
        runPipe = "PipelineRunner -p %s" %(pipe)
        
        run(runPipe,shell=True,check=True)
        f=open(file,'r')
        eulers=np.loadtxt(f,delimiter=',')
        eulers=eulers*180/np.pi
        eulers=np.apply_along_axis(conv_switch,1,eulers)
        eulers=np.column_stack([\
               np.arange(1,eulers.shape[0]+1).reshape((-1,1)),\
               eulers])
        eulers=eulers.repeat(2,axis=0)
        wfile=file.replace('EulerAngles','angles-%04d'%(j+1))
        wfile=wfile.replace('.txt','.inp')
        w=open(wfile,'w')
        np.savetxt(w,eulers,delimiter=',',fmt=['%d','%6.3f','%6.3f','%6.3f'])
        w.close()    
        f.close()