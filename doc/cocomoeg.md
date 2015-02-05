<small>_This file is part of cocomo. To know more, view the source code [cocomoeg.py](../src/cocomoeg.py) or read our [home](https://github.com/ai-se/cocomo) page._</small>

# Test Cases for COCOMO

````python
from cocomo import *

@go
def _complete():
  for _ in range(3):
    print("\n",complete(flight))
    

@go
def _sample1():
  sample(projects=[flight,anything]) 
 
PROJECTS  = [flight,ground,osp,osp2,anything]
TREATMENTS= [doNothing, improvePersonnel, improveToolsTechniquesPlatform,
             improvePrecendentnessDevelopmentFlexibility, 
             increaseArchitecturalAnalysisRiskResolution, relaxSchedule,
             improveProcessMaturity, reduceFunctionality]
             

@go
def _efforts():
  sample(projects=PROJECTS)

@go
def _effortsTreated():
  for project in PROJECTS:
    print("\n#### ",project.__name__," ","#"*50,"\n")
    sample(projects=[project],treatments=TREATMENTS)
 
````
