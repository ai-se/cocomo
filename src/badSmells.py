from __future__ import division,print_function
import sys,random
sys.dont_write_bytecode = True

"""

# Test Cases for COCOMO

"""
from cocomo import *

"""
## Bad Smells

The concept of a _bad smell_ has been widely
discussed by [Fowler and Beck][fowler99], [Fontana
et al.][fontana12], and [others][codesmell]. Such
_bad smells_ are an indicator of problems within a
software project.  They are characteristics
of projects that may indicate a problem that makes
software hard to evolve and maintain, may trigger
refactoring of code, or delivering code late and
over budget.

More generally, in software engineering, bad smells
are any symptom in a program that possibly indicates
a deeper problem.  Such bad smells may not always
come from actual problems.  Instead, they indicate
some weakness in some aspect of the project that may
be slowing down development or increasing the risk
of bugs or failures in the future.


[fowler99]: http://v.gd/QglBdv  "Fowler, M. and K. Beck, Refactoring: improving the design of existing code . 1999: Addison Wesley Professional."

[fontana12]: http://www.jot.fm/issues/issue_2012_08/article5.pdf "Fontana, F.A. and Braione, P. and Zanoni, M. Automatic detection of bad smells in code: An experimental assessment Journal of Object Technology, Vol.11 No.2, 2012."

[codesmell]: http://en.wikipedia.org/wiki/Code_smell "Web Reference for code smell"

[Madachy and his students][madachy97] have worked
through combinations of COCOMO parameters to offer a
_bad smell_ detector for software projects.
For example, here is a bad smell:

+ The schedule is tight ;
+ And we are building very complex software;  
+ Or we are building software that runs in tight execution time constraints,

That is modeled the first table shown below. Tight
schedule means the first few rows of `sced` and
(e.g.) high complexity are the right-hand side
columns of `cplx`:

[madachy97]: http://v.gd/zyX09Q  "Raymond J. Madachy, Heuristic Risk Assessment Using Cost Factors, IEEE Software, vol. 14, no. 3, pp. 51-59, May/June, 1997"

"""

Stink={}

Stink[('sced','cplx')] = Stink[('sced','time')] = [
 [0,0,0,1,2,4],
 [0,0,0,0,1,2],
 [0,0,0,0,0,1],
 [0,0,0,0,0,0],
 [0,0,0,0,0,0],
 [0,0,0,0,0,0]]

"""

The rest of the tables have the same form:  there is one corner of the table where the stink is worse (rises to "2"). And if the stink is really bad, the
smell goes up to "4". Note that these numbers are not precise values; rather they are qualitative indicators of subjective human opinion. But see if
you disagree with any of the following:

"""

Stink[('sced','rely')] =  Stink[('sced','pvol')] = [
 [0,0,0,1,2,0],
 [0,0,0,0,1,0],
 [0,0,0,0,0,0],
 [0,0,0,0,0,0],
 [0,0,0,0,0,0],
 [0,0,0,0,0,0]]

Stink[('ltex','pcap')] = Stink[('sced','acap')] = \
Stink[('sced','pexp')] = Stink[('sced','pcap')] = \
Stink[('sced','aexp')] = [
 [4,2,1,0,0,0],
 [2,1,0,0,0,0],
 [1,0,0,0,0,0],
 [0,0,0,0,0,0],
 [0,0,0,0,0,0],
 [0,0,0,0,0,0]]

Stink[('sced','tool')] = Stink[('sced','ltex')] = \
Stink[('sced','Pmat')] = Stink[('Pmat','acap')] = \
Stink[('tool','acap')] = Stink[('tool','pcap')] = \
Stink[('tool','Pmat')] = Stink[('Team','aexp')] = \
Stink[('Team','sced')] = Stink[('Team','site')] = [
 [2,1,0,0,0,0],
 [1,0,0,0,0,0],
 [0,0,0,0,0,0],
 [0,0,0,0,0,0],
 [0,0,0,0,0,0],
 [0,0,0,0,0,0]]

Stink[('rely','acap')] = Stink[('rely','Pmat')] = \
Stink[('rely','pcap')] = [
 [0,0,0,0,0,0],
 [0,0,0,0,0,0],
 [1,0,0,0,0,0],
 [2,1,0,0,0,0],
 [4,2,1,0,0,0],
 [0,0,0,0,0,0]]

Stink[('cplx','acap')] = Stink[('cplx','pcap')] = \
Stink[('cplx','tool')] = Stink[('stor','acap')] = \
Stink[('time','acap')] = Stink[('ruse','aexp')] = \
Stink[('ruse','ltex')] = Stink[('Pmat','pcap')] = \
Stink[('stor','pcap')] = Stink[('time','pcap')] = [
 [0,0,0,0,0,0],
 [0,0,0,0,0,0],
 [0,0,0,0,0,0],
 [1,0,0,0,0,0],
 [2,1,0,0,0,0],
 [4,2,1,0,0,0]]

Stink[('pvol','pexp')] = [
 [0,0,0,0,0,0],
 [0,0,0,0,0,0],
 [0,0,0,0,0,0],
 [1,0,0,0,0,0],
 [2,1,0,0,0,0],
 [0,0,0,0,0,0]]

Stink[('time','tool')] = [
  [0,0,0,0,0,0],
  [0,0,0,0,0,0],
  [0,0,0,0,0,0],
  [0,0,0,0,0,0],
  [1,0,0,0,0,0],
  [2,1,0,0,0,0]]

"""

Using these `Stink` tables, we can check how bad our
projects smell.

"""

def badSmell(project,log=None):
  stink = 0
  for (x1,x2),m in Stink.items():
      v1     = project[x1] 
      v2     = project[x2]
      inc    = m[v1 - 1][v2 - 2]
      if inc and not log is None:
         key = (x1,v1,x2,v2)
         log[key] = log.get(key,0) + inc 
      stink += inc
  return stink

"""

Here's the bad smells seen in 1000 randomly generated projects. Note that
`osp` really stinks.

```
>>>  sample(projects=[flight,ground,osp,osp2,anything],
            score=badSmell)

rank | rx                        | median  |                                                                             
==== | ==                        | ======= |                                                                             
1    | ('ground', 'doNothing')   |     4.0 | ( -*            |              ),    0.0,     2.0,     4.0,     6.0,    14.0
2    | ('osp2', 'doNothing')     |     5.0 | (  -*           |              ),    4.0,     4.0,     5.0,     6.0,     8.0
3    | ('flight', 'doNothing')   |     8.0 | (   -*--        |              ),    0.0,     5.0,     8.0,    12.0,    32.0
3    | ('anything', 'doNothing') |     8.0 | (  --*---       |              ),    0.0,     4.0,     8.0,    14.0,    35.0
4    | ('osp', 'doNothing')      |    26.0 | (           ---*|--            ),    8.0,    20.0,    26.0,    32.0,    46.0
```

To see why, we  collected 1000 samples from `osp` and looked at the 
dozen worst  offenders.

"""
def whatStinks(project,n=1000,rx=None):
  log = {}
  for _ in xrange(n):
    settings = complete(project,rx or {})
    badSmell(settings,log)
  lst = sorted([(v,k) for k,v in log.items()],
                reverse=True)
  return lst[:12]
"""

Running the above code gives us a report
on what dumb things people are doing on projects.
E.g. as shown below, for _flight_ systems, we often do things
like building complex systems with very little tools support.

```python
def _whatStinks():
    rseed(1)
    for project in PROJECTS:
        print("\n",project.__name__)
        stinks = whatStinks(project)
        worst  = stinks[0][0]
        for stink,what in stinks:
            if stink > worst*0.5:
                print('stink = ',stink,' when ',what)
```

When this runs, it reports all stinks that are at least as bad
as half the worst stink.

```
>>> _whatStinks()

 flight
stink =  1048  when  ('cplx', 6, 'tool', 2)
stink =  712  when  ('rely', 5, 'Pmat', 2)

 ground
stink =  498  when  ('tool', 2, 'Pmat', 2)
stink =  261  when  ('sced', 3, 'cplx', 1)
stink =  260  when  ('rely', 4, 'Pmat', 2)
stink =  253  when  ('sced', 3, 'aexp', 2)

 osp
stink =  2000  when  ('rely', 5, 'pcap', 3)
stink =  1940  when  ('rely', 5, 'acap', 2)
stink =  1088  when  ('rely', 5, 'Pmat', 2)
stink =  1030  when  ('rely', 5, 'acap', 3)
stink =  1026  when  ('cplx', 6, 'pcap', 3)

 osp2
stink =  2000  when  ('rely', 5, 'pcap', 3)

 anything
stink =  220  when  ('time', 6, 'acap', 2)
stink =  212  when  ('stor', 6, 'pcap', 2)
stink =  200  when  ('ruse', 6, 'aexp', 2)
stink =  196  when  ('time', 6, 'pcap', 2)
stink =  196  when  ('sced', 1, 'aexp', 2)
stink =  184  when  ('sced', 1, 'pcap', 2)
stink =  168  when  ('stor', 6, 'acap', 2)
stink =  168  when  ('ruse', 6, 'ltex', 2)
stink =  164  when  ('sced', 1, 'pexp', 2)
stink =  144  when  ('rely', 5, 'pcap', 2)
stink =  140  when  ('sced', 1, 'acap', 2)
stink =  140  when  ('cplx', 6, 'pcap', 2)
``` 

Do our treatments effect the bad smells?
The following code shows that removing bad smells with (e.g.)
improved precedentless a development flexibility is just as useless
as doing nothing. But improving personnel can be very useful.

```python
def _badSmellsTreated():
  rseed(1)
  for project in [anything]: 
    sample(projects   = [project],
           treatments = TREATMENTS,
           score      = badSmell)
```

And what does that get us?

```
>>> _badSmellsTreated()
 
rank | rx                                                          | median  |                                                                             
==== | ==                                                          | ======= |                                                                             
1    | ('anything', 'improvePersonnel')                            |     2.0 | (-*             |              ),    0.0,     0.0,     2.0,     4.0,    12.0
2    | ('anything', 'improveToolsTechniquesPlatform')              |     5.0 | (  -*-          |              ),    0.0,     3.0,     6.0,    10.0,    25.0
2    | ('anything', 'relaxSchedule')                               |     6.0 | (  -*--         |              ),    0.0,     3.0,     6.0,    11.0,    26.0
3    | ('anything', 'improveProcessMaturity')                      |     8.0 | (  ---*--       |              ),    0.0,     4.0,     9.0,    15.0,    35.0
3    | ('anything', 'doNothing')                                   |     9.0 | (  ---*--       |              ),    0.0,     4.0,     9.0,    15.0,    35.0
3    | ('anything', 'improvePrecendentnessDevelopmentFlexibility') |     9.0 | (   --*--       |              ),    0.0,     5.0,     9.0,    15.0,    37.0
3    | ('anything', 'increaseArchitecturalAnalysisRiskResolution') |     9.0 | (  ---*--       |              ),    0.0,     4.0,     9.0,    15.0,    35.0
3    | ('anything', 'reduceFunctionality')                         |     9.0 | (   --*--       |              ),    0.0,     5.0,     9.0,    15.0,    34.0
```

"""
