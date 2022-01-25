#!/usr/bin/env python
from PoissonDisk import PoissonDisk
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import argparse

def plot(width = 400,height=400,r=3.5,k=20,seed=1234) :
    start = datetime.now()
    p=PoissonDisk(width,height,r,k,seed)
    end = datetime.now()
    delta = end-start

    print('construction took {} ms'.format(int(delta.total_seconds() * 1000)))

    start = datetime.now()
    points=p.sample()
    end = datetime.now()
    delta = end-start
    print('sample took {} ms size'.format(int(delta.total_seconds() * 1000),len(points)))
    plt.title("Poisson disk sampling")
    p2=[]
    for t in points :
        p2.append((t.x,t.y))
    plt.scatter(*zip(*p2),s=1.3)
    plt.show()

if __name__ == '__main__' :
    parser = argparse.ArgumentParser(description='Plot params')

    parser.add_argument('--radius', '-r', nargs='?', 
											const=3.5, default=3.5, type=float,
											help='radius')

    parser.add_argument('--width' , '-wd' ,nargs='?', 
											const=400, default=400,type=int,
											help='width of sim')
    parser.add_argument('--height', '-ht' ,nargs='?', 
											const=400, default=400,type=int,
											help='height of sim')
    parser.add_argument('--simcount', '-k' ,nargs='?', 
											const=40, default=40,type=int,
											help='sim steps')
    parser.add_argument('--seed', '-s' ,nargs='?', 
											const=1234, default=1234,type=int,
											help='rand seed')
    args = parser.parse_args()


    plot(args.width,args.height,args.radius,args.simcount,args.seed)