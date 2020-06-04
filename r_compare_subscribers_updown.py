#!/usr/bin/python3
import fs.db.SubscriberDaysMod as subsmod

def process():
  sd = subsmod.SubscriberDays()
  sd.print_days_n_subscribers_per_channel()

if __name__ == '__main__':
  process()
