#!/usr/bin/env python
import random
import Poisson as ps
import matplotlib.pyplot as plt
from timeit import default_timer as timer
from datetime import datetime

width = 400
height =400
r=3.5
k=20
start = datetime.now()
scatter = ps.PoissonDisc(width, height, r,k)
end = datetime.now()
delta = end-start

print('construction took {} ms'.format(int(delta.total_seconds() * 1000)))
start = datetime.now()
points=scatter.sample()
end = datetime.now()
delta = end-start

print('sample took {} ms for {} points'.format(int(delta.total_seconds() * 1000),len(points)))

plt.title("Poisson disk sampling")
plt.scatter(*zip(*points),s=r)
plt.show()
