from __future__ import division,print_function
import sys 
sys.dont_write_bytecode = True

"""

# Storing data in tables

Each line of table is store as a row. _Row_ has a unique
integer hash (so interesections of set of _Row_s is very fast).

"""
from counts import *

@setting
def DATA(**d): return o(
    #Thresholds are from http://goo.gl/25bAh9
    more = ">",
    less = "<"
  ).update(**d)

class Row:
  id=0
  def __init__(i,cells,score):
    i.cells= cells
    i.score=score
    Row.id = i.id = Row.id+1 
  def __hash__(i): return i.id
  def __getitem__(i, n): return i.cells[n]
"""

_Row_s are generated from a dictionary with keys.

```python
dict(names=["girth","age","shoesize",">weight","<height"],
     data= [[1      , 2,   3,        , 100,     200],
            [2      , 4,   4,        , 110,     180],
            ...
            ])
```

As a side-effect of generating rows, tables also know
the indexes of the columns

+ _dep_ : dependent variables (the goals)
+ _indep_ : the independent variables (the inputs)
+ _more_ : to be maximized (denoted with a ">")
+ _less_:  to be minimized (denoted with a "<")

One last thing: _data()_ also computes the distance _fromHell()__
for each row; i.e. how far away this row falls from the worst
values of the dependent columns. _FromHell()_ is normalized (so
always is a number zero to one).

"""
def data(**d):  
  lo,hi={},{}
  def lohi0(j,n):  
      hi[j] = max(n, hi.get(j,-1*the.LIB.most))
      lo[j] = min(n, lo.get(j,   the.LIB.most))
  def lohi(one):
    for j in less: lohi0(j,one[j])
    for j in more: lohi0(j, one[j])
  def norm(j,n):  
    return (n - lo[j] ) / (hi[j] - lo[j] + the.LIB.tiny) 
  def fromHell(one):
    all,n = 0,0
    moreHell, lessHell = 0,1
    for j in more:
      n   += 1 
      all += (moreHell - norm(j,one[j]))**2
    for j in less:
      n   += 1 
      all += (lessHell - norm(j,one[j]))**2
    return all**2 / n**2
  names=d["names"] 
  data=d["data"]
  more=[i for i,name in enumerate(names)
          if the.DATA.more in name]
  less=[i for i,name in enumerate(names)
          if the.DATA.less in name]
  dep = more+less
  indep=[i for i,name in enumerate(names) if not i in dep]
  for one in data: lohi(one)
  out = o(more=more,less=less,indep=indep,names=names,
           data=map(lambda one: Row(one,
                                    fromHell(one)),
                    data))
  out.score = sum(map(lambda z: z.score,out.data))/len(out.data)
  return out
