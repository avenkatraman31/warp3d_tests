# -*- coding: utf-8 -*-
"""
Created on Mon Aug 01 20:31:58 2021

@author: vadit

1. Just copy this file in any folder with warp3d flat results files to get stress strain curves
2. adjust the number of elements 'nel' accordingly; its preferable to get element stress-strain results as they are 
   direct averages of gauss point values
3. 
"""
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from matplotlib import rc
from mpl_toolkits.mplot3d import Axes3D  
import scipy.io as sio

nel=9261
stress_files=[]
strain_files=[]

for file in os.listdir(os.getcwd()):
    if (file.startswith('wes')):
        stress_files.append(file)
    if(file.startswith('wee')):
        strain_files.append(file)
stress_files=sorted(stress_files)
strain_files=sorted(strain_files)

if nel==1:
    strain=np.zeros((len(strain_files),6))
    stress=np.zeros_like(strain)
else:
    strain=np.zeros((nel,len(strain_files),6))
    stress=np.zeros_like(strain)


for ii,(file1,file2) in enumerate(zip(strain_files,stress_files)):
    f1=open(file1,'r')
    f2=open(file2,'r')
    if nel==1:
        for _ in range(7):
            f1.readline()
            f2.readline()
        strain[ii,:],stress[ii,:]=np.array(f1.readline().split())[:strain.shape[-1]].astype(np.float64),\
                                  np.array(f2.readline().split())[:stress.shape[-1]].astype(np.float64)
    else:
        for _ in range(7):
            f1.readline()
            f2.readline()
        for j in range(nel):
            strain[j,ii,:],stress[j,ii,:]=np.array(f1.readline().split())[:strain.shape[-1]].astype(np.float64),\
                                          np.array(f2.readline().split())[:stress.shape[-1]].astype(np.float64)
    f2.close()
    f1.close()

if(nel!=1):
    stress=np.average(stress,axis=0)
    strain=np.average(strain,axis=0)
    
rc('font',size=10)
rc('font',family='serif')
rc('axes',labelsize=10)
rc('text', usetex=True)
l0,=plt.plot(strain[:,2],stress[:,2],'k')
plt.xlabel('Strain ')
plt.ylabel('Stress')
plt.title('Stress Strain curves')
sio.savemat('case1.mat',{'strain':strain[:,2],'stress':stress[:,2]})

# mg_sim=sio.loadmat('mg_single_crystal.mat')
# rc('font',size=10)
# rc('font',family='serif')
# rc('axes',labelsize=10)
# rc('text', usetex=True)
# l0,=plt.plot(mg_sim['case1'][:,0] ,mg_sim['case1'][:,1],'k')
# l1,=plt.plot(mg_sim['case2'][:,0] ,mg_sim['case2'][:,1],'r')
# l2,=plt.plot(mg_sim['case3'][:,0] ,mg_sim['case3'][:,1],'g')
# l3,=plt.plot(mg_sim['case4'][:,0] ,mg_sim['case4'][:,1],'b')
# mg_exp=sio.loadmat('mg_single_crystal_exp.mat')
# l4,=plt.plot(mg_exp['case_1_exp'][:,0] ,mg_exp['case_1_exp'][:,1],'ko')
# l5,=plt.plot(mg_exp['case_2_exp'][:,0] ,mg_exp['case_2_exp'][:,1],'ro')
# l6,=plt.plot(mg_exp['case_3_exp'][:,0] ,mg_exp['case_3_exp'][:,1],'go')
# l7,=plt.plot(mg_exp['case_4_exp'][:,0] ,mg_exp['case_4_exp'][:,1],'bo')
# plt.legend([l0,l1,l2,l3,l4,l5,l6,l7],['Case - 1 : FE','Case - 2 : FE','Case - 3 : FE','Case - 4 : FE','Case - 1 : Exp','Case - 2 : Exp','Case - 3 : Exp','Case - 4 : Exp'])
# plt.xlabel('Strain')
# plt.ylabel('Stress (MPa)')
# plt.savefig('mg_single_crystal.eps')


zr_sim=sio.loadmat('zr_polycrystal.mat')
rc('font',size=10)
rc('font',family='serif')
rc('axes',labelsize=10)
rc('text', usetex=True)
l0,=plt.plot(zr_sim['zr_nd_sim'][:,0] ,zr_sim['zr_nd_sim'][:,1],'k')
l1,=plt.plot(zr_sim['zr_td_sim'][:,0] ,zr_sim['zr_td_sim'][:,1],'r')
l2,=plt.plot(zr_sim['zr_rd_sim'][:,0] ,zr_sim['zr_rd_sim'][:,1],'g')
zr_exp=sio.loadmat('zr_polycrystal_exp.mat')
l3,=plt.plot(zr_exp['zr_nd_exp'][:,0] ,zr_exp['zr_nd_exp'][:,1],'ko')
l4,=plt.plot(zr_exp['zr_td_exp'][:,0] ,zr_exp['zr_td_exp'][:,1],'ro')
l5,=plt.plot(zr_exp['zr_rd_exp'][:,0] ,zr_exp['zr_rd_exp'][:,1],'go')

plt.legend([l0,l1,l2,l3,l4,l5],['ND : FE','TD : FE','RD : FE','ND : Exp','TD : Exp','RD : Exp'])
plt.xlabel('Strain')
plt.ylabel('Stress (MPa)')
plt.savefig('zr_polycrystal.eps')
