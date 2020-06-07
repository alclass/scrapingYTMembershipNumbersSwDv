#!/usr/bin/python3
import sys
import fs.datefunctions.datefs as dtfs
from models.scrapers.YTVideoItemScraperMod import YTVideoItemScraper
from models.scrapers.DatedHtmlsTraversorMod import DatedHtmlsTraversor

def scrap_videospageinfo_html(videospageinfo):
  '''
    # ytchannelid = 'upgjr23'
    ytchannelid = 'ueduardoamoreira'
    # refdate = get_refdate_from_param_n_days_before_or_today()

  :param videospageinfo:
  :return:
  '''
  videoitemscraper = YTVideoItemScraper(videospageinfo)
  videoitemscraper.scrape_html_on_folder()
  videoitemscraper.save_to_db()

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

def get_refdate_from_param_n_days_before_or_today():
  n_days_before = get_args()
  refdate = dtfs.return_refdate_as_datetimedate_or_today()
  if n_days_before is not None:
    refdate = dtfs.calc_past_date_from_refdate_back_n_days(refdate, n_days_before)
  print ('param refdate', refdate)
  return refdate

def process():
  # refdate = get_refdate_from_param_n_days_before_or_today()
  dateini = '2020-05-25' # '2020-05-22'
  datefim = None # '2020-05-24' # None
  traversor = DatedHtmlsTraversor(dateini, datefim)
  print(traversor)
  for i, videospageinfo in enumerate(traversor.traverse()):
    seq = i + 1
    print (seq, videospageinfo)
    scrap_videospageinfo_html(videospageinfo)

if __name__ == '__main__':
  process()
