<small>_This file is part of cocomo. To know more, view the source code [badSmells.py](../src/badSmells.py) or read our [home](https://github.com/ai-se/cocomo) page._</small>

# Test Cases for COCOMO

````python
from cocomo import *

````
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

````python

Stink={}

Stink[('sced','cplx')] = Stink[('sced','time')] = [
 [0,0,0,1,2,4],
 [0,0,0,0,1,2],
 [0,0,0,0,0,1],
 [0,0,0,0,0,0],
 [0,0,0,0,0,0],
 [0,0,0,0,0,0]]

````

The rest of the tables have the same form:  there is one corner of the table where the stink is worse (rises to "2"). And if the stink is really bad, the
smell goes up to "4". Note that these numbers are not precise values; rather they are qualitative indicators of subjective human opinion. But see if
you disagree with any of the following:

````python

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

````

Using these `Stink` tables, we can check how bad our
projects smell.

````python

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

````

Here's the bad smells seen in 1000 randomly generated projects. Note that
`osp` really stinks.

```
      osp, (    -------   *|  ----------  ),    8,    19,    25,    32,    49
 anything, (--   *  -------|-------       ),    0,     5,     9,    15,    40
   flight, (--  * ------   |              ),    0,     5,     8,    11,    22
     osp2, (  *-           |              ),    4,     4,     5,     6,     8
   ground, (- *--------    |              ),    0,     2,     4,     6,    20
```

To see why, we  collected 1000 samples from `osp` and looked at the 
dozen worst  offenders.

````python
def whatStinks(project,n=1000,rx=None):
  log = {}
  for _ in xrange(n):
    settings = complete(project,rx or {})
    badSmell(settings,log)
  lst = sorted([(v,k) for k,v in log.items()],
                reverse=True)
  return lst[:12]
````

The results showed that, with `osp`, there are many
times we are trying to build highly reliable or
highly complex software using lower-end developers.

```
stink = 2.13 when rely = 5 and acap = 2
stink = 2.00 when rely = 5 and pcap = 3
stink = 1.08 when cplx = 6 and acap = 2
stink = 1.05 when rely = 5 and Pmat = 2
stink = 0.99 when cplx = 6 and pcap = 3
stink = 0.94 when rely = 5 and acap = 3
stink = 0.89 when cplx = 6 and tool = 2
stink = 0.71 when sced = 1 and acap = 2
stink = 0.65 when sced = 1 and aexp = 2
stink = 0.65 when sced = 1 and pexp = 3
stink = 0.65 when sced = 1 and pcap = 3
stink = 0.54 when cplx = 6 and tool = 3
```
Another problem, that appears four times at the end of the list,
is that we are rushing to complete the project using lower-end developers.


