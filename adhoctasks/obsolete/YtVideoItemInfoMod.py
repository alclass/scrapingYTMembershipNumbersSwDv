#!/usr/bin/python3
import datetime
import logging
import os
import fs.datefunctions.datefs as dtfs
import models.procdb.sqlalch_fetches as fetch
import config

_, logfilename = os.path.split(__file__)
logfilename = str(datetime.date.today()) + '_' + logfilename[:-3] + '.log'
logfilepath = os.path.join(config.get_logfolder_abspath(), logfilename)
logging.basicConfig(filename=logfilepath, filemode='w', format='%(name)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class YtVideoItemInfo:
  """
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
  """

  def __init__(self, ytvideoid, title, ytchannelid, info_refdate=None):
    self._duration_in_sec = None
    self._views = None
    self._publishdate = None
    if len(ytvideoid) != 11:
      error_msg = 'YtVideoItemInfo() init received ytvideoid (%s) not having 11 chars' % ytvideoid
      raise ValueError(error_msg)
    self.ytvideoid = ytvideoid
    self.title = title
    self.published_time_ago = None
    self.infodate = None
    self.set_info_refdate_or_today(info_refdate)
    if ytchannelid is None:
      error_msg = 'YtVideoItemInfo() init ytchannelid (%s) received as None' % ytchannelid
      raise ValueError(error_msg)
    start_letter = ytchannelid[0]
    if start_letter not in ['c', 'u']:
      error_msg = "YtVideoItemInfo() init start_letter not in ['c', 'u'] for ytchannelid (%s)" % ytchannelid
      raise ValueError(error_msg)
    ytchannel = fetch.fetch_ytvideospage_by_its_dbid(ytchannelid)
    if ytchannel is None:
      error_msg = 'YtVideoItemInfo() init could not fetch ytchannel (videospage) by its ytchannelid (%s)' % ytchannelid
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
          v = v.replace('.', '')  # obs. v is supposed to never be a decimal (, and . are acceptable here)
        elif v.find(',') > -1:
          v = v.replace(',', '')  # obs. v is supposed to never be a decimal (, and . are acceptable here)
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

  def set_publishdate_with_time_ago(self):
    pass

  def asdict(self):
    outdict = {
      'ytvideoid': self.ytvideoid,
      'title': self.title,
      'duration_hms': self.duration_hms,
      'duration_in_sec': str(self.duration_in_sec),
      'views': str(self.views),
      'publishdate': self.publishdate,
      'published_time_ago': self.published_time_ago,
      'infodate': self.infodate,
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
''' % (self.asdict())
    return outstr


def test1():
  ytchannelid = 'ueduardoamoreira'
  ytvideoid = ''
  o = YtVideoItemInfo(ytvideoid, title='title', ytchannelid=ytchannelid)
  o.views = '123,123'
  o.set_duration_in_sec_as_hms('2:10:15')
  print(o)
  print('duration_hms', o.duration_hms)


def process():
  test1()


if __name__ == '__main__':
  process()
