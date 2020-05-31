#!/usr/bin/python3
# import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def ex1():
  # Data for plotting
  t = np.arange(0.0, 2.0, 0.01)
  s = 1 + np.sin(2 * np.pi * t)
  fig, ax = plt.subplots()
  ax.plot(t, s)
  ax.set(xlabel='time (s)', ylabel='voltage (mV)',
       title='About as simple as it gets, folks')
  ax.grid()

  filename = "ex1.png"
  print('Saving matplotlib graphic', filename)
  fig.savefig(filename)
  plt.show() # show() works in Ubuntu 18.04 but it seems not to work in Ubuntu 20.04

def process():
  ex1()

if __name__ == '__main__':
  process()
