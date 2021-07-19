# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 20:39:24 2020

@author: avenkatraman31

Skip to main block to make sense of these keywords
"""
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 19:43:16 2020

@author: avenkatraman31
"""

def aij(theta):
    from numpy import pi,cos,sqrt
    th=theta;
    th=th*pi/180;
    d11=cos(th-pi/3);
    d22=cos(th+pi/3);
    d33=-cos(th);
    
    Dtensor=sqrt(2/3)*np.array([[d11, 0 ,0],[ 0, d22, 0],[0, 0 ,d33]])
    return Dtensor
def dispcalc(strain,length):
    return (np.exp(strain)-1)*length

def displacementwriter(defmode,totalstrain,domain,timesteps=20):
    import numpy as np
    
    l0=domain# %initial length
    n=timesteps# %number of time steps, 2 for delta MS 20 for random MS
    strains=np.linspace(0,totalstrain,n)
    magnitude=1# %for validation of rate dependent
    
    
    Dij=aij(defmode)*l0*totalstrain*magnitude#; %desired strain rate tensor, for hardening case we will go all the way to 2% strain
    # How to extract the magnitude of the tensor
    
    
    
    
    eij=Dij#; %since simulation lasts one second eij=Dij;
    
    e11=eij[0,0];
    e22=eij[1,1];
    e33=eij[2,2];
    
    e= np.array([ e11 ,e22 ,e33])/l0#; %this to normalize by the length
    
    d1m=dispcalc((e11/l0),l0)#; %to normalize by the length
    d2m=dispcalc((e22/l0),l0)#; %to normalize by the length
    d3m=dispcalc((e33/l0),l0)#; %to normalize by the length
    
    dm=np.array([ d1m, d2m, d3m])
    
    amp=np.zeros((n,3))    
    for i in range(n):
        strain=strains[i]
    
        Dij=aij(defmode)*l0*strain*magnitude#; %desired strain rate tensor, for hardening case we will go all the way to 2% strain
    # How to extract the magnitude of the tensor
    
    
    
    
        eij=Dij#; %since simulation lasts one second eij=Dij;
    
        e11=eij[0,0];
        e22=eij[1,1];
        e33=eij[2,2];
        
        e= np.array([ e11 ,e22 ,e33])/l0#; %this to normalize by the length
        
        d1f=dispcalc((e11/l0),l0)#; %to normalize by the length
        d2f=dispcalc((e22/l0),l0)#; %to normalize by the length
        d3f=dispcalc((e33/l0),l0)#; %to normalize by the length
        
        d=np.array([ d1f, d2f, d3f])
        for j in range(3):
            if(dm[j]==0): 
                amp[i,j]=0
            else:
                amp[i,j]=d[j]/dm[j]    
    
    
    ampx='\n*Amplitude,name=ampx,definition=TABULAR\n'
    ampy='*Amplitude,name=ampy,definition=TABULAR\n'
    ampz='*Amplitude,name=ampz,definition=TABULAR\n'
    return dm,amp,ampx,ampy,ampz


        
if __name__=="__main__":
    '''
    system arguments 1,2 -->  number of elements per side , domain size

    '''
    import numpy as np
    from numpy import pi,cos,sin,arcsin,arccos,arctan2,sqrt,arctan
    from shutil import copyfile
    import numpy as np
    import scipy.io as sio
    from subprocess import call 
    import sys
    atan2=arctan2
    asin=arcsin
    acos=arccos
    #Defining number of elements, no. of nodes, domain size, indenter radius , domain discretization
    ndim=21#int(sys.argv[1])
    defmode=0
    totalstrain=0.5
    timesteps=101
    domain=2.1#float(sys.argv[2])
    nnode=np.copy(ndim)+1
    domain_discrete=np.linspace(0,domain,nnode)
    #Creating 3-D mesh grid of points and retrieving nodeset and elset
    x,y,z=np.meshgrid(domain_discrete,domain_discrete,domain_discrete,indexing='xy')
    node_indx=np.arange(1,nnode**3+1).astype('int')
    nodes=np.column_stack([x.ravel(),y.ravel(),z.ravel()])
    node_line='!\n coordinates\n *echo off\n'
    for i in range(nnode**3):
        node_line +='%d %7.3f %7.3f %7.3f\n'%(node_indx[i],nodes[i,0],nodes[i,1],nodes[i,2])
    elset_3d=np.reshape(np.arange(1,ndim**3+1),(ndim,ndim,ndim))
    nset_3d=np.reshape(np.arange(1,nnode**3+1),(nnode,nnode,nnode))
    #Corners
    corners=np.array([nset_3d[0,0,0],\
                      nset_3d[-1,0,0],\
                      nset_3d[-1,-1,0],\
                      nset_3d[0,-1,0],\
                      nset_3d[0,0,-1],\
                      nset_3d[-1,0,-1],\
                      nset_3d[-1,-1,-1],\
                      nset_3d[0,-1,-1],\
                      ])
    
    #Instantiating element array and defining connectivities for the continuum elements zone
    elements=np.ndarray([ndim**3, 9],dtype=np.int32)
    element_line="*echo on\n incidences\n*echo off"
    index=0
    
    for i in range(ndim):
        for j in range(ndim):
            for k in range(ndim):
                elements[index,:]=np.array([index,\
                                            j+i*nnode+k*nnode**2,\
                                            j+1+i*nnode+k*nnode**2,\
                                            j+1+(i+1)*nnode+k*nnode**2,\
                                            j+(i+1)*nnode+k*nnode**2,\
                                            j+i*nnode+(k+1)*nnode**2,\
                                            j+1+i*nnode+(k+1)*nnode**2,\
                                            j+1+(i+1)*nnode+(k+1)*nnode**2,\
                                            j+(i+1)*nnode+(k+1)*nnode**2])
                element_line +=' '.join(str(elements[index,:]+1)[1:-1].split())
                element_line +='\n'
                index=index+1
    elements=elements+1
    element_line +="*echo on\n"

    inpfile="rve_%dum_%delem.inp"%(domain,ndim)
    f=open(inpfile,'w')

    f.write(node_line)
    
    f.write(element_line)
    

    


#    node_connect=[]
#    for i in range(nnode**3):
#        ncon=np.argwhere(elements[:,1:]==i+1)[:,0]+1
#        assert len(ncon)
#        node_connect.append(ncon)
#    node_connect_array=np.zeros((nnode**3,8),dtype=np.int32)
#    node_lcon=np.zeros((nnode**3,),dtype=np.int32)
#    for i in range(nnode**3):
#        ncon=node_connect[i]
#        lcon=len(node_connect[i])
#        node_connect_array[i,:lcon]=node_connect[i]
#        node_lcon[i]=lcon
#    node_connect=np.column_stack([node_indx.reshape((-1,1)), \
#                                  node_lcon.reshape((-1,1)),\
#                                  node_connect_array])
#    f=open("rve_%delem_connectivity.inp"%(ndim),'w')
#    np.savetxt(f,node_connect,delimiter=',',fmt='%d')
#    f.close()
        
    '''
    Extra stuff used for tests: ABAQUS doesn't accept parameterized inputs in CAE
c1, 1, 1,0\n\
c1, 2, 2,0\n\
c1, 3, 3,0\n\
c2, 1, 1,0\n\
c2, 2, 2,0\n\
c2, 3, 3,0\n\
c3, 1, 1,0\n\
c3, 2, 2,0\n\
c3, 3, 3,0\n\
c4, 1, 1,0\n\
c4, 2, 2,0\n\
c4, 3, 3,0\n\
c5, 1, 1,0\n\
c5, 2, 2,0\n\
c5, 3, 3,0\n\
c6, 1, 1,0\n\
c6, 2, 2,0\n\
c6, 3, 3,0\n\
c7, 1, 1,0\n\
c7, 2, 2,0\n\
c7, 3, 3,0\n\
c8, 1, 1,0\n\
c8, 2, 2,0\n\
c8, 3, 3,0\n\

    '''