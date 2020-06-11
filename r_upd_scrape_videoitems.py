#!/usr/bin/python3
'''
Usage:
      $this_script [-h] [--ini=<yyyy-mm-dd>] [--fim=<yyyy-mm-dd>]
  Parameters:
    - h                       shows this help message
    --ini=<yyyy-mm-dd date>   sets initial-date
    --fim=<yyyy-mm-dd date>   sets final-date
    --all                     runs for all dates in database

Optional parameters:
  1) if no parameters are used, both ini and fim would be set to today's date and processing will occur only for today's date;
  2) if either one of --ini or --fim is not used, the processing will occur for given day only, not a range of days.

Erroneous date conditions:
  1) if ini is greater than fim, an exception (error) will be raised;
  2) if fim is greater than today, an exception (error) will also be raised;
  3) if a date not in format yyyy-mm-dd is entered, an exception (error) will be raised;
  4) if a wrong date is entered, an exception (error) will also be raised.

Examples:
      1) $this_script --ini=2020-05-23 --fim=2020-05-30
  will consider the 8-day range with 2020-05-23 and fim=2020-05-30, ie 2020-05-23, 2020-05-24, 2020-05-25 and so on up to 2020-05-30;
      2) $this_script --fim=2020-05-25
  will consider the 1-day 2020-05-25 for processing;
      3) $this_script --ini=2020-05-30 --fim=2020-05-23
  will trigger an error as explained above
      4) $this_script
  will consider today (1-day) for processing;
      5) $this_script --all
  will process for all dates inside the database;
'''

import sys
import fs.datefunctions.datefs as dtfs
import fs.filefunctions.autofinders as autofind
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

def find_ini_fim_full_date_range_in_data_n_confim():
  dateini, datefim = autofind.find_dateini_n_dateend_thru_yyyymmdd_level2_folders()
  screen_msg = 'Please confirm dateini as %s and datefim as %s:' %(dateini, datefim)
  print(screen_msg)
  ans = input('Confirm (Y/n) [default is Y, type in N/n to unconfirm] ? ')
  if ans in ['N', 'n']:
    sys.exit()
  return dateini, datefim

def get_args():
  outdict = {'dateini':None, 'datefim':None}
  # sys.argv.append('--all')
  for arg in sys.argv:
    if arg.startswith('-h'):
      show_help_n_exit()
    elif arg.startswith('--all'):
      dtini, dtfim = find_ini_fim_full_date_range_in_data_n_confim()
      outdict = {'dateini': dtini, 'datefim': dtfim}
      return outdict
    elif arg.startswith('--ini='):
      try:
        pos = len('--ini=')
        param = arg[pos:]
        paramdate = dtfs.get_refdate_from_strdate_or_None(param)
        outdict['dateini'] = paramdate
      except IndexError:
        pass
    elif arg.startswith('--fim='):
      try:
        pos = len('--fim=')
        param = arg[pos:]
        paramdate = dtfs.get_refdate_from_strdate_or_None(param)
        outdict['datefim'] = paramdate
      except IndexError:
        pass
  return outdict

def get_dateini_n_datefim_from_cli_params():
  datesdict = get_args()
  dateini = datesdict['dateini']
  datefim = datesdict['datefim']
  return dateini, datefim

def process():
  dateini, datefim = get_dateini_n_datefim_from_cli_params()
  traversor = DatedHtmlsTraversor(dateini, datefim)
  print(traversor)
  for i, videospageinfo in enumerate(traversor.traverse()):
    seq = i + 1
    print (seq, videospageinfo)
    scrap_videospageinfo_html(videospageinfo)

if __name__ == '__main__':
  process()
