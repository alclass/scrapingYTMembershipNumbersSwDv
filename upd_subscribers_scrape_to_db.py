#!/usr/bin/env python3
"""
  => Help: this script scrapes a days' directory for subscriber amount for channels.
  The default is to scrape the current day infodate.
  An argument (--daysbefore=<n>) may be used to achieve a number of days in the past.
  Example:
    #thisscript --daysbefore=2
  will scrape the day before yesterday if its related folder exists.
"""
import datetime
import sys
from models.scrapers import DateFolderScraperMod as scrapM
from models.procdb.SubscriberInsertorMod import SubscriberInsertor
from models.procdb.SubscriberInsertorMod import Session
import models.sa_models.ytchannelsubscribers_samodels as samodels


class SubscribersScraperToDB:

  def __init__(self, n_of_days_before=None):
    self.refdate = datetime.date.today()
    self.modified_processed = 0
    self.channel_with_no_n_subscribers = 0
    self.total_lookedup = 0
    self.ajust_refdate_if_need(n_of_days_before)
    self.insert()

  def ajust_refdate_if_need(self, n_of_days_before):
    if n_of_days_before is None:
      return
    if n_of_days_before > 0:
      self.refdate = self.refdate - datetime.timedelta(days=n_of_days_before)

  def insert(self):
    scraper = scrapM.DateFolderScraper(self.refdate)
    for i, id_n_qty_tuple in enumerate(scraper.id_n_qty_tuplelist):
      ytchid, n_subscribers = id_n_qty_tuple
      print(i+1, 'insert_day:', ytchid, n_subscribers)  # refdate is an instance var (self)
      self.insert_day(ytchid, n_subscribers)

  def insert_day(self, ytchid, n_subscribers):
    # TO-DO : log in file when a n_subscribers < 0 (or = -1) happens
    self.total_lookedup += 1
    if n_subscribers < 0:
      self.channel_with_no_n_subscribers += 1
      print(self.channel_with_no_n_subscribers, 'n_subscribers < 0 (or = -1) happened =>', ytchid, n_subscribers)
      return
    insertor = SubscriberInsertor(ytchid, self.refdate, n_subscribers)
    if insertor.boolean_dbmodified:
      self.modified_processed += 1
    print(self.modified_processed, 'dbmodified', insertor.boolean_dbmodified)

  def report(self):
    outstr = '''
  Report:
    modified_processed =  %d
    channel_with_no_n_subscribers = %d 
    total_lookedup = %d
    ''' % (self.modified_processed, self.channel_with_no_n_subscribers, self.total_lookedup)
    print(outstr)


def show_help_n_exit():
  print(__doc__)
  sys.exit()


def get_args():
  for arg in sys.argv:
    if arg.startswith('-h'):
      show_help_n_exit()
    elif arg.startswith('--daysbefore='):
      pos = len('--daysbefore=')
      rightside = arg[pos:]
      try:
          n_days_before = int(rightside)
      except ValueError:
        print('Error: parameter --daysbefore=<n> expects an integer as input (entered %s).' % rightside)
        sys.exit()
      return n_days_before
  return None


def process():
  n_days_before = get_args()
  subs_s2db_o = SubscribersScraperToDB(n_days_before)
  subs_s2db_o.report()


if __name__ == '__main__':
  process()
