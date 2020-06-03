#!/usr/bin/python3
import bs4, datetime, os
import fs.datefunctions.datefs as dtfs
import fs.textfunctions.scraper_helpers as scraphlp
from models.YtVideosPageMod import YtVideosPage

class YtVideoItemInfo:

  def __init__(self, ytvideoid, title, published_time_ago=None, info_refdate=None):
    self._duration_in_sec = None
    self._views = None
    self.ytvideoid = ytvideoid
    self.title = title
    self.published_time_ago = published_time_ago
    self.info_refdate = None; self.set_info_refdate_or_today(info_refdate)

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
    if self._duration_in_sec is None:
      return 'w/inf'
    if self._duration_in_sec < 60:
      return '0:%d' %self._duration_in_sec
    elif self._duration_in_sec < 60 * 60:
      minutes = self._duration_in_sec // 60
      seconds = self._duration_in_sec % 60
      return '%d:%d' %(minutes, seconds)
    else:
      hours = self._duration_in_sec // (60 * 60)
      remaining = self._duration_in_sec - hours * (60 * 60)
      minutes = remaining // 60
      seconds = remaining % 60
      return '%d:%d:%d' % (hours, minutes, seconds)
    return 'w/inf'

  def set_duration_in_sec_as_hms(self, duration_hms):
    if duration_hms is None:
      return
    pp = duration_hms.split(':')
    if len(pp) == 2:
      minutes = int(pp[0])
      seconds = int(pp[1])
      self._duration_in_sec = minutes * 60 + seconds
      return
    elif len(pp) == 3:
      hours = int(pp[0])
      minutes = int(pp[1])
      seconds = int(pp[2])
      self._duration_in_sec = hours * 60 * 60 + minutes * 60 + seconds
      return
    error_msg = 'Error: in set_duration_in_sec() => duration_in_sec =' + str(duration_hms)
    raise ValueError(error_msg)

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
    self.info_refdate = dtfs.return_refdate_as_datetimedate_or_today(info_refdate)

  def asdict(self):
    outdict = {
    'ytvideoid' : self.ytvideoid,
    'title'     : self.title,
    'duration_hms'   : self.duration_hms,
    'duration_in_sec': self.duration_in_sec,
    'views'     : self.views,
    'published_time_ago' : self.published_time_ago,
    'info_refdate'       : self.info_refdate,
    }
    return outdict

  def __str__(self):
    outstr = '''[YtVideo Info]
  ytvideoid = %(ytvideoid)s
  title = %(title)s
  duration_hms (in sec) = %(duration_hms)s (%(duration_in_sec)d)
  views = %(views)d
  published_time_ago = %(published_time_ago)s 
  info_refdate = %(info_refdate)s
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
