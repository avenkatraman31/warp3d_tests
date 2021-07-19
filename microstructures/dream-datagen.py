# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 22:37:41 2018

@author: mrupe
"""

import numpy as np

f=open("DRX-1.txt",'r')
fo=open("Dream_basal.txt",'w')
f.readline()
f.readline()
f.readline()
f.readline()
fo.write("Angle Count:4958\n")
for i in range(1000):
    temp=f.readline()
    temp=temp.split()
    #temp2=str(float(temp[0])*np.pi/180)+" "+str(float(temp[1])*np.pi/180)+" "+str(float(temp[2])*np.pi/180)+" "+str(float(temp[3]))+" 1\n"
    temp2=temp[0]+" "+temp[1]+" "+temp[2]+" "+temp[3]+" 1\n"
    #temp=temp+" 1\n"
    fo.write(temp2)
fo.close()
f.close()

# for j in range(9):
    # f=open("ODF_%d.txt"%(j+1),'r')
    # fo=open("Dream_ODF_%d.txt"%(j+1),'w')
    # f.readline()
    # f.readline()
    # f.readline()
    # f.readline()
    # fo.write("Angle Count:4958\n")
    # for i in range(4958):
        # temp=f.readline()
        # temp=temp.split()
        # temp2=str(float(temp[0])*np.pi/180)+" "+str(float(temp[1])*np.pi/180)+" "+str(float(temp[2])*np.pi/180)+" "+str(float(temp[3]))+" 1\n"
        # temp2=temp[0]+" "+temp[1]+" "+temp[2]+" "+temp[3]+" 1\n"
        # temp=temp+" 1\n"
        # fo.write(temp2)
    # fo.close()
    # f.close()
    
# f=open("DRX-test.txt",'r')
# fo=open("DRX-dream-test.txt",'w')
# f.readline()
# f.readline()
# f.readline()
# f.readline()
# fo.write("Angle Count:4958\n")
# for i in range(4958):
#         temp=f.readline()
#         temp=temp.split()
#         temp2=temp[0]+" "+temp[1]+" "+temp[2]+" "+temp[3]+" 1\n"
#         #temp=temp+" 1\n"
#         fo.write(temp2)
# fo.close()
# f.close()