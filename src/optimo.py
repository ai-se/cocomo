from __future__ import division,print_function
import sys 
sys.dont_write_bytecode = True

from ruler import *
from cocomo import *
from badSmells import *

def kloc(d): return d["kloc"]

def sampleN(samples=1000,
            projects=[anything],
            treatments=[doNothing],
            scores=[COCOMO2,badSmell,kloc]):
  names= sorted(Coc2tunings.keys())
  for project in projects:
    out    = o(names=names,data=[])
    o.name = (project.__name__,treatment.__name__)
    for _ in xrange(samples):
       p = complete(project,treatment()) 
       out.data += [[p[n] for n in names]+
                    [s(p) for s in scores]]
    yield data(o)

