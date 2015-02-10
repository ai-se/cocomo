<small>_This file is part of cocomo. To know more, view the source code [boot.py](../src/boot.py) or read our [home](https://github.com/ai-se/cocomo) page._</small>

# Boot code: stuff needed before anything else

## `o`: a Generic Holder for Names Slots

Useful when you want a bag of names things, that 
do not need methods.

````python
class o:
  def d(i)           : return i.__dict__
  def update(i,**d)  : i.d().update(**d); return i
  def has(i,k)    : return k in i.d()
  def __init__(i,**d): i.update(**d)
  def __repr__(i)    : 
    def name(x):
      f = lambda x: x.__class__.__name__ == 'function'
      return x.__name__ if f(x) else x
    keys = [k for k in sorted(i.d().keys()) 
            if k[0] is not "_"]
    show = [':%s %s' % (k, name(i.d()[k])) 
            for k in keys]
    return '{'+' '.join(show)+'}'
````


## `setting`: a Wrapper that remembers the Settings

````python
def setting(f):
  def wrapper(**d):
    tmp = the.d()[f.__name__] = f(**d)
    return tmp
  wrapper()
  return wrapper
````

## `the`: Where we Store the Globals

````python
the=o()
````

Use the following to print the global settings

````python
def THAT(x=the,s="",pre=""):
  d = x.d()
  say(pre)
  for k in sorted(d.keys()):
    if k[0] is not "_":
      say(s + (':%s ' % k))
      y = d[k]
      THAT(y,s+"   ","\n") if ako(y,o) else print(y)
````
