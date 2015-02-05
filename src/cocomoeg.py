from __future__ import division,print_function
import sys,random
sys.dont_write_bytecode = True

"""

# Test Cases for COCOMO

"""
from cocomo import *
 
PROJECTS  = [flight,ground,osp,osp2,anything]
TREATMENTS= [doNothing, improvePersonnel, improveToolsTechniquesPlatform,
             improvePrecendentnessDevelopmentFlexibility, 
             increaseArchitecturalAnalysisRiskResolution, relaxSchedule,
             improveProcessMaturity, reduceFunctionality]
             
def sample(samples=1000,
            projects=[anything],
            treatments=[doNothing],
            score=COCOMO2):
  samples = 1000
  results = []
  for project in projects:
    for treatment in treatments:
      what     = (project.__name__,treatment.__name__)
      result   = [score(complete(project,treatment()))  for _ in xrange(samples)]
      results += [[what] + result]
  xtiles(results,width=30,show="%7.1f")

#@go
def _efforts():
  sample(projects=PROJECTS)

#@go
def _effortsTreated():
  for project in PROJECTS:
    print("\n#### ",project.__name__," ","#"*50,"\n")
    sample(projects=[project],treatments=TREATMENTS)

#@go
def _badSmells():
  sample(projects=PROJECTS,score=badSmell)

@go
def _badSmellsTreated():
  for project in PROJECTS:
    print("\n#### ",project.__name__," ","#"*50,"\n")
    sample(projects=[project],treatments=TREATMENTS,score=badSmell)

 
 

 