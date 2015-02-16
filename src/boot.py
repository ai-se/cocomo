from __future__ import division,print_function
import sys
sys.dont_write_bytecode =True

"""

# Boot code: stuff needed before anything else

## `o`: a Generic Holder for Names Slots

Useful when you want a bag of names things, that 
do not need methods.

"""
class o:
  def d(i)            : return i.__dict__
  def update(i,**d)   : i.d().update(**d); return i
  def has(i,k)        : return k in i.d()
  def __init__(i,**d) : i.update(**d)
  def __getitem__(i,k): return i.d()[k]
  def __repr__(i):
    keys = [k for k in sorted(i.d().keys()) 
            if k[0] is not "_"]
    show = [':%s %s' % (k, name(i.d()[k])) 
            for k in keys]
    return '{'+' '.join(show)+'}'

def name(x):
  f=lambda z: z.__class__.__name__ == 'function'
  return 'function(%s)'% x.__name__ if f(x) else x
  
"""


## `setting`: a Wrapper that remembers the Settings

"""
def setting(f):
  def wrapper(**d):
    tmp = the.d()[f.__name__] = f(**d)
    return tmp
  wrapper()
  return wrapper
"""

## `the`: Where we Store the Globals

"""
the=o()
"""

Use the following to print the global settings

"""
def THAT(x=the,s="",pre=""):
  d = x.d()
  print(pre,end="")
  for k in sorted(d.keys()):
    if k[0] is not "_":
      print(s + (':%s ' % k),end="")
      y = d[k]
      if isinstance(y,o):
        THAT(y,s+"   ","\n")
      else:
        print(name(y))

