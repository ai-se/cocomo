from __future__ import division,print_function
import sys 
sys.dont_write_bytecode = True


from optimo import *

#@go
def _sampleN():
  for rx,t in sampleN(samples=1000):
    for k in t.d():
      if k != "data":
        print(k, t[k])
    d = t.data[20]
    for name,x in zip(t.names,d):
       print("\t",rx,d.id,d.score,name,x)
    exit()

@go
def _sampleNranges():
  LIB(seed=1)
  RULER(tiny=33)
  def _ranges():
    for rx,t in sampleN(samples=1000):
       print("\n=========",rx,"============\n"),
       for z in ranges(t): print("\t",z)
  run(_ranges)

PROJECTS  = [flight,ground,osp,osp2,anything]
TREATMENTS= [doNothing, improvePersonnel, improveToolsTechniquesPlatform,
             improvePrecendentnessDevelopmentFlexibility, 
             increaseArchitecturalAnalysisRiskResolution, relaxSchedule,
             improveProcessMaturity, reduceFunctionality]

@go
def _sampleNuler():
  LIB(seed=1)
  RULER(tiny=30,repeats=64,beam=32,fresh=0.5,better=gt)
  def _ruler():
    for rx,t in sampleN(samples=1000,
                        projects=PROJECTS,
                        treatments=TREATMENTS):
      print("\n=========",rx,"============\n"),
      print(t.score, "baseline :",len(t.data))
      for z in ruler(t):
        print(z.score,z)
  run(_ruler)

