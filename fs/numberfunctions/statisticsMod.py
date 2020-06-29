#!/usr/bin/python3

def calc_min_max_dif_del(alist):
  if alist is None or len(alist) == 0:
    return (0, 0, 0, 0)
  mini = 1000 ** 4;   maxi = -1
  first = alist[0];   last = alist[-1]
  delt = last - first
  for n in alist:
    if n > maxi:
      maxi = n
    if n < mini:
      mini = n
  diff = maxi - mini
  return (mini, maxi, diff, delt)

def adhoc_test():
  alist = [7, 15, 9, -1]
  result = calc_min_max_dif_del(alist)
  print (result)

def process():
  adhoc_test()

if __name__ == '__main__':
  process()