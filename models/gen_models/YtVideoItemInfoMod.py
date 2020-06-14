#!/usr/bin/python3
import fs.datefunctions.datefs as dtfs
import models.procdb.sqlalch_fetches as fetch

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
    ytchannel = fetch.FetchYtVideosPageByItsIdInDB(ytchannelid)
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
    self.infodate = dtfs.return_refdate_as_datetimedate_or_today(info_refdate)

  @property
  def publishdate(self):
    if self._publishdate is None:
      self.set_publishdate_with_time_ago()
    return self._publishdate

  def set_publishdate_with_time_ago(self):
    '''
    Notice:
      1) this method is to help find the publishdate;
      2) in the future, if publishdate can be more exactly determine, field published_time_ago may be dropped

    Example of content for published_time_ago: 3 semanas atrás

    :param infodate:
    :return:
    '''
    self._publishdate = None
    if self.published_time_ago is None:
      return
    pp = self.published_time_ago.split(' ')
    try:
      n = int(pp[0])
    except ValueError:
      return
    try:
      word = pp[1]; d = None
      if word.find('hora') > -1 or word.find('hour') > -1:
        if n < 15:
          n = 0
        else:
          n = 1
        d = dtfs.calc_past_date_from_refdate_back_n_days(self.infodate, n)
      elif word.find('dia') > -1:
        d = dtfs.calc_past_date_from_refdate_back_n_days(self.infodate, n)
      elif word.find('day') > -1:
        d = dtfs.calc_past_date_from_refdate_back_n_days(self.infodate, n)
      elif word.find('semana') > -1:
        d = dtfs.calc_past_date_from_refdate_back_n_days(self.infodate, n * 7)
      elif word.find('week') > -1:
        d = dtfs.calc_past_date_from_refdate_back_n_days(self.infodate, n * 7)
      elif word.find('mês') > -1:
        d = dtfs.calc_past_date_from_refdate_back_n_days(self.infodate, n * 7)
      elif word.find('mes') > -1:
        d = dtfs.calc_past_date_from_refdate_back_n_days(self.infodate, n * 7)
      elif word.find('month') > -1:
        d = dtfs.calc_past_date_from_refdate_back_n_days(self.infodate, n * 7)
      elif word.find('ano') > -1:
        d = dtfs.calc_past_date_from_refdate_back_n_days(self.infodate, n * 7)
      elif word.find('year') > -1:
        d = dtfs.calc_past_date_from_refdate_back_n_days(self.infodate, n * 7)
      self._publishdate = d
      return
    except ValueError:
      pass
    return

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
