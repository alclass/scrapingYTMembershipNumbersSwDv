#!/usr/bin/env python3
"""
  This script makes available the following functionalities:
    1) prints out a list of dates and times from video items table;
    2) updates db correcting infodayhour for records that do not have this field-value;
"""
import datetime
import os
import fs.filefunctions.autofinders as autof
import fs.datefunctions.datefs as dtfs
import models.sa_models.ytchannelsubscribers_samodels as sam
import fs.db.sqlalchdb.sqlalchemy_conn as con
from prettytable import PrettyTable


def update_infotime_for_all_ytvideopages():
  seq = 0
  for ytvideopage_abspath in autof.generate_all_ytvideopages_abspath_asc_date():
    t = os.stat(ytvideopage_abspath)
    _, filename = os.path.split(ytvideopage_abspath)
    filesdatetime = t[7]
    pdatetime = datetime.datetime.fromtimestamp(filesdatetime)
    pdate = dtfs.convert_datetime_to_date(pdatetime)
    strdate = filename[:10]
    if strdate != str(pdate):
      continue
    seq += 1
    print(seq, filename, 'filesdatetime', filesdatetime, pdatetime)
    # return


def show_dates_n_times_of_videoitems_table():
  session = con.Session()
  videitems = session.query(sam.YTVideoItemInfoSA).all()
  ptab = PrettyTable()
  ptab.field_names = [
    'seq', 'ytvideoid', 'nname', 'infodate', 'infodayhour', 'publishdatetime', 'calendarStr', 'created_at'
  ]
  seq = 0
  for vitem in videitems:
    seq += 1
    ptab.add_row([
      seq,
      vitem.ytvideoid,
      vitem.ytchannel.nname,
      vitem.infodate,
      vitem.infodayhour,
      vitem.publishdatetime,
      vitem.published_time_ago,
      vitem.created_at,
    ])
    if seq > 200:
      break
  print(ptab)


def process():
  # update_infotime_for_all_ytvideopages()
  show_dates_n_times_of_videoitems_table()


if __name__ == '__main__':
  process()
