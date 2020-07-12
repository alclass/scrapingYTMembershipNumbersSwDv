#!/usr/bin/python3
import datetime, json, calendar
# from dateutil import relativedelta # calculate duration between two dates
from models.gen_models.YtVideosPageMod import YtVideosPage
from models.sa_models.ytchannelsubscribers_samodels import YTVideoViewsSA
from models.sa_models.ytchannelsubscribers_samodels import YTVideoItemInfoSA
from models.sa_models.ytchannelsubscribers_samodels import get_all_ytchannelids
from fs.db.sqlalchdb.sqlalchemy_conn import Session
import fs.datefunctions.datefs as dtfs

# import fs.filefunctions.autofinders as finder

beginningStr = '{"gridVideoRenderer":{'
endStr = '}]}}}]}}'


class VideoItem:

  def __init__(self, ytvideoid, title, calendarDateStr, n_views, durationStr, infodatetime, ytchannelid):
    self.ytvideoid = ytvideoid
    self.title = title
    self.calendarDateStr = calendarDateStr
    self.treat_calendarDateStr()
    self.n_views = None;
    self.treat_views(n_views)
    self.durationStr = durationStr
    self.infodatetime = infodatetime  # former ytvideofiledatetime
    self.ytchannelid = ytchannelid
    self.publishdatetime = None  # to be calculated
    self.calculate_publishdate()

  def treat_views(self, n_views):
    try:
      word = n_views.strip().split(' ')[0]
      word = word.replace('.', '').replace(',', '')
      self.n_views = int(word)
    except ValueError:
      self.n_views = 0

  @property
  def infodate(self):
    return dtfs.convert_datetime_to_date(self.infodatetime)

  def publishdate(self):
    return dtfs.convert_datetime_to_date(self.publishdatetime)

  @property
  def duration_in_sec(self):
    return dtfs.transform_hms_into_duration_in_sec(self.durationStr)

  def treat_calendarDateStr(self):
    self.calendarDateStr = dtfs.ajust_calendardatestr_to_start_with_a_number(self.calendarDateStr)

  def calculate_publishdate(self):
    self.publishdatetime = dtfs.calculate_origdtime_from_targetdtime_n_calendarstr(self.infodatetime,
                                                                                   self.calendarDateStr)

  def write_item_to_db_item_n_views(self):
    bool_res = self.write_item_to_db()
    if bool_res:
      print('Written item', self.ytvideoid, self.title)
    else:
      print(' *NOT* Written item', self.ytvideoid, self.title)

    bool_res = self.write_views_to_db()
    if bool_res:
      print('Written views', self.n_views, self.infodatetime)
    else:
      print(' *NOT* Written views', self.n_views, self.infodatetime)

  def write_item_to_db(self):
    session = Session()
    videoitem = session.query(YTVideoItemInfoSA).filter(YTVideoItemInfoSA.ytvideoid == self.ytvideoid).first()
    if videoitem:
      was_changed = False
      if videoitem.title != self.title:
        videoitem.title = self.title
        was_changed = True
      if self.publishdatetime is not None:
        if videoitem.publishdatetime is None or videoitem.publishdatetime > self.publishdatetime:
          videoitem.publishdatetime = self.publishdatetime
          videoitem.published_time_ago = self.calendarDateStr
          videoitem.infodatetime = self.infodatetime
          was_changed = True
      if self.duration_in_sec is not None:
        if videoitem.publishdatetime != self.publishdatetime:
          videoitem.publishdatetime = self.publishdatetime
          was_changed = True
      if was_changed:
        session.commit()
      session.close()
      return was_changed
    videoitem = YTVideoItemInfoSA()
    videoitem.ytvideoid = self.ytvideoid
    videoitem.title = self.title
    videoitem.duration_in_sec = self.duration_in_sec
    videoitem.publishdatetime = self.publishdatetime
    videoitem.published_time_ago = self.calendarDateStr
    videoitem.infodatetime = self.infodatetime
    videoitem.ytchannelid = self.ytchannelid
    session.add(videoitem)
    session.commit()
    session.close()
    return True

  def write_views_to_db(self):
    session = Session()
    vviews = session.query(YTVideoViewsSA). \
      filter(YTVideoViewsSA.ytvideoid == self.ytvideoid). \
      filter(YTVideoViewsSA.infodate == self.infodate). \
      first()
    if vviews:
      session.close()
      return False
    vviews = YTVideoViewsSA()
    vviews.ytvideoid = self.ytvideoid
    vviews.views = self.n_views
    vviews.infodate = dtfs.convert_datetime_to_date(self.infodatetime)
    session.add(vviews)
    session.commit()
    session.close()
    return True

  def as_dict(self):
    outdict = {
      'ytvideoid': self.ytvideoid,
      'title': self.title,
      'infodatetime': self.infodatetime,
      'calendarDateStr': self.calendarDateStr,
      'publishdatetime': self.publishdatetime,
      'n_views': str(self.n_views),
      'durationStr': self.durationStr,
    }
    return outdict

  def __str__(self):
    outstr = '''<VideoItem
    ytvideoid = %(ytvideoid)s
    title = %(title)s
    infodatetime = %(infodatetime)s
    calendarDateStr = %(calendarDateStr)s
    publishedDatetime = %(publishdatetime)s
    n_views = %(n_views)s
    durationStr = %(durationStr)s
>''' % self.as_dict()
    return outstr

def drill_down_dict(pdict, videopagefilesdatetime, ytchannelid):
  ytvideoid = pdict['gridVideoRenderer']['videoId']
  try:
    title = pdict['gridVideoRenderer']['title']['simpleText']
  except KeyError:
    title = 'No Title'
  try:
    calendarDateStr = pdict['gridVideoRenderer']['publishedTimeText']['simpleText']
  except KeyError:
    calendarDateStr = '1 minut'
  try:
    n_views = pdict['gridVideoRenderer']['viewCountText']['simpleText']
  except KeyError:
    n_views = '0 v'
  try:
    durationStr = pdict['gridVideoRenderer']['thumbnailOverlays'][0]['thumbnailOverlayTimeStatusRenderer']['text'][
      'simpleText']
  except KeyError:
    durationStr = '0:0'
  vitem = VideoItem(ytvideoid, title, calendarDateStr, n_views, durationStr, videopagefilesdatetime, ytchannelid)
  print(vitem)
  vitem.write_item_to_db_item_n_views()


def extract_videoitems_from_videopage(ytchannelid, refdate):
  ytvideopage = YtVideosPage(ytchannelid, None, refdate)
  if ytvideopage.datedpage_filepath is None:
    print('Filepath is None for', ytchannelid, ':: returning...')
    return
  if not ytvideopage.datedpage_exists:
    print('Filepath does not exist for', ytchannelid, ':: returning...')
    return
  timestamp = ytvideopage.filesdatetime.st_atime
  print(ytvideopage.filesdatetime.st_atime)
  videopagefilesdatetime = datetime.datetime.fromtimestamp(timestamp)
  print(videopagefilesdatetime)

  text = ytvideopage.get_html_text()
  begpos = text.find(beginningStr)
  counter = 0;
  chunk = '';
  lastchunk = ''
  while begpos > -1:
    text = text[begpos:]
    endpos = text.find(endStr)
    if endpos > -1:
      lastchunk = chunk = text[: endpos + len(endStr)]
      # strchunk = chunk
      # chunkline = chunk if len(chunk) < 55 else strchunk[:25] + '...' + strchunk[-25:]
      counter += 1
      try:
        pdict = json.loads(lastchunk)
        drill_down_dict(pdict, videopagefilesdatetime, ytchannelid)
      except json.decoder.JSONDecodeError:
        print('=' * 50)
        # TO-DO log it to a file, so that we'll be able to find a flawd videopage file
        print('=> Failed for', ytvideopage.ytchannelid, ytvideopage.filename)
        print('=' * 50)
        continue
    text = text[endpos:]
    begpos = text.find(beginningStr)

  # pdict = json.loads(lastchunk)
  # print(lastchunk)


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
      extract_videoitems_from_videopage(ytchannelid, refdate)


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
