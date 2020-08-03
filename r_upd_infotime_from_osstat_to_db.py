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


def compare_source_n_target_videopage():
  autof.find_dateini_n_datefin_thru_yyyymmdd_level3_folders()


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


def remake_ptab(field_names):
  ptab = PrettyTable()
  ptab.field_names = field_names
  return ptab


def show_dates_n_times_of_videoitems_table():
  session = con.Session()
  videitems = session.query(sam.YTVideoItemInfoSA).all()
  seq = 0
  field_names = [
    'seq', 'ytvideoid', 'nname', 'titletrunc',
    'infodate', 'infodayhour',
    'publishdatetime', 'calendarStr', 'created_at'
  ]
  ptab = remake_ptab(field_names)
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
    if seq % 40 == 0:
      print(ptab)
      ptab = remake_ptab(field_names)
    # if seq > 400:
    # break
  print(ptab)


def compare_prefixdate_with_osstatdate():
  seq = 0
  count_equal_dates = 0
  field_names = [
    'seq', 'strdate', 'dayhour', 'dt'
  ]
  ptab = remake_ptab(field_names)
  ptab_out = remake_ptab(field_names)
  for ytvideopage_abspath in autof.generate_all_ytvideopages_abspath_asc_date():
    seq += 1
    _, ytvideopage = os.path.split(ytvideopage_abspath)
    strdate = ytvideopage[:10]
    filesdatetimest = os.stat(ytvideopage_abspath)[7]
    dt = datetime.datetime.fromtimestamp(filesdatetimest)
    dayhour = dt.hour
    filesdate = dtfs.convert_datetime_to_date(dt)
    if strdate == str(filesdate):
      count_equal_dates += 1
      if dt.minute > 30 and dt.hour < 23:
        dayhour += 1
      ptab.add_row([seq, strdate, dayhour, dt])
    else:
      ptab_out.add_row([seq, strdate, '', dt])
  print(ptab)
  print(ptab_out)
  print('seq', seq,  'count_equal_dates', count_equal_dates)


DEFAULT_SHORTIVIDEO_DURATION_CAP_IN_MIN = 20


def list_ytchannel_videos_less_than_nmin(ytchannelid=None, nmin=None):
  if ytchannelid is None:
    ytchannelid = 'ueduardoamoreira'
  if nmin is None:
    nmin = DEFAULT_SHORTIVIDEO_DURATION_CAP_IN_MIN
  if type(nmin) != int:
    try:
      nmin = int(nmin)
    except ValueError:
      nmin = DEFAULT_SHORTIVIDEO_DURATION_CAP_IN_MIN
  session = con.Session()
  nsec = nmin * 60
  ytchannel = session.query(sam.YTChannelSA).filter(sam.YTChannelSA.ytchannelid == ytchannelid).first()
  print(ytchannel)
  ytvideoids = []
  for i, vinfo in enumerate(ytchannel.vinfolist):
    if vinfo.duration_in_sec <= nsec:
      hms = dtfs.transform_duration_in_sec_into_hms(vinfo.duration_in_sec)
      print(i+1, hms, vinfo.title)
      ytvideoids.append(vinfo.ytvideoid)
  for ytvideoid in ytvideoids:
    print(ytvideoid)


def process():
  # update_infotime_for_all_ytvideopages()
  # show_dates_n_times_of_videoitems_table()
  # compare_prefixdate_with_osstatdate()
  list_ytchannel_videos_less_than_nmin()


if __name__ == '__main__':
  process()
