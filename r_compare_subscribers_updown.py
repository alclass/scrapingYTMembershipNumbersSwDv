#!/usr/bin/env python3
"""
  This simple script just prints out a tuple list of dates and subscribers per channel.
"""
import models.procdb.SubscriberDaysMod as subsmod

def process():
  sd = subsmod.SubscriberDays()
  sd.print_days_n_subscribers_per_channel(n_of_date_desc_rows=3)

if __name__ == '__main__':
  process()
