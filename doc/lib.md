<small>_This file is part of cocomo. To know more, view the source code [lib.py](../src/lib.py) or read our [home](https://github.com/ai-se/cocomo) page._</small>

# General stuff

````python
from boot import *
import random,math

@setting
def LIB(**d): return o(
    #Thresholds are from http://goo.gl/25bAh9
    dull = [0.147, 0.33, 0.474][0]
  ).update(**d)
````

## Type stuff

````python
def identity(x): return x
def ako(x,y)   : return isinstance(x,y)
def isList(x)  : 
  return x if isinstance(x,list) else [x]
def isSet(x): 
  return x if isinstance(x,set) else set([x])
def myIntersect(x,y):
  if isinstance(x,(str,int,float)): x = [x]
  if isinstance(y,(str,int,float)): y = [y]
  return [val for val in x if val in y]
````

## Math stuff

````python
pi=math.pi
e=math.e
sqrt=math.sqrt
log=math.log
 
def gt(x,y) : return x > y
def lt(x,y) : return x < y
def mult(lst): return reduce(lambda x,y: x*y,lst)
````

## Random stuff

````python
r     = random.random
rseed = random.seed

def ask(x):
  return random.choice(list(x))
    
def shuffle(lst): random.shuffle(lst); return lst

def normpdf(x, mu=0, sigma=1):
  u = (x-mu) /abs( sigma)
  y = e**(-u*u/2) / (sqrt(2*pi) * abs(sigma))
  return y
````

List stuff

````python
def first(lst): return lst[0]
def second(lst): return lst[1]
def last(lst): return lst[-1]

def median(lst,ordered=True):
  if not ordered: lst=sorted(lst)
  n = len(lst)
  p = int(n/2) 
  q = p if  n % 2 else p+1 
  return (lst[p] + lst[q])/2
````

#Misc stuff

````python
def msecs(f):
  import datetime
  t1 = datetime.datetime.now()
  f()
  t2 = datetime.datetime.now() - t1
  return t2.total_seconds()
````

## Iterator Stuff

Return all pairs of items i,i+1 from a list.

````python
def pairs(lst):
  last=lst[0]
  for i in lst[1:]:
    yield last,i
    last = i
````

Return counts of consecutively repeated items in a list.

````python
def runs(lst):
  for j,two in enumerate(lst):
    if j == 0:
      one,i = two,0
    if one!=two:
      yield j - i,one
      i = j
    one=two
  yield j - i + 1,two
````

## Printing stuff

Print one or more of anything (no new lines).

````python
def say(*l):
  sys.stdout.write(', '.join(map(str,l))) 
  sys.stdout.flush()
````

Print list of numbers without too many decimal places.

````python
def g(lst,n=3):
  for col,val in enumerate(lst):
    if isinstance(val,float): 
      val = round(val,n) if n else int(val)
    lst[col] = val
  return lst
````

Print a list of lists, aligning all the columns.

````python
def printm(matrix,sep=' | '):
  s = [[str(e) for e in row] for row in matrix]
  lens = [max(map(len, col)) for col in zip(*s)]
  fmt = sep.join('{{:{}}}'.format(x) for x in lens)
  for row in [fmt.format(*row) for row in s]:
    print(row)
````

## Demo Stuff

````python
def go(d):
  doc= '# '+d.__doc__+"\n" if d.__doc__ else ""
  s='|'+'='*40 +'\n'
  print('\n==|',d.func_name + ' ' + s+doc)
  try:
    d()
  except:
    print('Demo function did not crash: False')
  return d
  
````
