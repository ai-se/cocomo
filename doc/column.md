<small>_This file is part of cocomo. To know more, view the source code [column.py](../src/column.py) or read our [home](https://github.com/ai-se/cocomo) page._</small>
# Defining columns

````python
from lib import *

@setting
def COL(**d): return o( 
    buffer = 128,
    m = 2,
    k = 1,
    missing='?'
    ).update(**d)

````

## `Column`: Generic Columns

`Column`s keep track of what was seen in a column.
The general idea is that:

+  _Before_ you start reading data,
   you create one `Column` for each column. 
+ _After_ the data has been read, a column can be
   `ask()`ed  for a representative on what
   values have been observed.
+  _While_ reading data, the columns peek at each
   seen value (and update their information accordingly).
   This is called `tell()`ing the column about a value.

````python
class Column:
  def tell(i,x):
    if x is None or x == the.COL.missing:
      return x
    i.n += 1
    i.tell1(x)
    return x
````

Also, you can ask a `Column` for:

+ The distance between two col values (normalized 0 to 1)
+ A `logger()`; i.e
  a new column for storing things like this column.

Finally, a `Column` can tell you how `likely()` is some
value, given the `tell()`ed values of that column.

## `S`: Columns of Symbols

Tracks the frequency counts of the `tell()`ed symbols.
Can report the entropy `ent()` of that distribution
(which is a measure of the diversity of those symbols).

````python
class S(Column): 
  def __init__(i,all=None,name=''): 
    i.all = {}
    print('all',i.all)
    i.n = 0
    i.name = str(name)
    map(i.tell,all)
  def tell1(i,x)  : 
    i.all[x] = i.all.get(x,0) + 1
  def ask(i)     : return(ask(i.all.keys()))
  def dist(i,x,y): return 0 if x==y else 1
  def norm(i,x)  : return x
  def logger(i)  : return S(name=i.name)
  def read(i,x)  : return x
  def ent(i):
    e=0
    for key,value in i.all.items():
      if value > 0:
        p = value/i.n
      e -= p*log(p,2)
    return e
  def likely(i,x,prior=1):
    m = the.COL.m
    return (i.all.get(x,0) + m*prior)/(i.n + m)
````
    
In `likely()`, the `prior` value is some used in a Naive Bayes
classifier (details later).


## `N`: Columns of Numbers

Numeric columns track the `lo` and `hi` of the `tell()`ed
numbers as well as their mean `mu` and standard deviation
`sd()`.

`N`s  also keep `kept()` a random sampling
of the numbers (up to a max of `the.COL.buffer` numbers).
 
````python
class N(Column):
  def __init__(i,init=[],lo=None,hi=None,name=''):
    i.n, i.lo, i.hi, i.name = 0,lo,hi,str(name)
    i._kept = [None]*the.COL.buffer
    i.mu = i.m2= 0
    map(i.tell,init)
  def __repr__(i): 
    return '{:%s #%s [%s .. %s]}'%(
      i.name,i.n,i.lo ,i.hi)
  def ask(i): 
    return i.lo + r()*(i.hi - i.lo)
  def dist(i,x,y): 
    return i.norm(x) - i.norm(y)
  def q123(i):
    def r(x) : return int(round(x,0))
    lst = i.kept()
    q = len(lst)/4
    return lst[r(q)], lst[r(q*2)], lst[r(q*3)]  
  def mediqr(i):
    q1,q2,q3 = i.q123()
    return q2, q3 - q1
  def q2q3(i): 
    q1,q2,q3 = i.q123()
    return q2,q3
  def median(i):
    _,q2,_ = i.q123()
    return q2
  def kept(i): 
    return sorted([x for x in i._kept if x is not None])
  def likely(i,x,prior=None):
    return normpdf(x,i.mu,i.sd())
  def logger(i): 
    return N(name=i.name,lo=i.lo,hi=i.hi)
  def norm(i,x):
    tmp =(x - i.lo) / (i.hi - i.lo + 0.00001)
    return max(0,min(tmp,1))
  def read(i,x): 
    return float(x)
  def sd(i):
    if i.n < 2: return 0
    return (max(0,i.m2)/(i.n - 1))**0.5
  def tell1(i,x):
    if i.lo is None: i.lo = x
    if i.hi is None: i.hi = x
    i.lo =  min(i.lo,x)
    i.hi =  max(i.hi,x)
    delta = x - i.mu
    i.mu += delta/i.n
    i.m2 += delta*(x - i.mu)
    l = len(i._kept)
    if r() <= l/i.n: i._kept[ int(r()*l) ]= x
 
 
````
