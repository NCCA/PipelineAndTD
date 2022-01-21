#!/usr/bin/env python

import numpy as np

x = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
print(x)
print('shape is ',x.shape)
# we can index arrays
x[1][2]=99
print(x)
