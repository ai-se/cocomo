<small>_This file is part of cocomo. To know more, view the source code [cocomo.py](../src/cocomo.py) or read our [home](https://github.com/ai-se/cocomo) page._</small>

# Sample from the COCOMO Model

From the Boehm'00 book [Software Cost Estimation with Cocomo II][boehm00].

[boehm00]: http://goo.gl/kJE87M "Barry W. Boehm, Clark, Horowitz, Brown, Reifer, Chulani, Ray Madachy, and Bert Steece. 2000. Software Cost Estimation with Cocomo II (1st ed.). Prentice Hall"


The `COCOMO2` code uses the following set of tunings
that Boehm learned, sort of, from 161 projects from
commercial, aerospace, government, and non-profit
organizations-- mostly from the period 1990 to 2000
(I saw "sort of" cause Boehm actually "fiddled" with
these numbers, here and there, using his domain
knowledge).


## Overview

Q: What does this code do?  
A: It extracts valid projects from ranges describing:

+ Valid COCOMO ranges; a.k.a. "_Ranges(Base)_";
+ The space of options within one project; a.k.a "_Ranges(Project)_";
+ The suggested changes to that project; a.k.a. "_Ranges(Treatment)_";
    
The _intersection_ of that that space is the _result_ of changing a project.

Our goal is to use this tool to 

+ Assess planned changes;
+ And to find better changes.
       
## Example

### E.g. Ranges(Base) ###

The space of legal values for a COCOMO project. That looks like this:

````python
_ = None;  Coc2tunings = dict(
        #       vlow  low   nom   high  vhigh  xhigh   
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

For this code:

+ We use 1=v1ow, 2=low, 3=nom, 4=high, 5=vhigh, 6-xhigh.
+ The first few variables decrease effort exponentially.
+ To distinguish those _scale factors_ from the rest of the code, we  start
  them with an upper case letter.

### E.g. Ranges(Project) ###

The space of legal values for a project.

In  there any any uncertainties about that project then either:

+ The project description does not mention that item;
+ Or, that item is shown as a range of possible values.

```python
@ok # all functions defining projects have the prefix "@ok"
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
```

This is a decription of flight software from NASA's 
              Jet Propulsion lab.
              
+ Some things are known with certainity; e.g. 
              this team makes very little use of _tools_.
    + Hence, _tool = [2]_ has only one value
+ Many things are uncertain so:
    + We do not mention "team cohesion" (a.k.a. _team_)
                   so this can range very log to very high
    + We offer some things are ranges (e.g. _kloc_
                   and "process maturity" _pmat_)

### E.g. Ranges(treatment)

The planned change to the project.

For example, lets say someone decide to "treat" a project by
improving personnel.

```python
def improvePersonnel(): return dict(
  acap=[5],pcap=[5],pcon=[5], aexp=[5], pexp=[5], ltex=[5])
```

(Note that "improving personnel" is a sad euphism for sacking your current
contractors and hiring new ones with maximum analyst and programming capability 
as well as programmer continuity, experience with analysis, platform and this
development langauge.)
 

## The COCOMO Equation.


Using the above, generate some estimates, measured in terms of
_development months_ where one month
is 152 hours work by one developer (and includes development and management hours).
For example, if _effort_=100, then according to COCOMO,
five developers would finish
the project in 20 _months_.

````python
def COCOMO2(project, t=None,a=2.94, b=0.91):
  t=t or Coc2tunings # t = the big table of COCOMO tuning parameters
  sfs, ems, kloc = 0, 1, 10 # initializing some defaults
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


## Finding Ranges

We use the above to compute estimates for projects that have certain ranges.
Recall from the above those ranges are the intersection of

+ Valid COCOMO ranges (a.k.a. _Ranges(Base)_);
+ The space of options within one project (a.k.a _Ranges(Project)_);
+ The suggested changes to that project (a.k.a. Ranges(Treatment)_);

How do we specify all those ranges? Well...

### Finding "Ranges(Base)"

To find _Ranges(Base)_, we ask the _Coc2tunings_ table to report
all the non-None indexes it supports.

````python
def ranges(t=None):
  t = t or Coc2tunings
  out= {k:[n+1 for n,v in enumerate(lst) if v]
        for k,lst in t.items()}
  out["kloc"] = xrange(2,1001)
  return out
````

Two little details

+ Note one cheat:  I slipped in the range of value `kloc` values
  into `ranges` (2 to 1000).
+ Using `ranges`, we can do a little defensive programming.
    + Suppose a function describes a project by return a dictionary
      whose keys are meant to be valid COCOMO variables and whose
      values are meant to be numbers for legal COCOMO ranges.
    + The following decorator calls that function at load time
      and compile time and checks that all its keys and
      values are valid.  

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

For an example of using this function, see below.

### Defining "Ranges(Project)"
 
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

Note the addition of _@ok_ before each function. This means, at load time,
we check that all the following variables and ranges are valid.

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

### Defining "Ranges(Treatment)"

Lastly, we need to define what we are going to do to a project.

First, we define a little booking code that remembers all the 
treatments and, at load time, checks that the ranges are good.

````python
def rx(f=None,all=[]):
  if not f: return all
  all += [f]
  return ok(f) 
````

Ok, now that is done, here are the treatments. Note that they all start
with _@rx_. 

````python
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
  data = [2], nkloc=[0.5]) # nloc is a special symbol. Used to change kloc.
  
@rx
def improveTeam(): return dict(
  Team = [5])
  
@rx
def reduceQuality():  return dict(
  rely = [1], docu=[1], time = [3], cplx = [1])
````

### Under the Hood: Complete-ing the Ranges.

Now that we have defined _Ranges(Base), Ranges(Project), and
Ranges(Treatment)_, we need some tool to generate the ranges
of the currnet project, given some treatment. 
In the  following code:

+ `ranges()` looks up the ranges for `all` COCOMO values; i.e. the _Ranges(Base)_
+ `project()` accesses _Ranges(Project)_. For each of those ranges, we
  override _Ranges(Base)_.
+ Then we impose _Ranges(Treatment)_ to generate a list of valid ranges
  consistent with _Ranges(*)_ 
+ The guesses from the project are then added to  `ask` which
  pulls on value for each attribute.

```python
def ask(x):
  return random.choice(list(x))
```

And here's the code:

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
with what we know about `flight` projects. Note that we call it three
times and get three different project:

```python
>>> for _ in range(3):
      print("\n",complete(flight))

==>
 {'sced': 3, 'cplx': 5, 'site': 2, 'Prec': 3, 'Pmat': 3, 
  'acap': 3, 'Flex': 3, 'rely': 5, 'data': 2, 'tool': 2, 
  'pexp': 3, 'pcon': 1, 'aexp': 4, 'stor': 4, 'docu': 5, 
  'Team': 5, 'pcap': 5, 'kloc': 41, 'ltex': 1, 'ruse': 6, 
  'Resl': 2, 'time': 4, 'pvol': 3}

 {'sced': 3, 'cplx': 6, 'site': 5, 'Prec': 4, 'Pmat': 2, 
  'acap': 3, 'Flex': 2, 'rely': 5, 'data': 3, 'tool': 2, 
  'pexp': 1, 'pcon': 2, 'aexp': 4, 'stor': 3, 'docu': 1, 
  'Team': 3, 'pcap': 5, 'kloc': 63, 'ltex': 2, 'ruse': 3, 
  'Resl': 4, 'time': 3, 'pvol': 3}

 {'sced': 3, 'cplx': 5, 'site': 5, 'Prec': 4, 'Pmat': 2, 
  'acap': 5, 'Flex': 5, 'rely': 3, 'data': 3, 'tool': 2, 
   'pexp': 3, 'pcon': 5, 'aexp': 4, 'stor': 4, 'docu': 1, 
   'Team': 3, 'pcap': 4, 'kloc': 394, 'ltex': 2, 'ruse': 2, 
   'Resl': 1, 'time': 3, 'pvol': 5}
```
 
## Using  This Code

Finally, we can generate a range of estiamtes out of this code.

The following code builds _sample_ number of projects and scores
each one with _COCOMO2_ (later, we will score thse projects in other ways).
The results are pretty-printed using a utility called _xtiles_.

````python
def sample(samples=1000,
            projects=[anything],
            treatments=[doNothing],
            score=COCOMO2):
  samples = 1000
  results = []
  for project in projects:
    for treatment in treatments:
      what     = (project.__name__,treatment.__name__)
      result   = [score(complete(project,treatment()))  
                  for _ in xrange(samples)]
      results += [[what] + result]
  xtiles(results,width=30,show="%7.1f")
  
````

For example:

```python
>>> sample(projects=[flight,anything])

rank | rx                        | median  |                                                                             
==== | ==                        | ======= |                                                                             
1    | ('flight', 'doNothing')   |  2696.9 | ( -*-           |              ),   35.1,  1153.3,  2693.2,  4508.0,  8981.3
2    | ('anything', 'doNothing') |  8254.4 | (   ----*---    |              ),    6.9,  3610.8,  8238.5, 13651.2, 30233.4
```

Here's code to try all our treatments on all our projects:

```python
PROJECTS  = [flight,ground,osp,osp2,anything]
TREATMENTS= [doNothing, improvePersonnel, improveToolsTechniquesPlatform,
             improvePrecendentnessDevelopmentFlexibility, 
             increaseArchitecturalAnalysisRiskResolution, relaxSchedule,
             improveProcessMaturity, reduceFunctionality]
             

def _effortsTreated():
  for project in PROJECTS:
    print("\n#### ",project.__name__," ","#"*50,"\n")
    sample(projects=[project],treatments=TREATMENTS)
```

If executed, this generates the following:

### FLIGHT

```
rank | rx                                                        | median  |                                                                             
==== | ==                                                        | ======= |                                                                             
1    | ('flight', 'reduceFunctionality')                         |  1194.6 | ( --*-          |              ),   15.1,   575.0,  1193.5,  1972.7,  3370.3
2    | ('flight', 'improvePrecendentnessDevelopmentFlexibility') |  2222.4 | (   ----*---    |              ),   30.2,  1164.9,  2636.8,  4359.6,  8278.2
2    | ('flight', 'increaseArchitecturalAnalysisRiskResolution') |  2280.9 | (   ---*---     |              ),   36.1,  1078.5,  2279.8,  3951.5,  6785.6
2    | ('flight', 'improveToolsTechniquesPlatform')              |  2628.5 | (   ----*----   |              ),   30.2,  1128.8,  2624.8,  4509.4,  8597.5
2    | ('flight', 'relaxSchedule')                               |  2855.0 | (   ----*----   |              ),   39.9,  1289.6,  2853.6,  4603.2,  8251.3
2    | ('flight', 'improvePersonnel')                            |  2883.2 | (   -----*---   |              ),   50.5,  1299.8,  2881.8,  4634.9,  8604.1
2    | ('flight', 'doNothing')                                   |  2894.9 | (   -----*---   |              ),   36.0,  1265.8,  2893.6,  4643.0,  8435.4
2    | ('flight', 'improveProcessMaturity')                      |  3035.1 | (   -----*----  |              ),   33.8,  1248.4,  3029.8,  4775.5,  8949.9
```

### GROUND

```
rank | rx                                                        | median  |                                                                             
==== | ==                                                        | ======= |                                                                             
1    | ('ground', 'reduceFunctionality')                         |  1070.3 | ( --*-          |              ),   23.7,   495.3,  1068.4,  1676.3,  3052.0
2    | ('ground', 'improvePrecendentnessDevelopmentFlexibility') |  2039.5 | (   ----*---    |              ),   53.2,  1069.2,  2415.9,  3876.7,  7039.0
2    | ('ground', 'increaseArchitecturalAnalysisRiskResolution') |  2352.2 | (   ----*--     |              ),   53.2,  1075.9,  2351.4,  3574.0,  6312.3
2    | ('ground', 'doNothing')                                   |  2370.8 | (   ----*----   |              ),   56.3,  1023.3,  2366.4,  4148.4,  7851.0
2    | ('ground', 'relaxSchedule')                               |  2415.5 | (   ----*---    |              ),   67.6,  1129.4,  2415.2,  3928.6,  7449.6
2    | ('ground', 'improvePersonnel')                            |  2439.6 | (   ----*----   |              ),   60.5,  1084.0,  2436.4,  4004.7,  7001.9
2    | ('ground', 'improveToolsTechniquesPlatform')              |  2633.6 | (    ----*---   |              ),   59.7,  1240.2,  2630.5,  4132.5,  7105.8
2    | ('ground', 'improveProcessMaturity')                      |  2671.1 | (   -----*---   |              ),   62.2,  1112.3,  2670.7,  4213.4,  7527.8
```

### OSP

```
rank | rx                                                     | median  |                                                                             
==== | ==                                                     | ======= |                                                                             
1    | ('osp', 'reduceFunctionality')                         |   518.0 | (  --*          |              ),  279.6,   434.2,   517.9,   609.2,   803.1
2    | ('osp', 'improvePrecendentnessDevelopmentFlexibility') |  1200.2 | (           ---*|-             ),  658.2,   997.8,  1199.9,  1420.4,  1885.9
3    | ('osp', 'improvePersonnel')                            |  1291.1 | (            ---*---           ),  680.5,  1080.0,  1294.7,  1528.6,  2046.5
3    | ('osp', 'increaseArchitecturalAnalysisRiskResolution') |  1291.8 | (            ---*---           ),  716.0,  1081.1,  1291.6,  1529.8,  1992.9
3    | ('osp', 'relaxSchedule')                               |  1293.7 | (            ---*---           ),  680.5,  1082.4,  1293.3,  1531.0,  2039.3
3    | ('osp', 'improveToolsTechniquesPlatform')              |  1296.8 | (            ---*--            ),  743.4,  1076.1,  1296.4,  1521.4,  2043.7
3    | ('osp', 'improveProcessMaturity')                      |  1297.6 | (            ---*---           ),  716.3,  1084.1,  1297.2,  1536.5,  2102.5
3    | ('osp', 'doNothing')                                   |  1299.8 | (            ---*---           ),  698.9,  1079.7,  1299.8,  1545.8,  2054.4
```

### OSP2

```
rank | rx                                                      | median  |                                                                             
==== | ==                                                      | ======= |                                                                             
1    | ('osp2', 'reduceFunctionality')                         |   342.4 | (  --*          |              ),  226.0,   289.5,   342.4,   398.3,   475.2
2    | ('osp2', 'improveProcessMaturity')                      |   764.0 | (              -|--*---        ),  515.3,   671.3,   788.7,   913.3,  1114.4
2    | ('osp2', 'improvePrecendentnessDevelopmentFlexibility') |   769.0 | (              -|-*---         ),  515.3,   652.7,   767.2,   875.4,  1021.5
2    | ('osp2', 'increaseArchitecturalAnalysisRiskResolution') |   789.6 | (               |--*---        ),  518.4,   685.3,   789.3,   910.5,  1133.4
2    | ('osp2', 'improvePersonnel')                            |   797.6 | (              -|--*---        ),  517.7,   672.4,   797.6,   926.6,  1108.5
2    | ('osp2', 'doNothing')                                   |   797.9 | (              -|--*---        ),  520.9,   674.7,   797.9,   931.4,  1127.4
2    | ('osp2', 'improveToolsTechniquesPlatform')              |   805.8 | (              -|--*---        ),  517.7,   681.1,   805.6,   922.8,  1121.9
2    | ('osp2', 'relaxSchedule')                               |   811.8 | (               |---*---       ),  515.3,   685.5,   811.3,   936.7,  1133.4
```

### ANYTHING (all COOCMO)

```
rank | rx                                                          | median  |                                                                             
==== | ==                                                          | ======= |                                                                             
1    | ('anything', 'reduceFunctionality')                         |  3230.2 | ( -*-           |              ),    6.8,  1386.7,  3221.5,  5555.5, 11876.5
2    | ('anything', 'improvePrecendentnessDevelopmentFlexibility') |  6475.5 | (  ---*--       |              ),    7.0,  3039.2,  7214.9, 11984.9, 26446.2
2    | ('anything', 'increaseArchitecturalAnalysisRiskResolution') |  6490.5 | (  --*---       |              ),    7.2,  2709.7,  6476.9, 11278.4, 21944.9
2    | ('anything', 'improveProcessMaturity')                      |  6845.9 | (  ---*--       |              ),    7.0,  2897.5,  6821.6, 11083.2, 22207.5
2    | ('anything', 'improveToolsTechniquesPlatform')              |  7424.2 | (  ---*--       |              ),   20.5,  3259.0,  7417.8, 11993.4, 27895.3
2    | ('anything', 'improvePersonnel')                            |  7470.7 | (  ---*---      |              ),   18.7,  3324.8,  7470.4, 12509.5, 25775.5
2    | ('anything', 'relaxSchedule')                               |  7828.1 | (   --*---      |              ),   11.8,  3659.0,  7815.9, 13299.1, 28334.5
2    | ('anything', 'doNothing')                                   |  8212.3 | (  ----*---     |              ),   11.3,  3142.9,  8212.1, 13984.0, 28917.4
```

````python

 
````
