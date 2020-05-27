#!/usr/bin/python3
import datetime
import scrapeHtmlsMod as scrap
from db.insert_update_subscribers import SubscriberInsertor

def insert_day(ytchid, refdate, n_subscribers):
  insertor = SubscriberInsertor(ytchid, refdate, n_subscribers)
  print ('dbmodified', insertor.boolean_dbmodified)

def insert():
  refdate = datetime.date.today()
  # refdate = refdate - datetime.timedelta(days=4)
  scraper = scrap.HTMLScraper(refdate)
  for i, id_n_qty_tuple in enumerate(scraper.id_n_qty_tuplelist):
    ytchid, n_subscribers = id_n_qty_tuple
    print (i+1, 'insert_day:', ytchid, refdate, n_subscribers)
    insert_day(ytchid, refdate, n_subscribers)

def process():
  insert()

if __name__ == '__main__':
  process()
