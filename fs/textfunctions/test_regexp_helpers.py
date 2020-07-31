#!/usr/bin/env python3
"""
  docstring
"""
import fs.textfunctions.regexp_helpers as regexp
import unittest


class TestCase(unittest.TestCase):

  def test_1(self):
    """
    t = 'blah {"text": "437.6 k subscribers"} blah'
    expected = '437.6' # 437600
    returned = regexp.find_nsubscribers_via_either_re_or_find(t)
    self.assertEqual(expected, returned)

    :return:
    """

    t = 'bla [-cUlddjf_aj-dlf-_]'
    expected = '-cUlddjf_aj-dlf-_'
    returned = regexp.find_ytchannelid_within_brackets_in_filename(t)
    self.assertEqual(expected, returned)

    expected = 'cCVZ-XVXDadafd3_40RTR4'
    namewithoutext = '2020-06-01 Sname Blah ['+expected+']'
    returned = regexp.find_ytchannelid_within_brackets_in_filename(namewithoutext)
    self.assertEqual(expected, returned)

    strdate = '2020-06-01'
    sname = 'Sname Blah'
    ytchid = 'cOUDFAF9adafd340KIUIdadJK'
    triple_expected = (strdate, sname, ytchid)
    namewithoutext = '2020-06-01 Sname Blah [cOUDFAF9adafd340KIUIdadJK]'
    triple_returned = regexp.find_triple_date_sname_n_ytchid_in_filename(namewithoutext)
    self.assertEqual(triple_expected, triple_returned)


def process():
  pass


if __name__ == '__main__':
  process()
