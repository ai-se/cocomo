<small>_This file is part of cocomo. To know more, view the source code [badSmellseg.py](../src/badSmellseg.py) or read our [home](https://github.com/ai-se/cocomo) page._</small>

# Test Cases for COCOMO

````python
from cocomo import *
from badSmells import *
 
 
PROJECTS  = [flight,ground,osp,osp2,anything]
TREATMENTS= [doNothing, improvePersonnel, improveToolsTechniquesPlatform,
             improvePrecendentnessDevelopmentFlexibility, 
             increaseArchitecturalAnalysisRiskResolution, relaxSchedule,
             improveProcessMaturity, reduceFunctionality]
             
 
@go
def _badSmells():
  sample(projects=PROJECTS,score=badSmell)
   
@go
def _whatStinks():
    rseed(1)
    for project in PROJECTS:
        print("\n",project.__name__)
        stinks = whatStinks(project)
        worst = stinks[0][0]
        for stink,what in stinks:
            if stink > worst*0.5:
                print('stink = ',stink,' when ',what)

@go
def _badSmellsTreated():
  rseed(1)
  for project in [anything]:
    print("\n#### ",project.__name__," ","#"*50,"\n")
    sample(projects=[project],treatments=TREATMENTS,score=badSmell)

 
 

 
````
