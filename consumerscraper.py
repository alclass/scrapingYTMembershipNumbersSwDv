#!/usr/bin/python3
import datetime
from scrapeHtmlsMod import HTMLScraper

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
