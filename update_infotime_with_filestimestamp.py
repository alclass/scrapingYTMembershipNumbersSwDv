#!/usr/bin/env python3
"""
"""
import datetime
import logging
import os
import fs.datefunctions.datefs as dtfs
import fs.db.sqlalchdb.sqlalchemy_conn as con
import fs.filefunctions.autofinders as autof
import fs.filefunctions.pathfunctions as pathfs
import models.sa_models.ytchannelsubscribers_samodels as sam
import config

_, logfilename = os.path.split(__file__)
logfilename = str(datetime.date.today()) + '_' + logfilename[:-3] + '.log'
logfilepath = os.path.join(config.get_logfolder_abspath(), logfilename)
logging.basicConfig(filename=logfilepath, filemode='w', format='%(name)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

gcounter = 0


def ajust_vitems(refdate, ytchannelid, ptime, session):
  global gcounter
  counter = 0
  vitems = session.query(sam.YTVideoItemInfoSA). \
    filter(sam.YTVideoItemInfoSA.infodate == refdate). \
    filter(sam.YTVideoItemInfoSA.ytchannelid == ytchannelid). \
    all()
  for vitem in vitems:
    if vitem.infotime != ptime:
      counter += 1
      print(gcounter, counter, vitem.infodate, vitem.title, '|', vitem.ytchannel.nname, ' | updating time', ptime)
      vitem.infotime = ptime
  return counter


def ajust_vviews(refdate, ytchannelid, ptime, session):
  global gcounter
  counter_vviews = 0
  vviews = session.query(sam.YTVideoViewsSA). \
    filter(sam.YTVideoViewsSA.infodate == refdate). \
    filter(sam.YTVideoItemInfoSA.ytvideoid == sam.YTVideoViewsSA.ytvideoid). \
    filter(sam.YTVideoItemInfoSA.ytchannelid == ytchannelid). \
    all()
  for vview in vviews:
    if vview.infotime != ptime:
      counter_vviews += 1
      gcounter += 1
      print(gcounter, counter_vviews, vview.infodate, '|', vview.views, vview.ytvideo.title, '|', vview.ytvideo.ytchannel.nname, ' | updating time', ptime)
      vview.infotime = ptime

  return counter_vviews


def look_up_modifiedtime_of_htmlvideopagefiles(refdate, session):
  """
  """
  global gcounter
  htmlfilepaths = autof.find_htmlfilepaths_from_date(refdate)
  counter_vitems = 0
  counter_vviews = 0
  for filepath in htmlfilepaths:
    _, filename = os.path.split(filepath)
    t = os.stat(filepath)
    modified_dt = datetime.datetime.fromtimestamp(t.st_mtime)
    ptime = dtfs.extract_time_from_datetime(modified_dt)
    mdate = dtfs.convert_datetime_to_date(modified_dt)
    if mdate != refdate:
      line = 'cdate (%s) != refdate (%s)' % (mdate, refdate)
      print(line)
      continue
    ytchannelid = pathfs.extract_ytchid_from_filename(filename)
    # counter_vitems = ajust_vitems(refdate, ytchannelid, ptime, session)
    counter_vviews = ajust_vviews(refdate, ytchannelid, ptime, session)

  if counter_vviews > 0 or counter_vitems > 0:
    print('Committing counter with', counter_vviews, counter_vitems, gcounter)
    session.commit()


def look_up_dates_data():
  session = con.Session()
  inidate, findate = autof.find_dateini_n_datefin_thru_yyyymmdd_level3_folders()
  for refdate in dtfs.generate_daterange_with_dateini_n_datefin(inidate, findate):
    look_up_modifiedtime_of_htmlvideopagefiles(refdate, session)
  session.close()
  print(inidate, findate)


def look_up_empty_infotime_values():
  """

  :return:
  """
  bool_deleted = False
  session = con.Session()
  vviews = session.query(sam.YTVideoViewsSA). \
    filter(sam.YTVideoViewsSA.infotime == None). \
    all()
  n_of_vviews_with_null_infotime = len(vviews)
  print('count vviews', )
  for i, vview in enumerate(vviews):
    print(i+1, vview.infodate, vview.views, vview.ytvideo.title, vview.ytvideo.ytchannel.nname)
    bool_deleted = True
    session.delete(vview)
  if bool_deleted:
    print('records vviews deleted =',  n_of_vviews_with_null_infotime)
    session.commit()

  vitems = session.query(sam.YTVideoItemInfoSA). \
    filter(sam.YTVideoItemInfoSA.infotime == None). \
    all()
  n_of_vitems_with_null_infotime = len(vitems)
  print('count vitews', len(vitems))
  for i, vitem in enumerate(vitems):
    print(i+1, vitem.infodate, vitem.ytchannel.nname)
    # bool_deleted = True
    # session.delete(vitem)
  if bool_deleted:
    total = n_of_vitems_with_null_infotime + n_of_vviews_with_null_infotime
    print('records deleted =', total, 'vviews', n_of_vviews_with_null_infotime, 'vitems', n_of_vitems_with_null_infotime)

  session.close()


def look_up_empty_publishdatetime_values():
  bool_deleted = False
  session = con.Session()
  vitems = session.query(sam.YTVideoItemInfoSA). \
    filter(sam.YTVideoItemInfoSA.publishdatetime == None). \
    all()
  n_of_deleted_rows = 0
  print('count YTVideoItemInfoSA.publishdatetime', )
  for i, vitem in enumerate(vitems):
    print(i+1, 'nviews', vitem.vviewlist.count(), vitem.publishdatetime, vitem.published_time_ago, vitem.infodate, vitem.title, vitem.ytchannel.nname)
    bool_deleted = True
    for e in vitem.vviewlist:
      n_of_deleted_rows += 1
      session.delete(e)
    n_of_deleted_rows += 1
    session.delete(vitem)
  if bool_deleted:
    print('Committing n_of_deleted_rows', n_of_deleted_rows)
    session.commit()
  session.close()


def process():
  # look_up_dates_data()
  # look_up_empty_infotime_values()
  look_up_empty_publishdatetime_values()


if __name__ == '__main__':
  process()
