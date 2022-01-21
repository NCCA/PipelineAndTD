#!/usr/bin/env python

import numpy as np
from math import (cos,sin,radians)
from random import uniform
# create identity matrix then set as 45 rotation in X axis
tx = np.identity(4,dtype=float)
sr=sin(radians(45.0))
cr=cos(radians(45.0))
tx[1][1]=cr
tx[1][2]=sr
tx[2][1]=-sr
tx[2][2]=cr
print(tx)
print('shape is ',tx.shape)
# create array of random points (Vec43)
points=[np.array([uniform(-1,1),uniform(-1,1),uniform(-1,1),1.0]) for i in range(0,10)]
# show the use of either dot(x,y) or the @ operator to multiply the two
for p in points :
   print('{} * tx ={}'.format(p,np.dot(p,tx)))
   print('{} @ tx ={}'.format(p,p@tx))