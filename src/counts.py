from __future__ import division,print_function
import sys
sys.dont_write_bytecode =True

from lib import *

@setting
def CNT(**d): return o(
    #Thresholds are from http://goo.gl/25bAh9
    sdivTiny = 4,
    sdivCohen = 0.3,
    keep = 128
  ).update(**d)
"""

## Effect size

Cliff's delta detects a "small" (a.k.a. negliable or dull)
effort. It reports the probability that one list
has numbers bigger or smaller than another
list. 

It is based on the following inutiion: if one number 
is similar to another set of numbers
that this number should fall near the central 
tendancy of other set of numbers.
A number near   the central tendancy if there are nearly as many numbers above
it as below it. So Cliff's delta counts how many numbers in _lst2_
are greater or smaller than each item of _lst1_. 

This version sorts the lists before making
that test. For lists containing 100,1000,10000
random numbers,this implementations
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

## Sampling

### Keeping a Sample

A _Cache_ is a place to remember some items
in array of size, at most, _size_
(which is initially a list of _None_).

"""
class Cache():
  def __init__(i,keep=None):
    i.keep = keep or the.CNT.keep
    i.reset()
  def reset(i):
    i.n = 0
    i._kept = [None]*i.keep
  def tell(i,x):
    i.n += 1
    l = len(i._kept)
    if r() <= l/i.n: i._kept[ int(r()*l) ]= x
  def contents(): 
    return sorted([x for x in i._kept if x is not None])
"""

### Xtile: Showing a Sample

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
  out[int(width/2)]    = bar; 
  out[place(pos(0.5))] = star  
  return '('+''.join(out) +  ")," +  pretty(what)
"""

### Xtiles: Comparing Many Samples

Combines xtile with cliffsDelta. Row one
gets called "rank=1". Other rows get a  higher rank
if they are different to all proceeding rows of the same rank.

Assumes first item of each sublist is some tag describing the contents. e.g.
[["oranges",1,4 5 3 2],
 ["apples",3,3,4,5,3,2]]

"""

def xtiles(rows,showMin=0.25,showMax=0.75,
             width=50,
             chops=[0,0.25,0.5,0.75,0.99],
              marks=[" ","-","-"," "," "],
              bar="|",star="*",show=" %3.1f"):
  def before(row):
    rank = 1                   # an initial value. we change it later
    txt  = row[0]              # pull out the textual descriptor
    nums = sorted(row[1:])     # sort all the rest 
    med  = nums[ int( round(len(nums)*0.5)) ]        # get the median
    return [nums,rank,txt,med] # return all that info
  def after(row):
    nums = row[0]              # stop carrying round the raw numbers
    row  = row[1:]             # keep everything BUT those raw numbers
    row[-1] = show % row[-1]   # pretty print the median
    row += [xtile(nums,lo=lo,hi=hi,width=width, # add the xtile display
            chops=chops, marks=marks, bar=bar,star=star,show=show)]
    return row
  rows = sorted(map(before,rows), key=lambda x:x[-1]) # sort on median
  nums = sorted([num for row in rows for num in row[0]])  
  lo   = nums[  0 ]
  hi   = nums[ -1 ]
  rank = 1
  pool = rows[0][0]
  for one,two in pairs(rows):
    if cliffsDelta(pool,two[0]):  # This row is different to the proceeding
      rank += 1                   # so increment the rank
      pool = two[0]               # we have new nums to compare to the rest
    else:
      pool += two[0]              # rank is the same so add these nums
                                  # to the pool of numbers to compare with rest
    two[1] = rank
  header=[["rank","rx","median",""],  # pretty print stuff
         ["====","==","=======",""]] 
  rows = map(after,rows)            # clean up list before showing
  printm(header +  rows)    # and done
"""

## Counting

"_N_" is a place to incrementally add and delete
to our knowledge of the mean and standard deviation (_mu_, _sd()_)
of a set of numbers.  
When we need more info that _mu_ and _sd()_
(e.g. if we are testing the _cliffsDelta_ between two populations),
the message .cache.contents() returns a sorted sample 
of the numbers seen so far.

"""  
class N(): # Add/delete counts of numbers.
    def __init__(i,inits=[]):
      i.zero()
      for number in inits: i + number 
    def zero(i): 
        i.cache = Cache()
        i.n = i.mu = i.m2 = 0.0
    def sd(i)  : 
      if i.n < 2: return i.mu
      else:       
        return (max(0,i.m2)*1.0/(i.n - 1))**0.5
    def __add__(i,x):
      i.cache.tell(x)
      i.n  += 1
      delta = x - i.mu
      i.mu += delta/(1.0*i.n)
      i.m2 += delta*(x - i.mu)
    def __sub__(i,x):
      i.cache.reset()
      if i.n < 2: return i.zero()
      i.n  -= 1
      delta = x - i.mu
      i.mu -= delta/(1.0*i.n)
      i.m2 -= delta*(x - i.mu)    
"""

## Ranges

A _Range_ has a _Span_ from _lo_ to _hi_

"""
class Span:
    def __init__(i,x,lo,hi):
        i.x,i.lo,i.hi=x,lo,hi
        i.key=hash((x,lo,hi))
    def __hash__(i) : return i.key
    def __repr__(i) : return '%s <= %s <= %s' % (i.lo,i.x,i.hi)
"""

_Ranges_ keep their rows as sets and report their hash as the hash
of their span.

"""
class Range:
    def __init__(i,x=None,attr=None,y=None,rows=None):
        i.n     = len(rows)
        i.rows  = set(rows)
        i.attr  = attr
        i.x,i.y = x,y
        i.key   = Span(attr,x.lo,x.hi) 
    def __hash__(i): 
        return hash(i.key)
    def __repr__(i):
        return '%s:%s' % (i.key,i.n)
"""

_Sdiv()_ finds ranges by recursively dividing
a sorted list of "_x_" numbers at the point that
minimizes the expected value of the variance of
an associated "_y_" value.

As coded here, _sdiv()_ is a supervised range finder
since it divided "_x_" values according to their
impact on "_y_". To run this as a simpler
unsupervised learner, set "_x_" to "_y_" so it divides
itself according to changes in itself.

"""
def sdiv(lst, attr=None,tiny=None,cohen=None,small=None,
         x=lambda z:z[0], y=lambda z:z[-1],better=gt):
  "Divide lst of (x,y) using variance of y."
  tiny = tiny or the.CNT.sdivTiny
  cohen= cohen or the.CNT.sdivCohen
  #----------------------------------------------
  def divide(this,small): #Find best divide of 'this'
    lhs,rhs = N(), N(y(z) for z in this)
    n0, score, cut,mu = 1.0*rhs.n, rhs.sd(), None,rhs.mu
    for j,one  in enumerate(this): 
      if lhs.n > tiny and rhs.n > tiny: 
        maybe= lhs.n/n0*lhs.sd()+ rhs.n/n0*rhs.sd()
        if better(maybe,score) :  
          if abs(lhs.mu - rhs.mu) >= small:
            cut,score = j,maybe
      rhs - y(one)
      lhs + y(one)    
    return cut,mu,score,this
  #----------------------------------------------
  def recurse(this, small,cuts):
    cut,mu,sd,part0 = divide(this,small)
    if cut: 
      recurse(this[:cut], small, cuts)
      recurse(this[cut:], small, cuts)
    else:   
      cuts += [Range(attr = attr,
                     x    = o(lo=x(this[0]), hi=x(this[-1])),
                     y    = o(mu=mu, sd=sd),
                     rows = this)]
    return cuts
  #---| main |-----------------------------------
  small = small or N(y(z) for z in lst).sd()*cohen
  if lst: 
    return recurse(sorted(lst,key=x),small, [] )
