<small>_This file is part of LEANER. To know more, view the source code [badSmellseg.py](../src/badSmellseg.py) or read our [home](https://github.com/ai-se/cocomo) page._</small>

# Test Cases for COCOMO

````python
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

 
 

 
````
