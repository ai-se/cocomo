from __future__ import division,print_function
import sys 
sys.dont_write_bytecode = True

from counts import * 

@go
def _cliffsDelta():
  rseed(1)
  lst1=[r() for _ in xrange(1000)]
  print('big difference:',
        1==cliffsDelta(
          lst1,
          [r()**2 for _ in xrange(1000)]))
  print('small difference:',
        0==cliffsDelta(
          lst1,
          [r() for _ in xrange(1000)]))

@go
def _xtile():
  "Percentile print of numbers."
  def raisedTo(n):
    lst=[r()**n for _ in xrange(1000)]
    print(n,": ",xtile(lst,lo=0,hi=1,show="%3.2f"))
  raisedTo(0.5)
  raisedTo(1.0)
  raisedTo(2.0)

@go 
def _xtiles():
  xtiles([
        ["apples"]    + [4,5,7,4,7,6,5,8,6,5              ]*10,
        ["bananas"]   + [7,9,8,9,7,9,7,7,7,9,8,7,7,9,9    ]*10,
        ["oranges"]   + [1,5,5,3,3,2,4,6,3,2              ]*10,
        ["pears"]     + [7,7,8,6,8,7,6,7,8,6,8,7,6,7.1,8,6]*10,
        ["plantains"] + [7,9,8,9,7,9,7,7,7,9,8,7,7,9,9    ]*10])
        
