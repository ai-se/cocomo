# Risk Management with COCOMO

COCOMO is a project management tool that allows for testing management decisions
with respect to the stability of those decisions.

## Contents

+ [badSmells](doc/badSmells.md):  Test Cases for COCOMO
+ [badSmellseg](doc/badSmellseg.md):  Test Cases for COCOMO
+ [boot](doc/boot.md):  Boot code: stuff needed before anything else
+ [cocomo](doc/cocomo.md):  Sample from the COCOMO Model
+ [cocomoeg](doc/cocomoeg.md):  Test Cases for COCOMO
+ [data](doc/data.md):  Storing data in tables
+ [lib](doc/lib.md):  General stuff
+ [libeg](doc/libeg.md):  Examples of Running Lib.py

## Installation

COCOMO uses a standard UNIX environment (with git,
make, python 2.7+, bash, awk, etc).  To install and test, do
the following:

```
git clone https://github.com/ai-se/cocomo.git
cd cocomo
make tests
```
