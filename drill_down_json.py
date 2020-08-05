#!/usr/bin/env python3
"""
  docstring
"""
import datetime
import json
import logging
import os
from models.gen_models.YtVideosPageMod import YtVideosPage
from models.gen_models.YtVideoItemMod import VideoItem
from models.sa_models.ytchannelsubscribers_samodels import YTChannelSA
from models.sa_models.ytchannelsubscribers_samodels import get_all_ytchannelids
import fs.textfunctions.scraper_helpers as scraphlp
from fs.db.sqlalchdb.sqlalchemy_conn import Session
import config

_, logfilename = os.path.split(__file__)
logfilename = str(datetime.date.today()) + '_' + logfilename[:-3] + '.log'
logfilepath = os.path.join(config.get_logfolder_abspath(), logfilename)
logging.basicConfig(filename=logfilepath, filemode='w', format='%(name)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class VideoItemsPageScraper:

  def __init__(self, ytchannelid, videopagedatetime):
    self.ytchannelid = ytchannelid
    self._nname = None
    self.videopagedatetime = videopagedatetime
    self.ytvideoid = None
    self.title = None
    self.calendarDateStr = None
    self.n_views = None
    self.durationStr = None

  def introspect_json_to_find_items(self, json_as_dict):
    self.ytvideoid, self.title, self.calendarDateStr, self.n_views, self.durationStr = \
      scraphlp.videoitems_drill_down(json_as_dict)

  def dbsave_videoitem(self):
    if self.ytvideoid is None:
      return False
    if self.n_views is None:
      return False
    vitem = VideoItem(
      self.ytvideoid, self.title, self.calendarDateStr, self.n_views, self.durationStr,
      self.videopagedatetime,
      self.ytchannelid
    )
    # print(vitem)
    return vitem.write_item_to_db_item_n_views()

  @property
  def nname(self):
    if self._nname is not None:
      return self._nname
    session = Session()
    ytchannel = session.query(YTChannelSA).filter(YTChannelSA.ytchannelid == self.ytchannelid).first()
    if ytchannel:
      self._nname = ytchannel.nname
    session.close()
    if self._nname is None:
      return 'w/inf'
    return self._nname

  def as_dict(self):
    odict = {
      'ytchannelid': self.ytchannelid,
      'nname': self.nname,
      'ytvideoid': self.ytvideoid,
      'title': self.title,
      'durationStr': self.durationStr,
      'n_views': self.n_views,
    }
    return odict

  def __str__(self):
    outstr = '''
  ytchannelid : %(ytchannelid)s
  nname       : %(nname)s 
  ytvideoid   : %(ytvideoid)s   
  title       : %(title)s  
  durationStr : %(durationStr)s 
  n_views     : %(n_views)s 
    ''' % self.as_dict()
    return outstr


beginningStr = '{"gridVideoRenderer":{'
endStr = '}]}}}]}}'


def extract_videoitems_from_videopage(ytchannelid, refdate):
  ytvideopage = YtVideosPage(ytchannelid, None, refdate)
  if ytvideopage.datedpage_filepath is None:
    # print('Filepath is None for', ytchannelid, ':: returning...')
    return
  if not ytvideopage.datedpage_exists:
    # print('Filepath does not exist for', ytchannelid, ':: returning...')
    return
  timestamp = ytvideopage.filesdatetime.st_atime
  videopagedatetime = datetime.datetime.fromtimestamp(timestamp)
  log_msg = '%s %s %s' % (str(ytvideopage.filesdatetime.st_atime), str(videopagedatetime), ytchannelid)
  print(log_msg)
  logger.info(log_msg)

  text = ytvideopage.get_html_text()
  # 1st) get the subscribers number
  # ytvideopage.videopagedatetime = videopagedatetime
  extract_subscribers_from_htmltext(text, ytvideopage)
  # 2nd) get the video items
  extract_vitems_from_htmltext(text, ytvideopage)


def extract_subscribers_from_htmltext(text, ytvideopage):
  subscribers_number = scraphlp.extract_subscriber_number(text)
  if subscribers_number is None:
    return False
  return ytvideopage.dbsave_subscribers_number(subscribers_number)


def extract_vitems_from_htmltext(text, ytvideopage):
  begpos = text.find(beginningStr)
  counter = 0
  # there are about 29 videos per page, the while below intends to loop thru them all
  while begpos > -1:
    text = text[begpos:]
    endpos = text.find(endStr)
    if endpos > -1:
      jsondictchunk = text[: endpos + len(endStr)]
      counter += 1
      try:
        json_as_dict = json.loads(jsondictchunk)
        viscraper = VideoItemsPageScraper(ytvideopage.ytchannelid, ytvideopage.videopagedatetime)
        viscraper.introspect_json_to_find_items(json_as_dict)
        bool_written = viscraper.dbsave_videoitem()  # videopagefilesdatetime already in object
        if bool_written:
          situation_written_or_not = ' * WRITTEN *'
        else:
          situation_written_or_not = ' *** not WRITTEN ***'
        log_msg = '%s %d %s' % (situation_written_or_not, counter, str(viscraper))
        print(log_msg)
        logger.info(log_msg)
      except json.decoder.JSONDecodeError:
        print('=' * 50)
        # TO-DO log it to a file, so that we'll be able to find a flawd videopage file
        log_msg = '=> Failed for %s %s' % (ytvideopage.ytchannelid, ytvideopage.filename)
        print(log_msg)
        logger.info(log_msg)
        continue
    text = text[endpos:]
    begpos = text.find(beginningStr)


def run_thru_channels():
  today = datetime.date.today()
  ini_fim_daterange = [today]  # dtfs.get_range_date(yesterday, today):
  for ytchannelid in get_all_ytchannelids():
    for refdate in ini_fim_daterange:
      print('Rolling', ytchannelid, 'for date', refdate)
      print('-'*50)
      extract_videoitems_from_videopage(ytchannelid, refdate)


def process():
  run_thru_channels()


if __name__ == '__main__':
  process()
