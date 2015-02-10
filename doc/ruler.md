<small>_This file is part of cocomo. To know more, view the source code [ruler.py](../src/ruler.py) or read our [home](https://github.com/ai-se/cocomo) page._</small>

Multi-objective optimization

````python
from data import *
from counts import *

@setting
def RULER(**d): 
  def enough(ruleRows,allRows):
      return len(ruleRows) >= len(allRows)**0.5 
  return o( 
    better = gt,
    rules =o(tiny=20,
             small=0.01,
             repeats=32,
             beam=16,
             retries=32,
             enough=enough)
  ).update(**d)
````

## Rule: a collection of ranges

````python
class Rule:
  def __init__(i,ranges,rows):
    i.ranges = ranges
    i.keys   = set(map(lambda z:z.key, ranges))
    i.rows   = rows
    i.score  = sum(map(lambda z:z.score,rows))/len(rows)
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
   return Rule(ranges,rows)
````

Return the ranges:

+ From "useful" columns; i.e. those than can be
  divided into ranges that seperate the performance
  score;
+ Where the mean score of those ranges is better than
  the the mean score of all rows.
  
````python
def ranges(t,atLeast=0):
  out = []
  for column  in t.indep: 
    tmp = sdiv(t.data,attr=t.names[column],
              tiny = the.RULER.ranges.tiny,
              x    = lambda z : z[column],
              y    = lambda z : z.score,
              small= the.RULER.ranges.small)
    if len(tmp) > 1: # this column is useful
        out += tmp 
  return [one for one in out if # better mu than b4
          better(one.y.mu,atLeast)]

def ruler(t):
  b4       = N(map(lambda l:l.score,t.data))
  hitherto = b4.mu  
  rules    = map(lambda z : Rule([z],z.rows),
                 ranges(t, hitherto))
  n = 0 
  for _ in xrange(the.RULER.rules.retries):
    rules = sorted(rules,key=lambda z: z.score)[-1*the.Ruler.rules.beam:] 
    for i in xrange(the.RULER.rules.repeats): 
      n += 1
      rule1  = random.choice(rules)
      rule2  = random.choice(rules) 
      rule3  = rule1+rule2
      if rule3:
        if rule3.score > hitherto: 
          if the.RULER.rules.enough(rule3.rows,t.data):
            hitherto = rule3.score
            rules += [rule3]
  return sorted(rules,key=lambda z: z.score)[-1])

````
