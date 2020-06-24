#!/usr/bin/python3

def return_cross_missing_elements_from_l1_l2(list1, list2):
  missing_corresp_1 = list(filter(lambda elem : not elem in list2, list1))
  missing_corresp_2 = list(filter(lambda elem : not elem in list1, list2))
  return missing_corresp_1, missing_corresp_2

def adhoc_test():
  l1 = [1, 2, 23, 67, 99]
  l2 = [1, 23, 68, 99]
  m1, m2 = return_cross_missing_elements_from_l1_l2(l1, l2)
  print ('l1', l1)
  print ('l2', l2)
  print ('m1', m1)
  print ('m2', m2)

def process():
  adhoc_test()

if __name__ == '__main__':
  process()