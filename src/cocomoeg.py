from __future__ import division,print_function
import sys,random
sys.dont_write_bytecode = True

"""

# Test Cases for COCOMO

"""
from cocomo import *

@go
def _range():
 for n in xrange(2):
    all= complete(flight)
    print("\n",n)
    for k,v in all.items():
      print("\t",k,v)


def sample(seed=1,n=1000,rxs=[doNothing], 
           score=COCOMO2,what='effort',
           projects=[anything,flight,ground,osp,osp2],
           ):  
  rseed(seed)
  COL()
  the.COL.buffer=n 
  minMax=N()
  logs={}
  for project in projects:
    say("|")
    lst = logs[project.__name__] = []
    for rx in rxs:
      say(".")
      log = N()
      log.name =  rx.__name__
      lst += [log]
      for _ in xrange(n):
        settings = complete(project, rx() or {})
        x = score(settings)
        log.tell(x)
        minMax.tell(x)
  print("")
  for project in projects:
    p = project.__name__
    lst = logs[p]
    lst = sorted(lst,
                 key = lambda log: log.median())
    if len(rxs) > 1: 
      print("")
    last=lst[0]
    rank=1; 
    for log in lst:
      str = xtile(log.kept(),
                 lo=minMax.lo,
                 hi=minMax.hi, 
                 chops=[ 0.1,0.3,0.5,0.7,0.9 ],
                 marks=["-"," "," ","-" ],
                 width=40,
                 show= "%5d")
      if cliffsDelta(log.kept(),last.kept()):
        rank += 1
      last = log
      pre = '%3s,' % rank if len(rxs)> 1 else '    '
      print(pre+str, ',%s,%s,' % (p,log.name))

@go
def _efforts(): 
  sample()
 

@go
def _badSmells(): 
  sample(score=badSmell)

@go
def _ospStinks(model=None,rx=None):
  rseed(1)
  for v,(x1,v1,x2,v2) in \
      whatStinks(model or osp, 
                 rx=rx or \
                         dict(cplx=[4],
                              rely=[1,2,3,5])):
    print('stink = %5s when' % v,
          x1,'=',v1,'and',x2,'=',v2)

@go
def _treatedProjectEffort():
 sample(rxs=rx(),projects=[anything,flight,ground,osp,osp2]) 

@go
def _treatedProjectSmell():
 sample(rxs=rx(),score=badSmell,
        projects=[anything,flight,ground,osp,osp2]) 

"""
"*" not in right place
also, noeed to check treatments are actyually workinf
3345.84795964 (- *  -----     |              ),    4,  1367,  3345,  5771, 12018 anything(reduceFunctionality),
6177.82686741 (---    *   ----|-----------   ),    6,  2660,  6177, 10087, 24230 anything(improvePrecendentnessDevelopmentFlexibility),
6849.67132806 (--   *   ------|---           ),   11,  2682,  6849, 11512, 24972 anything(increaseArchitecturalAnalysisRiskResolution),
7051.03224069 (--   *   ------|------------- ),   17,  3111,  7051, 11976, 37848 anything(improvePersonnel),
7072.58607921 (--    *   -----|----------    ),   19,  3080,  7072, 11390, 29063 anything(improveProcessMaturity),
7239.65938544 (--    *   -----|------------- ),    7,  2869,  7239, 11924, 34058 anything(improveTeam),
7251.61545498 (--    *    ----|------------- ),    6,  2805,  7251, 12708, 32442 anything(reduceQuality),
7500.63196142 (--   *    -----|--------      ),    6,  3049,  7500, 13376, 31301 anything(relaxSchedule),
7831.11742136 (--    *   -----|------        ),   17,  3404,  7831, 13105, 28934 anything(improveToolsTechniquesPlatform),
8221.04571379 (--    *   -----|------------- ),    6,  3731,  8221, 13210, 37938 anything(doNothing),
"""

      
 