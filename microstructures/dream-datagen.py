# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 22:37:41 2018

@author: vadit
"""

import numpy as np

f=open("DRX-1.txt",'r')
fo=open("DRX-dream.txt",'w')
f.readline()
f.readline()
f.readline()
f.readline()
fo.write("Angle Count:4958\n")
for i in range(4958):
    temp=f.readline()
    temp=temp.split()
    temp2=temp[0]+" "+temp[1]+" "+temp[2]+" "+temp[3]+" 1\n"
    #temp=temp+" 1\n"
    fo.write(temp2)
fo.close()
f.close()