#!/usr/bin/env python3
"""
  This simple script just prints out a tuple list of dates and subscribers per channel.
"""
from prettytable import PrettyTable
import models.procdb.SubscriberDaysMod as subsM


# subs_report_ntconstr = coll.namedtuple('SubsReport', 'seq nname d1 subs1 d2 subs2 d3 subs3 mini maxi diff delt')

def print_report_namedtuple_list(report_namedtuple_list):
  ptab = PrettyTable()
  ptab.field_names = ['seq', 'nname', 'd1', 'subs1', 'd2', 'subs2', 'd3', 'subs3', 'mini', 'maxi', 'diff', 'delt']
  for report_nt in report_namedtuple_list:
    row = list(report_nt)
    ptab.add_row(row)
  print(ptab)


def process():
  sd = subsM.SubscriberDays()
  report_namedtuple_list = sd.print_days_n_subscribers_per_channel(n_of_date_desc_rows=3)
  print_report_namedtuple_list(report_namedtuple_list)


if __name__ == '__main__':
  process()
