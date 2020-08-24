#!/usr/bin/env python3
"""
  docstring
"""
import datetime
import os
import fs.db.dbfetchers.centralfetchersmod as fetcher
import fs.textfunctions.scraper_helpers as scrap
import fs.datefunctions.datefs as dtfs
import fs.filefunctions.autofinders as autof
import fs.textfunctions.regexp_helpers as regexp
import fs.db.sqlalchdb.sqlalchemy_conn as con
import models.sa_models.ytchannelsubscribers_samodels as sam


def list_channels_scrapedates():
  sess = con.Session()
  likenname = '%plantão br%'
  ytchannel = fetcher.fetch_ytchannel_with_likenname(likenname, sess)
  print('list_channels_scrapedates ytchannel', ytchannel)
  if ytchannel is None:
    return
  c = 0
  for subs in ytchannel.daily_subscribers:
    c += 1
    if c > 3:
      break
    print('\t', subs.infodate, subs.subscribers)
  sess.close()


def scrape_n_return_number_of_subscribers_from_channels_pagetext(text):
  chunk = text if len(text) <= 80 else text[:80]
  print(chunk)
  scraperesult = scrap.extract_subscriber_number(text)
  print('scraperesult', scraperesult)
  return scraperesult

def scrape_channel_from_its_datedfile_n_return_number_of_subscribers(ytchannel, pdate):
  text = ytchannel.get_text_from_conventioned_datedvideopage_file(pdate)
  if text is None:
    return
  return scrape_n_return_number_of_subscribers_from_channels_pagetext(text)

def scrape_channel_from_its_datedfile():
  """
    Deactivated
  :return:
  """
  likenname = '%plantão br%'
  ytchannel = fetcher.fetch_ytchannel_with_likenname(likenname)
  print('ytchannel', ytchannel)
  if ytchannel is None:
    return
  return scrape_channel_from_its_datedfile_n_return_number_of_subscribers(ytchannel)

gcount = 0
g_nsubs_is_none = 0


def transport_osdatetime_to_null_infotime_values_in_subscribers():
  global g_nsubs_is_none, gcount
  session = con.Session()
  subs = session.query(sam.YTDailySubscribersSA).\
    filter(sam.YTDailySubscribersSA.infotime == None).\
    order_by(sam.YTDailySubscribersSA.infodate).\
    all()
  for i, sub in enumerate(subs):
    sname = sub.ytchannel.sname
    filename = autof.form_datedpage_filename_with_triple(sub.infodate, sname, sub.ytchannelid)
    filepath = autof.form_datedpage_filepath_with_triple(sub.infodate, sname, sub.ytchannelid)
    print(sname, sub, 'infotime', sub.infotime)
    osstat_nt = os.stat(filepath)
    mtime = osstat_nt.st_mtime
    dt = datetime.datetime.fromtimestamp(mtime)
    print(i+1, dt, filepath)
    pdate = dtfs.convert_datetime_to_date(dt)
    ptime = dtfs.extract_time_from_datetime(dt)
    if sub.infodate != pdate:
      g_nsubs_is_none += 1
      line = '============= sub.infodate %s != pdate %s =============' % (sub.infodate, pdate)
      print(line)
      continue
    gcount += 1
    sub.infotime = ptime

  print('g_nsubs_is_none', g_nsubs_is_none)
  print('gcount', gcount)
  session.commit()
  session.close()


def update_subscribers(ytchannel, refdate, n_of_subs, dt, session):
  global gcount
  pdate = dtfs.convert_datetime_to_date(dt)
  if pdate != refdate:
    error_msg = 'Error: pdate (%s) != refdate (%s) dt=(%s)' %(pdate, refdate, dt)
    raise ValueError(error_msg)
  ptime = dtfs.extract_time_from_datetime(dt)
  subs = session.query(sam.YTDailySubscribersSA).\
    filter(sam.YTDailySubscribersSA.ytchannelid == ytchannel.ytchannelid).\
    filter(sam.YTDailySubscribersSA.infodate == pdate).\
    first()
  if subs:
    was_changed = False
    if subs.subscribers != n_of_subs:
      subs.subscribers = n_of_subs
      was_changed = True
    if subs.infotime != n_of_subs:
      subs.infotime = ptime
      was_changed = True
    if was_changed:
      gcount += 1
      print(gcount, 'db-update', subs)
      session.commit()
    return
  subs = sam.YTDailySubscribersSA()
  subs.ytchannelid = ytchannel.ytchannelid
  subs.subscribers = n_of_subs
  subs.infodate = pdate
  subs.infotime = ptime
  gcount += 1
  print(gcount, 'db-insert', subs)
  session.commit()


def update_subscribers_scrape_for_date(refdate):
  global g_nsubs_is_none
  sess = con.Session()
  ytchannelids_n_cdatetimes = autof.find_ytchannelid_n_videopagefilemodifiedtimestamp_tuplelist_for_date(refdate)
  for ytchannelid_n_cdatetime in ytchannelids_n_cdatetimes:
    ytchannelid, cdatetime = ytchannelid_n_cdatetime
    ytchannel = fetcher.fetch_ytchannel_with_ytchannelid(ytchannelid, sess)
    if ytchannel is None:
      continue
    dt = datetime.datetime.fromtimestamp(cdatetime)
    pdate = dtfs.convert_datetime_to_date(dt)
    n_of_subs = scrape_channel_from_its_datedfile_n_return_number_of_subscribers(ytchannel, pdate)
    if n_of_subs is None:
      g_nsubs_is_none += 1
      print(g_nsubs_is_none, 'n_of_subs is None')
      continue
    print(ytchannel.nname, refdate, n_of_subs, dt)
    update_subscribers(ytchannel, refdate, n_of_subs, dt, sess)
  sess.close()


def update_subscribers_scrape_for_daterange(inidate, findate):
  print('inidate, findate', inidate, findate)
  for refdate in dtfs.generate_daterange_with_dateini_n_datefin(inidate, findate):
    update_subscribers_scrape_for_date(refdate)


def update_subscribers_scrape_for_month(refdate=None):
  inidate, findate = dtfs.get_daterange_for_month(refdate)
  update_subscribers_scrape_for_daterange(inidate, findate)


def update_subscribers_scrape_for_months():
  months = [5, 6, 7, 8]
  for mo in months:
    pdate = '2020-%s-01' % str(mo).zfill(2)
    update_subscribers_scrape_for_month(pdate)


def list_last_subscribers_for_ytchannel(ytchannel, session):
  n_subs = ytchannel.daily_subscribers.count()
  last_ones = n_subs if n_subs < 10 else 9
  print(ytchannel.nname)
  for i in range(last_ones):
    subs = ytchannel.daily_subscribers[i]
    print(i+1, subs.infodate, subs.infotime, subs.subscribers)


def verify_videopagefiles_w_no_corresponding_dbsubs():
  """
  About 800 pages were committed with the function below, ie they received missing subscriber numbers.
    There is one 'subscriber_number' per day per channel and some were missing within the last 3 months.
  However, after about 800 recups, there are still 22 missing, with scraperesult returning None;
    ie, there are yet 22 pages that maybe demand the old scraping routine for fetching n_of_subscribers;
    it's probably possible to treat them, picking up the 'museum' code.
  This above is a TO-DO (segunda, 24 de agosto de 2020 01:43), ie try to rescrape these with the old routine.
  :return:
  """
  count = 0
  n_commits = 0
  session = con.Session()
  for abspath in autof.generate_all_ytvideopages_abspath_asc_date():
    strdate, sname, ytchannelid = regexp.find_triple_date_sname_n_ytchid_in_filepath(abspath)
    subs = session.query(sam.YTDailySubscribersSA).\
      filter(sam.YTDailySubscribersSA.ytchannelid == ytchannelid).\
      filter(sam.YTDailySubscribersSA.infodate == strdate).\
      first()
    if subs:
      continue
    count += 1
    print(count, strdate, sname, ytchannelid, abspath)
    t_osstat = os.stat(abspath)
    timestamp = t_osstat.st_mtime
    dt = datetime.datetime.fromtimestamp(timestamp)
    filedate = dtfs.convert_datetime_to_date(dt)
    pdate = dtfs.get_refdate_from_strdate_or_none(strdate)
    if pdate != filedate:
      print('strdate', strdate, 'pdate', pdate, 'filedate', filedate, 'dt', dt)
      continue
    filetime = dtfs.extract_time_from_datetime(dt)
    text = open(abspath, encoding='utf8').read()
    n_of_subscribers = scrape_n_return_number_of_subscribers_from_channels_pagetext(text)
    # print('n_of_subscribers', n_of_subscribers)
    if n_of_subscribers is None:
      continue
    subs = sam.YTDailySubscribersSA()
    subs.ytchannelid = ytchannelid
    subs.infodate = pdate
    subs.infotime = filetime
    subs.subscribers = n_of_subscribers
    session.add(subs)
    n_commits += 1
    print('n_commits', n_commits, 'committing', subs)
    session.commit()
  print('n_commits', n_commits, 'missing', count)
  session.close()



def list_last_subs():
  session = con.Session()
  ytchannels = fetcher.fetch_all_active_ytchannels_in_db(session)
  for ytchannel in ytchannels:
    list_last_subscribers_for_ytchannel(ytchannel, session)
  session.close()


def adhoc_test():
  refdate = '2020-05-22'
  ytchid_n_videopagecdatetime_tlist = autof.find_ytchannelid_n_videopagefilemodifiedtimestamp_tuplelist_for_date(refdate)
  for tupl in ytchid_n_videopagecdatetime_tlist:
    _, timestamp = tupl
    dt = datetime.datetime.fromtimestamp(timestamp)
    print(refdate, dt)


def adhoc_test2():

  filepath = '/media/friend/SAMSUNG/Ytvideos BRA Politics/z Other ytchannels/000_scrape_ytdata/' \
             '2020/2020-08/2020-08-14/2020-08-14 Leonel Rad [cUCEttBYmNrvFl9m9f7Uz4XJg] .html'
  filepath = '/media/friend/SAMSUNG/Ytvideos BRA Politics/z Other ytchannels/000_scrape_ytdata/' \
             '2020/2020-08/2020-08-14/2020-08-14 Jessé Souz [aJesséSouzaSociologo].html'
  strdate, sname, ytchannelid = regexp.find_triple_date_sname_n_ytchid_in_filepath(filepath)
  print(strdate, sname, ytchannelid)


def process():
  """
  scrape_channel_from_its_datedfile()
  list_channels_scrapedates()

  :return:
  """
  # update_subscribers_scrape_for_month()
  # list_last_subs()
  # update_subscribers_scrape_for_months()
  # print('g_nsubs_is_none', g_nsubs_is_none)
  # transport_osdatetime_to_null_infotime_values_in_subscribers()
  verify_videopagefiles_w_no_corresponding_dbsubs()
  # adhoc_test2()


if __name__ == '__main__':
  process()
