from __future__ import division,print_function
import sys 
sys.dont_write_bytecode = True


from optimo import *

@go
def _sampleN():
  for x in sampleN(samples=10):
    print(x)
