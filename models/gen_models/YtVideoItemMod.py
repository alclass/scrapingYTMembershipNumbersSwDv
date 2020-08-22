#!/usr/bin/python3
"""
  The module contains class VideoItem.
  This class may later be integrated with its corresponding
    SqlAlchemy models (YTVideoItemInfoSA & YTVideoViewsSA)
    (*) The way this integration should happen is not yet known, but it could be either:
      1) via inheritance or
      2) via mix-in or
      3) helper functions called from the SqlAlchemy model.

  Its function is to receive and organize the scraped data and then insert it or update it to db.

  Its main client is class drill_down_json.VideoItemsPageScraper

"""
import datetime
import logging
import os
import fs.datefunctions.datefs as dtfs
from fs.db.sqlalchdb.sqlalchemy_conn import Session
from models.sa_models.ytchannelsubscribers_samodels import YTVideoViewsSA
from models.sa_models.ytchannelsubscribers_samodels import YTVideoItemInfoSA
import config

_, logfilename = os.path.split(__file__)
logfilename = str(datetime.date.today()) + '_' + logfilename[:-3] + '.log'
logfilepath = os.path.join(config.get_logfolder_abspath(), logfilename)
logging.basicConfig(filename=logfilepath, filemode='w', format='%(name)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class VideoItem:

  def __init__(self, ytvideoid, title, calendar_strdate, n_views, duration_str, videopagedatetime, ytchannelid):
    self.ytvideoid = ytvideoid
    self.title = title
    self.calendar_strdate = calendar_strdate
    self.durationStr = duration_str
    self.videopagedatetime = videopagedatetime
    self.ytchannelid = ytchannelid
    self.n_views = None
    self._duration_in_sec = None
    self._infodate = None
    self._infotime = 12
    self._videopagedate = None
    self._videopagetime = None
    self._publishdatetime = None  # to be calculated against first access to self.publishdate
    self.set_n_treat_derived_fields(n_views)

  def set_n_treat_derived_fields(self, n_views):
    self.treat_views(n_views)
    self.treat_calendar_strdate()
    self.set_infodate_n_infotime()
    self.set_publishdatetime()
    self.set_videopagedate_n_time()

  def treat_views(self, n_views):
    try:
      word = n_views.strip().split(' ')[0]
      word = word.replace('.', '').replace(',', '')
      self.n_views = int(word)
    except ValueError:
      self.n_views = 0
    log_msg = 'self.n_views = %d' % self.n_views
    logger.info(log_msg)

  def set_infodate_n_infotime(self):
    self._infodate, self._infotime = dtfs.split_date_n_time_from_datetime(self.videopagedatetime)
    # defaults
    if self._infodate is None:
      self._infodate = dtfs.get_refdate_from_strdate_or_today()
    if self._infotime is None:
      self._infotime = datetime.datetime.now()
    log_msg = 'set_infodate_n_infotime() infodate = %s | infotime = %s | videopagedatetime = %s' \
              % (str(self._infodate), str(self._infotime), str(self.videopagedatetime))
    logger.info(log_msg)

  @property
  def infodate(self):
    if self._infodate is None or self._infotime is None:
      self.set_infodate_n_infotime()
    return self._infodate

  @property
  def infotime(self):
    if self._infotime is None:
      self.set_infodate_n_infotime()
    return self._infotime

  def set_duration_in_sec(self):
    self._duration_in_sec = dtfs.transform_hms_into_duration_in_sec(self.durationStr)
    log_msg = 'self._duration_in_sec = %d' % self._duration_in_sec
    logger.info(log_msg)

  @property
  def duration_in_sec(self):
    if self._duration_in_sec is None:
      self.set_duration_in_sec()
    return self._duration_in_sec

  def treat_calendar_strdate(self):
    self.calendar_strdate = dtfs.ajust_calendardatestr_to_start_with_a_number(self.calendar_strdate)

  def set_publishdatetime(self):
    try:
      timestamp = self.videopagedatetime.st_atime
      pdatetime = datetime.datetime.fromtimestamp(timestamp)
    except AttributeError:
      return
    self._publishdatetime = dtfs.calculate_origdtime_from_targetdtime_n_calendarstr(
      pdatetime,
      self.calendar_strdate
    )
    log_msg = 'self._publishdatetime = %s' % (str(self._publishdatetime))
    logger.info(log_msg)

  @property
  def publishdatetime(self):
    if self._publishdatetime is None:
      self.set_publishdatetime()
    return self._publishdatetime

  def publishdate(self):
    return dtfs.convert_datetime_to_date(self.publishdatetime)

  def set_videopagedate_n_time(self):
    self._videopagedate, self._videopagetime = dtfs.split_date_n_time_from_datetime(self.videopagedatetime)

  @property
  def videopagedate(self):
    if self._videopagedate is None:
      self.set_videopagedate_n_time()
    return self._videopagedate

  @property
  def videopagetime(self):
    if self._videopagetime is None:
      self.set_videopagedate_n_time()
    return self._videopagetime

  def write_item_to_db_item_n_views(self):
    bool_items = self.write_item_to_db()
    situation_written_or_not = 'Written item'
    if not bool_items:
      situation_written_or_not = ' *NOT* ' + situation_written_or_not
    log_msg = situation_written_or_not + ' ' + self.ytvideoid + ' ' + self.title + str(self.infodate)
    print(log_msg)
    logger.info(log_msg)

    bool_views = self.write_views_to_db()
    situation_written_or_not = 'Written item'
    if not bool_views:
      situation_written_or_not = ' *NOT* ' + situation_written_or_not
    log_msg = situation_written_or_not + str(self.n_views) + str(self.infodate)
    print(log_msg)
    logger.info(log_msg)
    return bool_items and bool_views

  def insert_videoitem(self, session):
    videoitem = YTVideoItemInfoSA()
    session.add(videoitem)
    videoitem.ytvideoid = self.ytvideoid
    videoitem.title = self.title
    videoitem.duration_in_sec = self.duration_in_sec
    videoitem.publishdatetime = self.publishdatetime
    videoitem.published_time_ago = self.calendar_strdate
    videoitem.infodate = self.infodate
    videoitem.infotime = self.infotime
    videoitem.ytchannelid = self.ytchannelid
    session.commit()
    log_msg = 'session closed in insert_videoitem() ' + str(videoitem)
    print(log_msg)
    logger.info(log_msg)
    session.close()
    return True

  def update_videoitem(self, dbvideoitem, session):
    """

    The quadruple fields: publishdatetime, infodate, infotime and published_time_ago
      should all be treated together as in a group, so, because of that,
      attempts to update them here were removed (code fragment below in this docstring).

    (A separate script will be written to check consistency of the four crossing info with
      mtime of its html video page file, if it still exists.)

    if self.publishdatetime is not None and dbvideoitem.publishdatetime is None:
      dbvideoitem.publishdatetime = self.publishdatetime
      log_msg = 'Updating published_time_ago from ['\
                + dbvideoitem.published_time_ago + '] to [' + self.calendar_strdate + ']'
      dbvideoitem.published_time_ago = self.calendar_strdate
      print(log_msg)
      logger.info(log_msg)
      was_changed = True
    # logically, if infodate has already been recorded, pdate will be later and no update will occurr,
    # but it'll help when databases are out of sync and infodate must be the lesser of the two
    if dbvideoitem.infodate is None or dbvideoitem.infodate > self.infodate:
      log_msg = 'Updating infodate from ['\
                + str(dbvideoitem.infodate) + '] to [' + str(self.infodate) + ']'
      dbvideoitem.infodate = self.infodate
      print(log_msg)
      logger.info(log_msg)
      was_changed = True
    if dbvideoitem.infotime is None or self.infotime != dbvideoitem.infotime:
      log_msg = 'Updating infotime from [' \
                + str(dbvideoitem.infotime) + '] to [' + str(self.infotime) + ']'
      dbvideoitem.infotime = self.infotime
      print(log_msg)
      logger.info(log_msg)
      was_changed = True

    :param dbvideoitem:
    :param session:
    :return:
    """
    was_changed = False
    if dbvideoitem.title != self.title:
      if self.title is not None:
        if self.title != 'No Title':
          if len(self.title) > 0:
            log_msg = 'Updating title from [' + dbvideoitem.title + '] to [' + self.title + ']'
            dbvideoitem.title = self.title
            print(log_msg)
            logger.info(log_msg)
            was_changed = True
    if self.duration_in_sec is not None and self.duration_in_sec > 0:
      if dbvideoitem.duration_in_sec != self.duration_in_sec:
        log_msg = 'Updating duration_in_sec from ['\
                  + str(dbvideoitem.duration_in_sec) + '] to [' + str(self.duration_in_sec) + ']'
        dbvideoitem.duration_in_sec = self.duration_in_sec
        print(log_msg)
        logger.info(log_msg)
        was_changed = True
    if was_changed:
      session.commit()
    log_msg = 'session closed in update_videoitem() commit=' + str(was_changed) + ' ' + str(dbvideoitem)
    print(log_msg)
    logger.info(log_msg)
    session.close()
    return was_changed

  def write_item_to_db(self):
    session = Session()
    videoitem = session.\
        query(YTVideoItemInfoSA).\
        filter(YTVideoItemInfoSA.ytvideoid == self.ytvideoid).\
        first()
    if videoitem:
      bool_ret = self.update_videoitem(videoitem, session)
    else:
      bool_ret = self.insert_videoitem(session)
    session.close()
    return bool_ret

  def write_views_to_db(self):
    session = Session()
    vviews = session.query(YTVideoViewsSA). \
        filter(YTVideoViewsSA.ytvideoid == self.ytvideoid). \
        filter(YTVideoViewsSA.infodate == self.infodate). \
        first()
    if vviews:
      was_changed = False
      if self.n_views is not None and vviews.views != self.n_views:
        was_changed = True
        vviews.views = self.n_views
      if self.infotime is not None and vviews.infotime != self.infotime:
        was_changed = True
        vviews.infotime = self.infotime
      if was_changed:
        session.commit()
      session.close()
      if was_changed:
        return True
      else:
        return False
    vviews = YTVideoViewsSA()
    vviews.ytvideoid = self.ytvideoid
    vviews.views = self.n_views
    vviews.infodate = self.infodate
    vviews.infotime = self.infotime
    session.add(vviews)
    session.commit()
    log_msg = 'Committed videoviews object ' + str(vviews)
    print(log_msg)
    logger.info(log_msg)
    session.close()
    return True

  def as_dict(self):
    outdict = {
      'ytvideoid': self.ytvideoid,
      'title': self.title,
      'infodate': self.infodate,
      'calendar_datestr': self.calendar_strdate,
      'publishdatetime': self.publishdatetime,
      'n_views': str(self.n_views),
      'durationStr': self.durationStr,
    }
    return outdict

  def __str__(self):
    outstr = '''<VideoItem
    ytvideoid = %(ytvideoid)s
    title = %(title)s
    infodate = %(infodate)s
    calendar_datestr = %(calendarDateStr)s
    publishedDatetime = %(publishdatetime)s
    n_views = %(n_views)s
    durationStr = %(durationStr)s
>''' % self.as_dict()
    return outstr


def process():
  pass


if __name__ == '__main__':
  process()
