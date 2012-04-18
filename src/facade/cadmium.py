
import json

A_MIN = 1
A_MAX = 2
A_CENTER = 3

UNION = '+'
SUBTRACTION = '-'
INTERSECTION = '*'

TRANSLATION = 'translation'
ROTATION = 'rotation'
SCALE = 'scale'
SHEAR = 'shear'

X_axis = [1,0,0]
Y_axis = [0,1,0]
Z_axis = [0,0,1]

class Solid():

  def __init__(self,
    solid=None, primitive=None, left=None, right=None, op=None):

    self.solid = None
    if solid:
      self.solid = solid
    elif primitive:
      self.primitive = primitive
    else:
      self.primitive = None
      self.left = left
      self.right = right
      self.op = op
    self.transforms = []
    self.params = dict()

  def __add__(self, other):
    return Solid(left=self, right=other, op=UNION)

  def __sub__(self, other):
    return Solid(left=self, right=other, op=SUBTRACTION)

  def __mul__(self, other):
    return Solid(left=self, right=other, op=INTERSECTION)

  def translate(self, x=0, y=0, z=0):
    self.transforms.append(dict(kind=TRANSLATION,x=x,y=y,z=z))
    return self

  def rotate(self, axis, angle):
    self.transforms.append(dict(kind=ROTATION,axis=axis,angle=angle))
    return self

  def scale(self, sx=1, sy=1, sz=1):
    self.transforms.append(dict(kind=SCALE,sx=sx,sy=sy,sz=sz))
    return self

  def shear(self, xy=0, xz=0, yx=0, yz=0, zx=0, zy=0):
    self.transforms.append(dict(kind=SHEAR,xy=xy,xz=xz,yx=yx,yz=yz,zx=zx,zy=zy))
    return self

  def toData(self):
    if self.solid:
      return self.solid.toData()
    elif self.primitive:
      return dict(kind=self.primitive,
        params=self.params,transforms=self.transforms)
    else:
      return dict(op=self.op,left=self.left.toData(),
        right=self.right.toData(), transforms=self.transforms)

class Box(Solid):
  def __init__(self, x,y,z, center=True):
    Solid.__init__(self, primitive='box')
    self.params = dict(x=x,y=y,z=z)

class Cylinder(Solid):
  def __init__(self, radius=None, height=None, h=None, r=None, center=True):
    Solid.__init__(self, primitive='cyl')
    if radius is not None:
      rad = radius
    else:
      rad = r
    if height is not None:
      hgt = height
    else:
      hgt = h
    self.params = dict(r=rad,h=hgt)

class Cone(Solid):
  def __init__(self, radius=None, height=None, h=None, r=None, center=True):
    Solid.__init__(self, primitive='con')
    if radius is not None:
      rad = radius
    else:
      rad = r
    if height is not None:
      hgt = height
    else:
      hgt = h
    self.params = dict(r=rad,h=hgt)

def description(*arg, **kwdArg):
  def decorator(func): return func
  return decorator

def param(*arg, **kwdArg):
  def decorator(func): return func
  return decorator

def main():
  bA = Box(3,3,3).translate(dy=-0.5)
  bB = Box(2,2,2).translate(dy=1)
  cyl = Cylinder(radius=0.5,height=7).translate(dy=1)\
    .rotate(axis=X_axis,angle=90)
  #s = (cyl*bA)+(cyl*bB)
  #s = cyl * (bA+bB)
  #s = bA - (bB * cyl)
  #s = (bA - bB) + (bA - cyl)
  #s = bA * (bB * cyl)
  #s = (bA - bB) + (bA * cyl)
  #s = bA - (bB - cyl)
  #s = (bA * bB) - cyl
  #s = bA * (bB - cyl)
  s = (bA - cyl) * bB
  #s = (bA - cyl) + (bB - cyl)
  #s = (bA + bB) - cyl
  #s = (bA * cyl) + (bB * cyl)
  #s = (bA + bB) * cyl

  #s = bA + bB + cyl
  print json.dumps(s.toData(), indent=2)

if __name__ == '__main__':
  main()
