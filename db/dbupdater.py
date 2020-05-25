#!/usr/bin/python3
import datetime
from scrapeHtmlsMod import HTMLScraper

class DBWriter:

  def __init__(self, refdate):
    self.scraper = HTMLScraper(refdate)
    self.updatedb()

  def updatedb(self):
    for ytvideopageobj in self.scraper.reader.ytvideopageobj_list:
      pass

def scrapePages():
  refdate = datetime.date(2020, 5, 23)
  scraper = HTMLScraper(refdate)
  scraper.print_scraping_results()
  print('Saving JSON')
  scraper.saveJson()

def process():
  scrapePages()

if __name__ == '__main__':
  process()
