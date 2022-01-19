#!/usr/bin/env mayapy

import maya.standalone
import maya.cmds as cmds
import maya.mel as mel
import math
import random
import string
import os
import argparse


def random_point_on_sphere(radius=1,hemisphere=False) :
    xiTheta=random.uniform(0,1)
    temp=2.0*radius*math.sqrt(xiTheta*(1.0 - xiTheta))
    twoPiXiPhi=math.pi*2*random.uniform(0,1)
    x=temp*math.cos(twoPiXiPhi)
    y=temp*math.sin(twoPiXiPhi)
    if hemisphere == True :
        y=abs(y)
    z=radius*(1.0 - 2.0*xiTheta)
    return x,y,z

def randName() :
    """ 
    generate a random name, in python3 we can use choices however in py2 we need a different version 
    return ''.join(random.choice(string.ascii_letters)+(random.choice(string.ascii_letters + string.digits, k=random.randint(5, 20))))
    """
    return ''.join(random.choice(string.ascii_letters)+(random.choice(string.ascii_letters + string.digits)) for i in range(0,random.randint(5,20)))
colours=[(1,0,0),(0,1,0),(0,0,1),(1,1,1)] # red green blue white


if __name__ == '__main__' :

    parser = argparse.ArgumentParser(description='Create random Maya Scenes')
    parser.add_argument('--nscenes' , '-n' ,nargs='?',const=2, default=2,type=int,help='how many scenes to create 2 default')
    parser.add_argument("--fname", "-f", type=str, default='testScene',help="filename")
    parser.add_argument('--maxlights' , '-m' ,nargs='?',const=100, default=100,type=int,help='max lights in scene')

    args = parser.parse_args()


    maya.standalone.initialize(name='python')

    location=os.getcwd()
    for i in range(0,args.nscenes) :
        cmds.file( f=True, new=True )
        cmds.file( rename='{}/{}.{}.ma'.format(location,args.fname,i) )

        for i in range(0,random.randint(10, 200)) :
            x,y,z=random_point_on_sphere(14,hemisphere=True)
            name=randName()
            colour=random.choice(colours)
            cmds.shadingNode('pointLight', asLight=True, name=name)
            cmds.move(x,y,z)
            cmds.rename('pointLight1',  name)
            cmds.setAttr(name+'|'+name+'.color',colour[0],colour[1],colour[2],type = 'double3' )



        commands=[ "polyCone", "polyCube", "polySphere", "polyTorus" ]
        for i in range(0,random.randint(5,200)) :
            mel.eval('{} -n "{}";'.format(commands[random.randint(0,len(commands)-1)],randName()))
            cmds.move(random.uniform(-10,10),0,random.uniform(-10,10))
        # now save scene
        cmds.file( save=True, de=False, type='mayaAscii' )



    print('closing down maya-standalone')
    maya.standalone.uninitialize()