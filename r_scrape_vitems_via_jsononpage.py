#!/usr/bin/env python3
import datetime, json, calendar
from models.sa_models.ytchannelsubscribers_samodels import get_all_ytchannelids
import fs.datefunctions.datefs as dtfs
import drill_down_json as drill


import r_upd_scrape_videoitems as prev_scrap

def get_ini_fim_daterange():
  dateini, datefim = prev_scrap.get_dateini_n_datefim_from_cli_params()
  ini_fim_daterange = dtfs.make_daterange_with_dateini_n_datefim(dateini, datefim)
  return ini_fim_daterange

def run_all():
  ini_fim_daterange = get_ini_fim_daterange()
  for ytchannelid in get_all_ytchannelids():  # ytchannelids = finder.get_ytchannelids_on_datefolder(today)
    for refdate in ini_fim_daterange:  # dtfs.get_range_date(yesterday, today):
      print('Rolling', ytchannelid, 'for date', refdate)
      print('-' * 50)
      drill.extract_videoitems_from_videopage(ytchannelid, refdate)


def process():
  '''
  refdate = datetime.date.today()
  ytchannelid = 'ueduardoamoreira'
  ytchannelid = 'uhumbertocostapt'
  extract_videoitems_from_videopage(ytchannelid, refdate)

  :return:
  '''
  run_all()


if __name__ == '__main__':
  process()
