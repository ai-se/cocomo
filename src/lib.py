from __future__ import division,print_function
import sys
sys.dont_write_bytecode =True

"""

# General stuff

"""
from boot import *
import random,math

@setting
def LIB(**d): return o(
    "Thresholds are from http://goo.gl/25bAh9"
    dull = [0.147, 0.33, 0.474][0]
  ).update(**d)
"""

## Type stuff

"""
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
"""

## Math stuff

"""
pi=math.pi
e=math.e
sqrt=math.sqrt
log=math.log

def mult(lst): return reduce(lambda x,y: x*y,lst)
"""

## Random stuff

"""
r     = random.random
rseed = random.seed

def ask(x):
  return random.choice(list(x))
    
def shuffle(lst): random.shuffle(lst); return lst

def normpdf(x, mu=0, sigma=1):
  u = (x-mu) /abs( sigma)
  y = e**(-u*u/2) / (sqrt(2*pi) * abs(sigma))
  return y
"""

List stuff

"""
def first(lst): return lst[0]
def second(lst): return lst[1]
def last(lst): return lst[-1]

def median(lst,ordered=True):
  if not ordered: lst=sorted(lst)
  n = len(lst)
  p = int(n/2) 
  q = p if  n % 2 else p+1 
  return (lst[p] + lst[q])/2
"""

#Misc stuff

"""
def msecs(f):
  import datetime
  t1 = datetime.datetime.now()
  f()
  t2 = datetime.datetime.now() - t1
  return t2.total_seconds()
"""

## Iterator Stuff

Return all pairs of items i,i+1 from a list.

"""
def pairs(lst):

  last=lst[0]
  for i in lst[1:]:
    yield last,i
    last = i
"""

Return counts of consecutively repeated items in a list.

"""
def runs(lst):
  for j,two in enumerate(lst):
    if j == 0:
      one,i = two,0
    if one!=two:
      yield j - i,one
      i = j
    one=two
  yield j - i + 1,two
"""

## Stats stuff

Cliff's delta computes the probability that one list
has numbers bigger or smaller than another
list. This version sorts the lists before making
that test. For lists containing 100,1000,10000
random numbers, this implementations
is  one to three orders
of magnitude faster
than another version that does not
use sorting.

"""
def cliffsDelta(lst1,lst2,dull=None):
  dull = dull or the.LIB.dull
  m, n = len(lst1), len(lst2)
  lst2 = sorted(lst2)
  j = more = less = 0
  for repeats,x in runs(sorted(lst1)):
    while j <= (n - 1) and lst2[j] <  x: 
      j += 1
    more += j*repeats
    while j <= (n - 1) and lst2[j] == x: 
      j += 1
    less += (n - j)*repeats
  d= (more - less) / (m*n) 
  return abs(d)  > dull
"""

## Printing stuff

Print one or more of anything (no new lines).

"""
def say(*l):
  sys.stdout.write(', '.join(map(str,l))) 
  sys.stdout.flush()
"""

Print list of numbers without too many decimal places.

"""
def g(lst,n=3):
  for col,val in enumerate(lst):
    if isinstance(val,float): 
      val = round(val,n) if n else int(val)
    lst[col] = val
  return lst
"""

Print a list of lists, aligning all the columns.

"""
def printm(matrix,sep=' | '):
  s = [[str(e) for e in row] for row in matrix]
  lens = [max(map(len, col)) for col in zip(*s)]
  fmt = sep.join('{{:{}}}'.format(x) for x in lens)
  for row in [fmt.format(*row) for row in s]:
    print(row)
""""

Print a list of numbers (possibly
unsorted) 
 and presents them as a horizontal
 percentile chart (in ascii format). The default is a 
  contracted _quintile_ that shows the 
  10,30,50,70,90 breaks in the data (but this can be 
  changed- see the optional flags of the function)

"""
def xtile(lst,lo=0,hi=100,width=50,
             chops=[0.1 ,0.3,0.5,0.7,0.9],
             marks=["-" ," "," ","-"," "],
             bar="|",star="*",show=" %3.0f"):
  def r(x)     : return int(round(x,0))
  def pos(p)   : return ordered[r(len(lst)*p)]
  def place(x) : 
    return r(width*(x - lo)/(hi-lo+0.00001))
  def pretty(lst) : 
    return ', '.join([show % x for x in lst])
  ordered = sorted(lst)
  lo      = min(lo,ordered[0])
  hi      = max(hi,ordered[-1])
  what    = [pos(p)   for p in chops]
  where   = [place(n) for n in  what]
  out     = [" "] * width
  for one,two in pairs(where):
    for i in range(one,two): 
      out[i] = marks[0]
    marks = marks[1:]
  out[int(width/2)]    = bar
  out[place(pos(0.5))] = star 
  return '('+''.join(out) +  ")," +  pretty(what)
"""

## Xtiles

Combines xtile with cliffsDelta. Line one
gets called "rank=1". Other lines get a  higher rank
if they are different to all proceeding lines of the same rank.

Assumes first item of each sublist is some tag describing the contents. e.g.
[["oranges",1,4 5 3 2],
 ["apples",3,3,4,5,3,2]]
"""

def xtiles(lists,
             width=50,
             chops=[0,0.25,0.5,0.75,0.99],
              marks=[" ","-","-"," "," "],
              bar="|",star="*",show=" %3.1f"):
  def before(lst):
    rank = 1
    txt  = lst[0]
    nums = sorted(lst[1:]) 
    med  = median(nums)
    return [nums,rank,txt,med]
  def after(lst):
    nums = lst[0]
    lst  = lst[1:] 
    lst[-1] = show % lst[-1]
    lst += [xtile(nums,lo=lo,hi=hi,width=width,
            chops=chops, marks=marks, bar=bar,star=star,show=show)]
    return lst
  lists = sorted(map(before,lists), key=lambda x:x[-1])
  lo    = min(*map(lambda z:z[0][ 0],lists))
  hi    = max(*map(lambda z:z[0][-1],lists))
  rank = 1
  pool = lists[0][0]
  for one,two in pairs(lists):
    if cliffsDelta(pool,two[0]):  
      rank += 1
      pool = two[0]
    else:
      pool += two[0]
    two[1] = rank
  header=[["rank","rx","median",""],
         ["====","==","=======",""]] 
  printm(header +  map(after,lists))
"""

## Demo Stuff

"""
def go(d):
  doc= '# '+d.__doc__+"\n" if d.__doc__ else ""
  s='|'+'='*40 +'\n'
  print('\n==|',d.func_name + ' ' + s+doc)
  try:
    d()
  except:
    print('Demo function did not crash: False')
  return d
  
@go 
def _xtiles():
  xtiles([
        ["apples"]    + [4,5,7,4,7,6,5,8,6,5]*10,
        ["bananas"]   + [7,9,8,9,7,9,7,7,7,9,8,7,7,9,9]*10,
        ["oranges"]   + [1,5,5,3,3,2,4,6,3,2]*10,
        ["pears"]     + [7,7,8,6,8,7,6,7,8,6,8,7,6,7.1,8,6]*10,
        ["plantains"] + [7,9,8,9,7,9,7,7,7,9,8,7,7,9,9]*10])