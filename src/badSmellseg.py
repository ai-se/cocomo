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
             
 
@go
def _badSmells():
  sample(projects=PROJECTS,score=badSmell)

@go
def _badSmellsTreated():
  for project in PROJECTS:
    print("\n#### ",project.__name__," ","#"*50,"\n")
    sample(projects=[project],treatments=TREATMENTS,score=badSmell)

 
 

 