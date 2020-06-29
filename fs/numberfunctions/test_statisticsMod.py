#!/usr/bin/python3
import fs.numberfunctions.statisticsMod as statm
import unittest

class TestCase(unittest.TestCase):

  def test_1(self):
    '''
      returned = statm.calc_min_max_dif_del(alist)
      The returned value is (mini, maxi, diff, delt) where:
      - mini is the least value in row
      - maxi is the greatest value in row
      - diff is the amplitude value in row, ie, maxi - mini
      - delt is the different on right and left borders, ie, last - first
    Example:
      alist = [7, 15, 9, 2, 20, 11, 21, 26, 29]
      expected = (mini=2, maxi=29, diff=27(ie. 29-2), delt=22(ie. 29-7))

    :return:
    '''
    alist = None
    expected = (0, 0, 0, 0)
    returned = statm.calc_min_max_dif_del(alist)
    self.assertEqual(expected, returned)

    alist = [7, 15, 9, -1]
    expected = (-1, 15, 16, -8)
    returned = statm.calc_min_max_dif_del(alist)
    self.assertEqual(expected, returned)

    alist = [7, 15, 9, 2, 20, 11, 21, 26, 29]
    expected = (2, 29, 29-2, 29-7)
    returned = statm.calc_min_max_dif_del(alist)
    self.assertEqual(expected, returned)


def process():
  pass

if __name__ == '__main__':
  process()