#!/usr/bin/python3
''' => Help: this script scrapes a days' directory for subscriber amount for channels.
  The default is to scrape the current day date.
  An argument (--daysbefore=<n>) may be used to achieve a number of days in the past.
  Example:
    #thisscript --daysbefore=2
  will scrape the day before yesterday if its related folder exists.
'''
import datetime, sys
import scrapeHtmlsMod as scrap
from db.insert_update_subscribers import SubscriberInsertor

class SubscribersScraperToDB:

  def __init__(self, n_of_days_before=None):
    self.refdate = datetime.date.today()
    self.ajust_refdate_if_need(n_of_days_before)
    self.insert()

  def ajust_refdate_if_need(self, n_of_days_before):
    if n_of_days_before is None:
      return
    if n_of_days_before > 0:
      self.refdate = self.refdate - datetime.timedelta(days=n_of_days_before)

  def insert(self):
    scraper = scrap.HTMLScraper(self.refdate)
    for i, id_n_qty_tuple in enumerate(scraper.id_n_qty_tuplelist):
      ytchid, n_subscribers = id_n_qty_tuple
      print (i+1, 'insert_day:', ytchid, n_subscribers) # refdate is an instance var (self)
      self.insert_day(ytchid, n_subscribers)

  def insert_day(self, ytchid, n_subscribers):
    insertor = SubscriberInsertor(ytchid, self.refdate, n_subscribers)
    print('dbmodified', insertor.boolean_dbmodified)

def show_help_n_exit():
  print (__doc__)
  sys.exit()

def get_args():
  for arg in sys.argv:
    if arg.startswith('-h'):
      show_help_n_exit()
    elif arg.startswith('--daysbefore='):
      try:
        pos = len('--daysbefore=')
        rightside = arg[pos:]
        n_days_before = int(rightside)
      except ValueError:
        print ('Error: parameter --daysbefore=<n> expects an integer as input (entered %s).' %rightside)
        sys.exit()
      return n_days_before
  return None

def process():
  n_days_before = get_args()
  SubscribersScraperToDB(n_days_before)

if __name__ == '__main__':
  process()
