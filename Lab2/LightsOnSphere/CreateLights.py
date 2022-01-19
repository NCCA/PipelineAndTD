import math
import random
import maya.cmds as cmds
import string



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
    return ''.join(random.choices(string.ascii_letters)+(random.choices(string.ascii_letters + string.digits, k=random.randint(5, 20))))

colours=[(1,0,0),(0,1,0),(0,0,1),(1,1,1)] # red green blue white


if __name__ == '__main__' :
    cmds.select(all=True)
    cmds.delete()
    for i in range(0,random.randint(10, 200)) :
        x,y,z=random_point_on_sphere(14,hemisphere=True)
        name=randName()
        colour=random.choices(colours)
        cmds.shadingNode('pointLight', asLight=True, name=name)
        cmds.move(x,y,z)
        xrot,yrot,zrot=aimToPoint(x,y,z,0,0,0)
        cmds.rotate(xrot,yrot,zrot)
        cmds.rename('pointLight1',  name)
        cmds.setAttr(name+'|'+name+'.color',colour[0][0],colour[0][1],colour[0][2],type = 'double3' )

    
