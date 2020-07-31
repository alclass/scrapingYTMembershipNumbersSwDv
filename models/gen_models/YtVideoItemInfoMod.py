#!/usr/bin/python3
import fs.datefunctions.datefs as dtfs
import models.procdb.sqlalch_fetches as fetch
from fs.db.sqlalchdb.sqlalchemy_conn import Session
from models.gen_models.YtVideosPageMod import YtVideosPage
from models.sa_models.ytchannelsubscribers_samodels import YTVideoViewsSA
from models.sa_models.ytchannelsubscribers_samodels import YTVideoItemInfoSA

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
    bool_items = self.write_item_to_db()
    if bool_items:
      print('Written item', self.ytvideoid, self.title)
    else:
      print(' *NOT* Written item', self.ytvideoid, self.title)

    bool_views = self.write_views_to_db()
    if bool_views:
      print('Written views', self.n_views, self.infodatetime)
    else:
      print(' *NOT* Written views', self.n_views, self.infodatetime)
    return bool_items and bool_views

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
      if self.duration_in_sec is not None or self.duration_in_sec == 0:
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
      'calendar_datestr': self.calendarDateStr,
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
    calendar_datestr = %(calendarDateStr)s
    publishedDatetime = %(publishdatetime)s
    n_views = %(n_views)s
    durationStr = %(durationStr)s
>''' % self.as_dict()
    return outstr


class YtVideoItemInfo:
  '''
  This is a helper class to unite the scraped video items page info to the SqlAlchemy db-model
    for inserting or updating.

  The main attributes are:
    duration_in_sec
    views
    publishdate
    published_time_ago
    info
    ytchannel

  Notice that views is recorded in a separate table due to its changing value through dates.
  '''

  def __init__(self, ytvideoid, title, ytchannelid, info_refdate=None):
    self._duration_in_sec = None
    self._views = None
    self._publishdate = None
    if len(ytvideoid) != 11:
      error_msg = 'YtVideoItemInfo() init received ytvideoid (%s) not having 11 chars' %ytvideoid
      raise ValueError(error_msg)
    self.ytvideoid = ytvideoid
    self.title = title
    self.published_time_ago = None
    self.infodate = None; self.set_info_refdate_or_today(info_refdate)
    if ytchannelid is None:
      error_msg = 'YtVideoItemInfo() init ytchannelid (%s) received as None' %ytchannelid
      raise ValueError(error_msg)
    start_letter = ytchannelid[0]
    if start_letter not in ['c', 'u']:
      error_msg = "YtVideoItemInfo() init start_letter not in ['c', 'u'] for ytchannelid (%s)" %ytchannelid
      raise ValueError(error_msg)
    ytchannel = fetch.fetch_ytvideospage_by_its_dbid(ytchannelid)
    if ytchannel is None:
      error_msg = 'YtVideoItemInfo() init could not fetch ytchannel (videospage) by its ytchannelid (%s)' %ytchannelid
      raise ValueError(error_msg)
    self.ytchannel = ytchannel

  @property
  def duration_in_sec(self):
    return self._duration_in_sec

  @duration_in_sec.setter
  def duration_in_sec(self, duration_in_sec):
    if type(duration_in_sec) == int:
      self._duration_in_sec = duration_in_sec
    return

  @property
  def duration_hms(self):
    return dtfs.transform_duration_in_sec_into_hms(self._duration_in_sec)

  def set_duration_in_sec_as_hms(self, duration_hms):
    self._duration_in_sec = dtfs.transform_hms_into_duration_in_sec(duration_hms)

  @property
  def views(self):
    if self._views is None:
      return 0
    try:
      return int(self._views)
    except ValueError:
      pass
    return 0

  @views.setter
  def views(self, v):
    if v is None:
      return
    try:
      if type(v) in [int, float]:
        self._views = int(v)
        return
      try:
        if v.find('.') > -1:
          v = v.replace('.','') # obs. v is supposed to never be a decimal (, and . are acceptable here)
        elif v.find(',') > -1:
          v = v.replace(',','') # obs. v is supposed to never be a decimal (, and . are acceptable here)
      except AttributeError:
        pass
      self._views = int(v)
    except ValueError:
      pass
    return

  def set_info_refdate_or_today(self, info_refdate=None):
    self.infodate = dtfs.return_refdate_as_datetimedate_or_today(info_refdate)

  @property
  def publishdate(self):
    if self._publishdate is None:
      self.set_publishdate_with_time_ago()
    return self._publishdate

  def asdict(self):
    outdict = {
    'ytvideoid' : self.ytvideoid,
    'title'     : self.title,
    'duration_hms'   : self.duration_hms,
    'duration_in_sec': str(self.duration_in_sec),
    'views'      : str(self.views),
    'publishdate': self.publishdate,
    'published_time_ago' : self.published_time_ago,
    'infodate'       : self.infodate,
    }
    return outdict

  def __str__(self):
    outstr = '''[YtVideo Info]
  ytvideoid = %(ytvideoid)s
  title = %(title)s
  duration_hms (in sec) = %(duration_hms)s (%(duration_in_sec)s)
  views       = %(views)s
  publishdate = %(publishdate)s 
  published_time_ago = %(published_time_ago)s 
  infodate = %(infodate)s
''' %(self.asdict())
    return outstr

def test1():
  o = YtVideoItemInfo('ytid', 'title bla')
  o.views = '123,123'
  o.set_duration_in_sec_as_hms('2:10:15')
  print (o)
  print ('duration_hms', o.duration_hms)

def process():
  test1()

if __name__ == '__main__':
  process()
