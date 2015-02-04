<small>_This file is part of LEANER. To know more, view the source code [cocomo.py](../src/cocomo.py) or read our [home](https://github.com/ai-se/cocomo) page._</small>

# Software Effort and Risk Estimation

````python

from columns import *

````

## Core COCOMO Equation.

From the Boehm'00 book [Software Cost Estimation with Cocomo II][boehm00].

[boehm00]: http://goo.gl/kJE87M "Barry W. Boehm, Clark, Horowitz, Brown, Reifer, Chulani, Ray Madachy, and Bert Steece. 2000. Software Cost Estimation with Cocomo II (1st ed.). Prentice Hall"

Take a dictionary whose keys describe COCOMO attributes.
Look up the value of those keys in a array of tunings.

Using the above, generate some estimates, measured in terms of
_development months_ where one month
is 152 hours work by one developer (and includes development and management hours).
For example, if _effort_=100, then according to COCOMO,
five developers would finish
the project in 20 _months_.

````python
def COCOMO2(project, t=None,a=2.94, b=0.91):
  t=t or Coc2tunings
  sfs, ems, kloc = 0, 1, 10
  for k,setting in project.items():
    if k == 'kloc':
      kloc = setting
    else:
      values = t[k]
      value  = values[setting - 1]
      if k[0].isupper: sfs += value 
      else           : ems *= value
  return a * ems * kloc**(b + 0.01 * sfs)
````

__LESSON 1__: According to Boehm,
development effort is exponential on lines of code 
But there is more to it that just size.
  Effort is changed linearly by a set of _effort multipliers_ (`em`) and
  exponentially by some _scale factors_ (`sf`).

```
scale          | Prec |  have we done this before?
factors        | Flex |  development flexibility 
(exponentially | Resl |  any risk resolution activities?
 decrease      | Team |  team cohesion
 effort)       | Pmat |  process maturity
------------------------------------------------------------
upper          | acap |  analyst capability
(linearly      | pcap |  programmer capability
 decrease      | pcon |  programmer continuity
 effort)       | aexp |  analyst experience
               | pexp |  programmer experience
               | ltex |  language and tool experience
               | tool |  use of tools
               | site |  multiple site development
               | sced |  length of schedule   
-----------------------------------------------------------
lower          | rely |  required reliability  
(linearly      | data |  secondary memory  storage requirements
 increase      | cplx |  program complexity
 effort)       | ruse |  software reuse
               | docu |  documentation requirements
               | time |  runtime pressure
               | stor |  main memory requirements
               | pvol |  platform volatility  
```

__LESSON 2__ : The factors that effect delivery are not just
what code is being developed. The above factors divide into:

+ Product attributes: _what _ is being developed 
  (rely, data, clx, ruse, doco);
+ Platform attributes: _where_ is it being developed
  (time, stor, pvol);
+ Personnel attributes: _who_ is doing the work
  (acap, pcal, pcon, aexp, pexp, ltex);
+ Project attributes: _how_ is it being developed
  (tools, site, sced).
+ And the _misc_ scale factors: Prec, Flex, Resl, Team, Pmat.

The `COCOMO2` code uses the following set of tunings
that Boehm learned, sort of, from 161 projects from
commercial, aerospace, government, and non-profit
organizations-- mostly from the period 1990 to 2000
(I saw "sort of" cause Boehm actually "fiddled" with
these numbers, here and there, using his domain
knowledge).

Here are the actual tunings. The variables can range
from very low to extremely high. The first few
variables decrease effort exponentially and to
distinguish those _scale factors_, we will start
them with an upper case letter.

````python
_ = None;  Coc2tunings = dict(
#              vlow  low   nom   high  vhigh  xhigh   
  Flex=[        5.07, 4.05, 3.04, 2.03, 1.01,    _],
  Pmat=[        7.80, 6.24, 4.68, 3.12, 1.56,    _],
  Prec=[        6.20, 4.96, 3.72, 2.48, 1.24,    _],
  Resl=[        7.07, 5.65, 4.24, 2.83, 1.41,    _],
  Team=[        5.48, 4.38, 3.29, 2.19, 1.01,    _],
  acap=[        1.42, 1.19, 1.00, 0.85, 0.71,    _],
  aexp=[        1.22, 1.10, 1.00, 0.88, 0.81,    _],
  cplx=[        0.73, 0.87, 1.00, 1.17, 1.34, 1.74],
  data=[           _, 0.90, 1.00, 1.14, 1.28,    _],
  docu=[        0.81, 0.91, 1.00, 1.11, 1.23,    _],
  ltex=[        1.20, 1.09, 1.00, 0.91, 0.84,    _],
  pcap=[        1.34, 1.15, 1.00, 0.88, 0.76,    _], 
  pcon=[        1.29, 1.12, 1.00, 0.90, 0.81,    _],
  pexp=[        1.19, 1.09, 1.00, 0.91, 0.85,    _], 
  pvol=[           _, 0.87, 1.00, 1.15, 1.30,    _],
  rely=[        0.82, 0.92, 1.00, 1.10, 1.26,    _],
  ruse=[           _, 0.95, 1.00, 1.07, 1.15, 1.24],
  sced=[        1.43, 1.14, 1.00, 1.00, 1.00,    _], 
  site=[        1.22, 1.09, 1.00, 0.93, 0.86, 0.80], 
  stor=[           _,    _, 1.00, 1.05, 1.17, 1.46],
  time=[           _,    _, 1.00, 1.11, 1.29, 1.63],
  tool=[        1.17, 1.09, 1.00, 0.90, 0.78,    _]) 
````

## Defining Legal Ranges

The above lets us define legal
range for inputs to the COCOMO model. For example:

+ For `tool`, those legal values are 1,2,3,4,5 (cause
  the most-right-hand-side value is empty.
+ For `site`, those legal values are 1,2,3,4,5,6. 

We use this later as part of some routines to
explore options with software projects.

````python
def ranges(t=None):
  t = t or Coc2tunings
  out= {k:[n+1 for n,v in enumerate(lst) if v]
        for k,lst in t.items()}
  out["kloc"] = xrange(2,1001)
  return out
````

(Note that I slipped in the range of value `kloc` values
into `ranges` (2 to 1000).)

Using `ranges`, we can do a little defensive programming.
Suppose a function describes a project by return a dictionary
whose keys are meant to be valid COCOMO variables and whose
values are meant to be numbers for legal COCOMO ranges.
The following decorator calls that function at load time
and compile time and checks that all its keys and
values are valid. For an example of its usage, see below
(the functions describing JPL projects).

````python
def ok(f):
  all    = ranges()
  prefix = f.__name__
  for k,some in f().items():
    if k == 'nkloc': continue
    if not k in all:
      raise KeyError( '%s.%s' % (prefix,k))
    else:
      possible   = all[k]
      impossible = set(some) - set(possible)
      if impossible:
        raise IndexError( '%s.%s=%s' % 
                          (prefix,k,impossible))
  return f
````

## Handling Uncertainty

In practice, we rarely know all the exact COCOMO factors for
any project with 100% certainty. So the real game with effort
estimation is study estimates across a _space of possibilities_.

For example, after talking to some experts at NASA's Jet Propulsion
Laboratory, here are some descriptors of various NASA projects.
Some of these are point values (for example, for flight guidance
systems, reliabilty must be as high as possible so we set it to its
maximum value of 5). However, many
other variables are really  _ranges_ of values
representing the space of options within certain software being built
at NASA.

````python

@ok
def flight():
  "JPL Flight systems"
  return dict(
    kloc= xrange(7,418),
    Pmat = [2,3],         aexp = [2,3,4,5],
    cplx = [3,4,5,6],     data = [2,3],
    ltex = [1,2,3,4],     pcap = [3,4,5],
    pexp = [1,2,3,4],     rely = [3,4,5],
    stor = [3,4],         time = [3,4],         
    acap = [3,4,5],
    sced = [3],
    tool = [2]) 

@ok
def ground():
  "JPL ground systems"
  return dict(
    kloc=xrange(11,392),
    Pmat = [2,3],         acap = [3,4,5],
    aexp = [2,3,4,5],     cplx = [1,2,3,4],
    data = [2,3],         rely = [1,2,3,4],
    ltex = [1,2,3,4],     pcap = [3,4,5],
    pexp = [1,2,3,4],     time = [3,4],
    stor = [3,4],         
    tool = [2],           
    sced = [3])

@ok
def osp():
  "Orbital space plane. Flight guidance system."
  return dict(
    kloc= xrange(75,125),
    Flex = [2,3,4,5],     Pmat = [1,2,3,4],
    Prec = [1,2],         Resl = [1,2,3],
    Team = [2,3],         acap = [2,3],
    aexp = [2,3],         cplx = [5,6],
    docu = [2,3,4],       ltex = [2,3,4],       
    pcon = [2,3],         tool = [2,3],        
    ruse = [2,3,4],       sced = [1,2, 3],
    stor = [3,4,5],
    data = [3],
    pcap = [3],
    pexp = [3],
    pvol = [2],
    rely = [5],
    site = [3])

@ok
def osp2():
  """Osp, version 2. Note there are more restrictions
  here than in osp version1 (since as a project
  develops, more things are set in stone)."""
  return dict(
    kloc= xrange(75,125),
    docu = [3,4],         ltex = [2,5],
    sced = [2,3,4],       Pmat = [4,5],         
    Prec = [3,4, 5],
    Resl = [4],           Team = [3],
    acap = [4],           aexp = [4],
    cplx = [4],           data = [4],
    Flex = [3],           pcap = [3],
    pcon = [3],           pexp = [4],
    pvol = [3],           rely = [5],
    ruse = [4],           site = [6],           
    stor = [3],           time = [3],           
    tool = [5])

@ok
def anything(): 
  "Anything goes."
  return ranges()
````

### Complete-ing

Note that some of these descriptions are more detailed than others.
For example:

+  For _flight systems_, we just do not know the range of
   possibilities for (e.g.) _site_. 
+  For the  last function (`anything`), nothing is mentioned at all
   so an `anything` project samples across the entire range 
   of everything.

To complete these partial descriptions, we need to _complete_ them.
Any value missing from these
descriptions is assumed to range over its full range (min to max).
The following code:

+ `ranges()` looks up the ranges for `all` COCOMO values 
+ `project()` makes some `decisions` by selecting one value
   for each range of a particular project.
+ `guess()` replaces a range with one value, picked at random
+ The guesses from the project are then added to  `all`.

````python
def complete(project, rx=None, allRanges=ranges()):
  rx = rx or {}
  p = project()
  for k,default in allRanges.items():
    if not k in p:
      p[k] = default
  for k,rx1 in rx.items():
    if k == 'nkloc':
        p['kloc'] = [ ask(p['kloc']) * rx1[0] ] 
    else:
      overlap = list(set(p[k]) & set(rx1))
      if overlap:
        p[k] = overlap
  return  {k: ask(x) for k,x in p.items()}
````


For example, here some code to generate projects that are consistent
with what we know about `flight` projects:

```
all,_ = complete(flight)
for k,v in all.items():
       print("\t",k,v)

 	 Flex 3
	 Pmat 2
	 Prec 3
	 Resl 2
	 Team 5
	 acap 4
	 aexp 3
	 cplx 6
	 data 3
	 docu 3
	 kloc 385
	 ltex 3
	 pcap 4
	 pcon 4
	 pexp 3
	 pvol 4
	 rely 3
	 ruse 3
	 site 6
	 stor 3
	 time 4
	 tool 2
    sced 3
```

## Putting It All Together

Using the above, we can generate (say) 1000 projects at random
that conform to the constraints of `fight`, `ground`, `osp`, `osp2`
and study their effort estimates.

The generated distributions are as follows. Note that the anything/osp2
projects have the largest/smallest ranges since they have the least/most
constraints.

```
                                               min  25-th  50-th  75-th  max
                                             =====  =====  =====  =====  ====
 anything, (--    *  ------|------------- ),    7,  3778,  8716, 13892, 41697
   flight, (- *---         |              ),   32,  1433,  2888,  4721,  9729
   ground, ( *----         |              ),   57,  1051,  2387,  3975,  8665
      osp, (*              |              ),  718,  1092,  1294,  1521,  2146
     osp2, (*              |              ),  515,   683,   816,   924,  1151
```

In the effort estimation literature, it is usual to
report the 50 to 75th percentile as the estimate.

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

## What to Do?

So now we know that if we specify the range of possibilities in a project,
and sample across that range, that projects can have widely varying
estimates and, sometimes, can really smell really bad.

What to do? How to find project settings that let us deliver most code,
with least effort, while incurring fewest smells? Formally this is an 
_optimization_ problem of the form _(decisions,objectives)_ where

+ _Decisions_ are some values selected from the ranges of 
  of our projects (e.g. `flight`, `ground`, `osp`, etc);
+ The _objectives_ are to minimize _effort_, _badSmells_ while
  maximizing _kloc_

To guide this search we will run our projects 1000 times and then
(to make a level playing field), normalize all the efforts, badSmells
and kloc to 0..1 for min to max. Then we will score each project with a formula
that gets _better_ the further we move from the worst case
scenario of _(kloc,badSmells,effort) = (0,1,1)_. For that,
we will add _kloc_ to a _likes_ list and _badSmells,effort_
to a _dislikes_ list:

```
def fromHell(goods,bads):
    n, all = 0, 0
    for v in goods:
      n   += 1
      all += (0 - v)**2
    for v in bads:
      n   += 1
      all += (1 - v)**2
    return all**0.5 / n**5
```

(We divide by the square root of the number of
dimensions, just for convenience-- the resulting
score will be bounded 0 to 1 for worst to best.)

Lastly, we divide our results into the  _best_
top-half scores and the _rest_ then look for decisions
that are more common in _best_ than _rest_.

````python
def eval1(settings):
  est   = COCOMO2(settings)
  smell = badSmell(settings)
  kloc  = settings["kloc"]
  return [kloc],[est,smell]
  
def run1(project, rx=None):
  settings,decisions = complete(project,rx)  
  good,bad = eval1(settings)
  del  decisions["kloc"]
  return o(decisions = decisions,
              good   = good,
              bad    = bad)

def run(project, n=1000, enough=0.33):
  print("")
  baseline = [ run1(project) for _ in xrange(n) ]
  report(baseline, project.__name__+"(baseline)",['kloc'], ['effort','smell'])
  policies = bore(baseline,enough=enough)
  todo=[]
  print(len(policies))
  for _,(k,v) in policies:
    todo += [(k,v)]
    p  = {k1:v1 for k1,v1 in todo}
    rx = [ run1(project,p) for _ in xrange(n) ]
    report(rx, 
           project.__name__+'('+str(len(todo)) +')'+(str((k,v))),
           ['kloc'], ['effort','smell'])

def des(project,n=40,cf=0.3,f=0.5):
  def complete1(one):
    tmp = guess(ranges(),one)  
    return eval1(tmp)
  pop     =  [ run1(project) for _ in xrange(n*20) ]
  print(pop[0].decisions.keys())
  good,bad = ['kloc'],['effort','smell']
  report(pop, project.__name__+"(baseline)", good,bad)
  for generation in range(n):
    pop,log = de(pop,score=complete1,cf=cf,f=f)
    if generation % 5 == 0:
      report(pop, project.__name__+"("+str(generation+1)+")", good,bad)
  
def report(log,what,goodis,badis):
  bads  = [N() for _ in log[0].bad]
  goods = [N() for _ in log[0].good]
  for one in log:
    for n,v in enumerate(one.bad):
      bads[n].tell(v)
    for n,v in enumerate(one.good):
      goods[n].tell(v)
  out=[what]
  for x,v in zip(badis,bads)  : 
    out += [x]
    q2,q3 = v.q2q3()
    out += g([q2,q3],n=0)
  for x,v in zip(goodis,goods): 
    out += [x]
    q2,q3 = v.q2q3()
    out += g([q2,q3],n=0)
  print(out)

def rx(f=None,all=[]):
  if not f: 
    return all
  else:
    all += [f]
    return ok(f) 
    
@rx
def doNothing(): return {}

@rx
def improvePersonnel(): return dict(
  acap=[5],pcap=[5],pcon=[5], aexp=[5], pexp=[5], ltex=[5])

@rx
def improveToolsTechniquesPlatform(): return dict(
  time=[3],stor=[3],pvol=[2],tool=[5], site=[6])
  
@rx
def improvePrecendentnessDevelopmentFlexibility(): return dict(
  Prec=[5],Flex=[5])

@rx
def increaseArchitecturalAnalysisRiskResolution(): return dict(
  Resl=[5])
  
@rx
def relaxSchedule(): return dict(
  sced = [5])
  
@rx
def improveProcessMaturity(): return dict(
  Pmat = [5])
  
@rx
def reduceFunctionality(): return dict(
  data = [2], nkloc=[0.5])
  
@rx
def improveTeam(): return dict(
  Team = [5])
  
@rx
def reduceQuality():  return dict(
  rely = [1], docu=[1], time = [3], cplx = [1])
           
def COCONUT(training,          # list of projects
            a=10, b=1,         # initial  (a,b) guess
            deltaA    = 10,    # range of "a" guesses 
            deltaB    = 0.5,   # range of "b" guesses
            depth     = 10,    # max recursive calls
            constricting=0.66):# next time,guess less
  if depth > 0:
    useful,a1,b1= GUESSES(training,a,b,deltaA,deltaB)
    if useful: # only continue if something useful
      return COCONUT(training, 
                     a1, b1,  # our new next guess
                     deltaA * constricting,
                     deltaB * constricting,
                     depth - 1)
  return a,b

def GUESSES(training, a,b, deltaA, deltaB,
           repeats=20): # number of guesses
  useful, a1,b1,least,n = False, a,b, 10**32, 0
  while n < repeats:
    n += 1
    aGuess = a1 - deltaA + 2 * deltaA * rand()
    bGuess = b1 - deltaB + 2 * deltaB * rand()
    error  = ASSESS(training, aGuess, bGuess)
    if error < least: # found a new best guess
      useful,a1,b1,least = True,aGuess,bGuess,error
  return useful,a1,b1

def ASSESS(training, aGuess, bGuess):
   error = 0.0
   for project in training: # find error on training
     predicted = COCOMO2(project, aGuess, bGuess)
     actual    = effort(project)
     error    += abs(predicted - actual) / actual
   return error / len(training) # mean training error

def nasa93():
  vl=1;l=2;n=3;h=4;vh=5;xh=6
  return dict(
    sfem=21,
    kloc=22,
    effort=23,
    names= [ 
     # 0..8
     'Prec', 'Flex', 'Resl', 'Team', 'Pmat', 'rely', 'data', 'cplx', 'ruse',
     # 9 .. 17
     'docu', 'time', 'stor', 'pvol', 'acap', 'pcap', 'pcon', 'aexp', 'plex',  
     # 18 .. 25
     'ltex', 'tool', 'site', 'sced', 'kloc', 'effort', '?defects', '?months'],
    projects=[
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,25.9,117.6,808,15.3],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,24.6,117.6,767,15.0],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,7.7,31.2,240,10.1],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,8.2,36,256,10.4],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,9.7,25.2,302,11.0],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,2.2,8.4,69,6.6],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,3.5,10.8,109,7.8],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,66.6,352.8,2077,21.0],
	[h,h,h,vh,h,h,l,h,n,n,xh,xh,l,h,h,n,h,n,h,h,n,n,7.5,72,226,13.6],
	[h,h,h,vh,n,n,l,h,n,n,n,n,l,h,vh,n,vh,n,h,n,n,n,20,72,566,14.4],
	[h,h,h,vh,n,n,l,h,n,n,n,n,l,h,h,n,vh,n,h,n,n,n,6,24,188,9.9],
	[h,h,h,vh,n,n,l,h,n,n,n,n,l,h,vh,n,vh,n,h,n,n,n,100,360,2832,25.2],
	[h,h,h,vh,n,n,l,h,n,n,n,n,l,h,n,n,vh,n,l,n,n,n,11.3,36,456,12.8],
	[h,h,h,vh,n,n,l,h,n,n,n,n,h,h,h,n,h,l,vl,n,n,n,100,215,5434,30.1],
	[h,h,h,vh,n,n,l,h,n,n,n,n,l,h,h,n,vh,n,h,n,n,n,20,48,626,15.1],
	[h,h,h,vh,n,n,l,h,n,n,n,n,l,h,n,n,n,n,vl,n,n,n,100,360,4342,28.0],
	[h,h,h,vh,n,n,l,h,n,n,n,xh,l,h,vh,n,vh,n,h,n,n,n,150,324,4868,32.5],
	[h,h,h,vh,n,n,l,h,n,n,n,n,l,h,h,n,h,n,h,n,n,n,31.5,60,986,17.6],
	[h,h,h,vh,n,n,l,h,n,n,n,n,l,h,h,n,vh,n,h,n,n,n,15,48,470,13.6],
	[h,h,h,vh,n,n,l,h,n,n,n,xh,l,h,n,n,h,n,h,n,n,n,32.5,60,1276,20.8],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,19.7,60,614,13.9],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,66.6,300,2077,21.0],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,29.5,120,920,16.0],
	[h,h,h,vh,n,h,n,n,n,n,h,n,n,n,h,n,h,n,n,n,n,n,15,90,575,15.2],
	[h,h,h,vh,n,h,n,h,n,n,n,n,n,n,h,n,h,n,n,n,n,n,38,210,1553,21.3],
	[h,h,h,vh,n,n,n,n,n,n,n,n,n,n,h,n,h,n,n,n,n,n,10,48,427,12.4],
	[h,h,h,vh,h,n,vh,h,n,n,vh,vh,l,vh,n,n,h,l,h,n,n,l,15.4,70,765,14.5],
	[h,h,h,vh,h,n,vh,h,n,n,vh,vh,l,vh,n,n,h,l,h,n,n,l,48.5,239,2409,21.4],
	[h,h,h,vh,h,n,vh,h,n,n,vh,vh,l,vh,n,n,h,l,h,n,n,l,16.3,82,810,14.8],
	[h,h,h,vh,h,n,vh,h,n,n,vh,vh,l,vh,n,n,h,l,h,n,n,l,12.8,62,636,13.6],
	[h,h,h,vh,h,n,vh,h,n,n,vh,vh,l,vh,n,n,h,l,h,n,n,l,32.6,170,1619,18.7],
	[h,h,h,vh,h,n,vh,h,n,n,vh,vh,l,vh,n,n,h,l,h,n,n,l,35.5,192,1763,19.3],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,5.5,18,172,9.1],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,10.4,50,324,11.2],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,14,60,437,12.4],
	[h,h,h,vh,n,h,n,h,n,n,n,n,n,n,n,n,n,n,n,n,n,n,6.5,42,290,12.0],
	[h,h,h,vh,n,n,n,h,n,n,n,n,n,n,n,n,n,n,n,n,n,n,13,60,683,14.8],
	[h,h,h,vh,h,n,n,h,n,n,n,n,n,n,h,n,n,n,h,h,n,n,90,444,3343,26.7],
	[h,h,h,vh,n,n,n,h,n,n,n,n,n,n,n,n,n,n,n,n,n,n,8,42,420,12.5],
	[h,h,h,vh,n,n,n,h,n,n,h,n,n,n,n,n,n,n,n,n,n,n,16,114,887,16.4],
	[h,h,h,vh,h,n,h,h,n,n,vh,h,l,h,h,n,n,l,h,n,n,l,177.9,1248,7998,31.5],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,h,n,n,n,n,n,n,n,302,2400,8543,38.4],
	[h,h,h,vh,h,n,h,l,n,n,n,n,h,h,n,n,h,n,n,h,n,n,282.1,1368,9820,37.3],
	[h,h,h,vh,h,h,h,l,n,n,n,n,n,h,n,n,h,n,n,n,n,n,284.7,973,8518,38.1],
	[h,h,h,vh,n,h,h,n,n,n,n,n,l,n,h,n,h,n,h,n,n,n,79,400,2327,26.9],
	[h,h,h,vh,l,l,n,n,n,n,n,n,l,h,vh,n,h,n,h,n,n,n,423,2400,18447,41.9],
	[h,h,h,vh,h,n,n,n,n,n,n,n,l,h,vh,n,vh,l,h,n,n,n,190,420,5092,30.3],
	[h,h,h,vh,h,n,n,h,n,n,n,h,n,h,n,n,h,n,h,n,n,n,47.5,252,2007,22.3],
	[h,h,h,vh,l,vh,n,xh,n,n,h,h,l,n,n,n,h,n,n,h,n,n,21,107,1058,21.3],
	[h,h,h,vh,l,n,h,h,n,n,vh,n,n,h,h,n,h,n,h,n,n,n,78,571.4,4815,30.5],
	[h,h,h,vh,l,n,h,h,n,n,vh,n,n,h,h,n,h,n,h,n,n,n,11.4,98.8,704,15.5],
	[h,h,h,vh,l,n,h,h,n,n,vh,n,n,h,h,n,h,n,h,n,n,n,19.3,155,1191,18.6],
	[h,h,h,vh,l,h,n,vh,n,n,h,h,l,h,n,n,n,h,h,n,n,n,101,750,4840,32.4],
	[h,h,h,vh,l,h,n,h,n,n,h,h,l,n,n,n,h,n,n,n,n,n,219,2120,11761,42.8],
	[h,h,h,vh,l,h,n,h,n,n,h,h,l,n,n,n,h,n,n,n,n,n,50,370,2685,25.4],
	[h,h,h,vh,h,vh,h,h,n,n,vh,vh,n,vh,vh,n,vh,n,h,h,n,l,227,1181,6293,33.8],
	[h,h,h,vh,h,n,h,vh,n,n,n,n,l,h,vh,n,n,l,n,n,n,l,70,278,2950,20.2],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,0.9,8.4,28,4.9],
	[h,h,h,vh,l,vh,l,xh,n,n,xh,vh,l,h,h,n,vh,vl,h,n,n,n,980,4560,50961,96.4],
	[h,h,h,vh,n,n,l,h,n,n,n,n,l,vh,vh,n,n,h,h,n,n,n,350,720,8547,35.7],
	[h,h,h,vh,h,h,n,xh,n,n,h,h,l,h,n,n,n,h,h,h,n,n,70,458,2404,27.5],
	[h,h,h,vh,h,h,n,xh,n,n,h,h,l,h,n,n,n,h,h,h,n,n,271,2460,9308,43.4],
	[h,h,h,vh,n,n,n,n,n,n,n,n,l,h,h,n,h,n,h,n,n,n,90,162,2743,25.0],
	[h,h,h,vh,n,n,n,n,n,n,n,n,l,h,h,n,h,n,h,n,n,n,40,150,1219,18.9],
	[h,h,h,vh,n,h,n,h,n,n,h,n,l,h,h,n,h,n,h,n,n,n,137,636,4210,32.2],
	[h,h,h,vh,n,h,n,h,n,n,h,n,h,h,h,n,h,n,h,n,n,n,150,882,5848,36.2],
	[h,h,h,vh,n,vh,n,h,n,n,h,n,l,h,h,n,h,n,h,n,n,n,339,444,8477,45.9],
	[h,h,h,vh,n,l,h,l,n,n,n,n,h,h,h,n,h,n,h,n,n,n,240,192,10313,37.1],
	[h,h,h,vh,l,h,n,h,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,144,576,6129,28.8],
	[h,h,h,vh,l,n,l,n,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,151,432,6136,26.2],
	[h,h,h,vh,l,n,l,h,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,34,72,1555,16.2],
	[h,h,h,vh,l,n,n,h,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,98,300,4907,24.4],
	[h,h,h,vh,l,n,n,h,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,85,300,4256,23.2],
	[h,h,h,vh,l,n,l,n,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,20,240,813,12.8],
	[h,h,h,vh,l,n,l,n,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,111,600,4511,23.5],
	[h,h,h,vh,l,h,vh,h,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,162,756,7553,32.4],
	[h,h,h,vh,l,h,h,vh,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,352,1200,17597,42.9],
	[h,h,h,vh,l,h,n,vh,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,165,97,7867,31.5],
	[h,h,h,vh,h,h,n,vh,n,n,h,h,l,h,n,n,n,h,h,n,n,n,60,409,2004,24.9],
	[h,h,h,vh,h,h,n,vh,n,n,h,h,l,h,n,n,n,h,h,n,n,n,100,703,3340,29.6],
	[h,h,h,vh,n,h,vh,vh,n,n,xh,xh,h,n,n,n,n,l,l,n,n,n,32,1350,2984,33.6],
	[h,h,h,vh,h,h,h,h,n,n,vh,xh,h,h,h,n,h,h,h,n,n,n,53,480,2227,28.8],
	[h,h,h,vh,h,h,l,vh,n,n,vh,xh,l,vh,vh,n,vh,vl,vl,h,n,n,41,599,1594,23.0],
	[h,h,h,vh,h,h,l,vh,n,n,vh,xh,l,vh,vh,n,vh,vl,vl,h,n,n,24,430,933,19.2],
	[h,h,h,vh,h,vh,h,vh,n,n,xh,xh,n,h,h,n,h,h,h,n,n,n,165,4178.2,6266,47.3],
	[h,h,h,vh,h,vh,h,vh,n,n,xh,xh,n,h,h,n,h,h,h,n,n,n,65,1772.5,2468,34.5],
	[h,h,h,vh,h,vh,h,vh,n,n,xh,xh,n,h,h,n,h,h,h,n,n,n,70,1645.9,2658,35.4],
	[h,h,h,vh,h,vh,h,xh,n,n,xh,xh,n,h,h,n,h,h,h,n,n,n,50,1924.5,2102,34.2],
	[h,h,h,vh,l,vh,l,vh,n,n,vh,xh,l,h,n,n,l,vl,l,h,n,n,7.25,648,406,15.6],
	[h,h,h,vh,h,vh,h,vh,n,n,xh,xh,n,h,h,n,h,h,h,n,n,n,233,8211,8848,53.1],
	[h,h,h,vh,n,h,n,vh,n,n,vh,vh,h,n,n,n,n,l,l,n,n,n,16.3,480,1253,21.5],
	[h,h,h,vh,n,h,n,vh,n,n,vh,vh,h,n,n,n,n,l,l,n,n,n,  6.2, 12,477,15.4],
	[h,h,h,vh,n,h,n,vh,n,n,vh,vh,h,n,n,n,n,l,l,n,n,n,  3.0, 38,231,12.0],
	])

````
