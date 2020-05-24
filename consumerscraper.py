#!/usr/bin/python3
from scrapeHtmlsMod import HTMLScraper

def scrapePages():
  scraper = HTMLScraper()
  scraper.print_scraping_results()
  print('Saving JSON')
  scraper.saveJson()

def process():
  scrapePages()

if __name__ == '__main__':
  process()
