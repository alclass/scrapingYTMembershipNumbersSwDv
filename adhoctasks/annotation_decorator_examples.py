#!/usr/bin/python3
import re

def mutate(method):
  def newmethod(*args, **kwargs):
    print('Executing method')
    method(**kwargs) # *args,
    print('Finished Executing method')
  return newmethod

@mutate
def myfunction(a=None, b=None, **kwargs):
  print ('hello', a, b, kwargs)

myfunction(1, 2, bla='blah')

