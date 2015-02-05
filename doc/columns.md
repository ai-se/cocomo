<small>_This file is part of cocomo. To know more, view the source code [columns.py](../src/columns.py) or read our [home](https://github.com/ai-se/cocomo) page._</small>

# Handling Columns of Data

Rows contain columns of data.
Column headers are either `N` nums or `S`
symbols objects. Columns are divided
into independent and dependent variables.

+ Dependent symbolic columns are called `klasses`;
+ Dependent numeric columns can be optionally
  tagged with a boolean `like` (and we want more
   things with
  `like==True`).

````python
from column import *
import zipfile,re

@setting
def COLS(**d): return o( 
    skip="?",
    num="$",
    sep  = ',',
    bad = r'(["\' \t\r\n]|#.*)',
    source = lambda f: unzip('../data/data.zip',f)
  ).update(**d)

def columns(**d):
  return o(indep=[], dep=[],rows=[]
           ).update(**d)

def unzip(zipped, want):
  with zipfile.ZipFile(zipped,'r') as archive:
    for got in archive.namelist():
      if got == want: 
        for line in archive.open(got,'r'):
          yield line
        break

def rows(file, source=open):
  w = the.COLS
  def reader(name):
    return float if w.num in name else identity
  def lines(): 
    n,kept = 0,""
    for line in source(file):
      now   = re.sub(w.bad,"",line)
      kept += now
      if kept:
        if not now[-1] == w.sep:
          yield n, kept.split(w.sep)
          n += 1
          kept = "" 
  todo = None
  for n,line in lines():
    if n == 0:
      todo = [(n,reader(header))
              for n,header in enumerate(line)
              if not w.skip in header]
    else:
      yield n, [ read(line[col]) 
                 for col,read in todo ]

````
