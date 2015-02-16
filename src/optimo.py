from __future__ import division,print_function
import sys 
sys.dont_write_bytecode = True

from cocomo import *
from badSmells import *
from ruler import *

def kloc(d): return d["kloc"]

def sampleN(samples=1000,
            projects=[anything],
            treatments=[doNothing],
            scores=[COCOMO2,badSmell,kloc]):
  names= sorted(Coc2tunings.keys())
  for project in projects:
    for treatment in treatments:
      out      = o(names=names,data=[])
      rx   = (project.__name__,treatment.__name__)
      for _ in xrange(samples):
        p = complete(project,treatment()) 
        tmp =  [p[n] for n in names] + [s(p) for s in scores]
        out.data += [tmp]
      yield rx,data(names = names + ["<effort","<smells",">kloc"],
                     data  = out.data)

