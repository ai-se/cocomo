from __future__ import division,print_function
import sys 
sys.dont_write_bytecode = True

from lib import *
 
class Span:
    def __init__(i,x,lo,hi):
        i.x,i.lo,i.hi=x,lo,hi
        i.key=hash((x,lo,hi))
    def __hash__(i) : return i.key
    def __repr__(i) : return '%s <= %s <= %s' % (i.lo,i.x,i.hi)
        
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
        
class Rule:
  def __init__(i,ranges,rows,score=lambda x:1):
    i.ranges=ranges
    i.keys=set(map(lambda z:z.key, ranges))
    i.rows=rows
    i.score=sum(map(lambda z:z.score,rows))/len(rows)
  def __repr__(i):
    return '%s:%s' % (str(map(str,i.ranges)),len(i.rows))
  def same(i,j):
    if len(i.keys) < len(j.keys):
      return j.same(i)
    else: # is the smaller a subset of the larger
      return j.keys.issubset(i.keys)
  def __add__(i,j): 
   if i.same(j): 
     return False
   ranges = list(set(i.ranges + j.ranges)) # list uniques
   ranges = sorted(ranges,key=lambda x:x.attr) 
   b4  = ranges[0] 
   rows = b4.rows
   for now in ranges[1:]:
     if now.attr == b4.attr:
       rows = rows | now.rows
     else:
       rows = rows & now.rows 
     if not rows: 
       return False
     b4 = now
   return Rule(ranges,rows,i.score)
 
def data(**d):  
  lo,hi={},{}
  def lohi0(j,n):  
      hi[j] = max(n, hi.get(j,-1*10**32))
      lo[j] = min(n, lo.get(j,   10**32))
  def lohi(one):
    for j in less: lohi0(j,one[j])
    for j in more: lohi0(j, one[j])
  def norm(j,n):  
    return (n - lo[j] ) / (hi[j] - lo[j] + 0.0001) 
  def score(one):
    all,n = 0,0
    for j in less:
      n   += 1 
      all += (1 - norm(j,one[j]))**2
    for j in more:
      n   += 1 
      all += norm(j,one[j])**2
    return all**2 / n**2
  names=d["names"] 
  data=d["data"]
  more=[i for i,name in enumerate(names) if ">" in name]
  less=[i for i,name in enumerate(names) if "<" in name]
  dep = more+less
  indep=[i for i,name in enumerate(names) if not i in dep]
  for one in data: lohi(one)
  return o(more=more,less=less,indep=indep,names=names,
           data=map(lambda one: Row(one,score(one)),
                    data))
  
class Row:
  id=0
  def __init__(i,cells,score):
    Row.id = i.id = Row.id+1
    i.cells= cells
    
    #n,all=0,0
    i.score=score
  def __hash__(i): return i.id
  def __getitem__(i, n): return i.cells[n]