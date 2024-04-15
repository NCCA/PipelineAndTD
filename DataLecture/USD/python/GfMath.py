#!/usr/bin/env python

from pxr import Gf, Usd, UsdGeom

# create a point
point = Gf.Vec3f(1, 2, 3)
print(point)
# Now a matrix
tx = Gf.Matrix3f()
print(tx)
# We can do maths as normal
print(tx * point)
print(point * tx)

# We can set the matrix using various methods for example rotate.
tx.SetRotate(Gf.Rotation(Gf.Vec3d(0, 0, 1), 45.0))
print(tx)
print(tx * point)
print(point * tx)


# for more complex operations we can combine matrices as per normal

rotation = Gf.Matrix4f().SetRotate(Gf.Rotation(Gf.Vec3d(0, 0, 1), 45.0))
translation = Gf.Matrix4f().SetTranslate(Gf.Vec3f(1, 2, 3))
scale = Gf.Matrix4f().SetScale(Gf.Vec3f(1, 2, 1))

points = [
    Gf.Vec4f(1, 0, 1, 1),
    Gf.Vec4f(1, 0, -1, 1),
    Gf.Vec4f(-1, 0, -1, 1),
    Gf.Vec4f(-1, 0, 1, 1),
]

# now create transform matrix

tx = scale * rotation * translation
print(tx)

for point in points:
    print(tx * point)


quat = Gf.Quath(1, 0.1, 0.2, 0)
print(quat)
print(quat.GetImaginary())
print(quat.GetReal())
print(quat.GetInverse())
print(quat.GetNormalized())
print(quat.GetConjugate())
print(quat.Transform(Gf.Vec3h(1, 2, 3)))

rot = Gf.Rotation(Gf.Vec3d(0, 0, 1), 45.0)
print(rot)
print(rot.GetQuaternion())
