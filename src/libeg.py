from __future__ import division,print_function
import sys
sys.dont_write_bytecode =True


"""

# Examples of Running Lib.py

"""

from lib import *

def lst0(): return list('0123456789')

@go
def _lists():
  "Random stuff"
  rseed(1)
  l1= shuffle(lst0())
  print(l1)
  print(shuffle(lst0()))
  rseed(1)
  l2=shuffle(lst0())
  print('Resetting seed replicated old results:',
        l1==l2)

@go
def _pairs():
  "Walk thru pairs of the list."
  for one,two in pairs(lst0()):
    print('pairs of one',one,' and two',two)

@go
def _runs():
  rseed(1)
  lst = sorted([round(r()/0.01) for _ in xrange(25)])
  print(lst)
  got =[(n,x) for n,x in runs(lst)]
  want = [(1, 0.0), (3, 3.0), (1, 9.0), (1, 13.0), 
          (1, 22.0), (1, 23.0), (1, 26.0), (1, 38.0), 
          (1, 43.0), (2, 45.0), (1, 50.0), (1, 54.0), 
          (1, 65.0), (1, 72.0), (2, 76.0), (1, 79.0), 
          (1, 84.0), (1, 85.0), (1, 90.0), (1, 94.0),
          (1, 95.0)]
  print("\ngot= ",got)
  print('\ngood runs?',want==got)

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
def _g():
  lst = [r() for _ in xrange(20)]
  print(lst)
  print(g(lst))

@go
def _printm():
  "Pretty print columns of text."
  text="""Lorem ipsum dolor sit amet, consectetur adipiscing
  elit, sed do eiusmod tempor incididunt ut labore et
  dolore magna aliqua. Ut enim ad minim veniam, quis
  nostrud exercitation ullamco laboris nisi ut aliquip
  ex ea commodo consequat. Duis aute irure dolor in
  reprehenderit in voluptate velit esse cillum dolore
  eu fugiat nulla pariatur. Excepteur sint occaecat
  cupidatat non proident, sunt in culpa qui officia 
  deserunt mollit anim id est laborum."""
  m= [line.split() for line in text.splitlines()]
  printm(m)

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
        ["apples"]    + [4,5,7,4,7,6,5,8,6,5]*10,
        ["bananas"]   + [7,9,8,9,7,9,7,7,7,9,8,7,7,9,9]*10,
        ["oranges"]   + [1,5,5,3,3,2,4,6,3,2]*10,
        ["pears"]     + [7,7,8,6,8,7,6,7,8,6,8,7,6,7.1,8,6]*10,
        ["plantains"] + [7,9,8,9,7,9,7,7,7,9,8,7,7,9,9]*10])
        