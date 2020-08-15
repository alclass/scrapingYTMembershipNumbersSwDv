#!/usr/bin/env python3
"""

Script's Usage:
==============
  #<scriptname> [--name=<partialname>]
obs:
  1 => obs1
"""
import datetime
import logging
import os
import requests
import fs.db.sqlalchdb.sqlalchemy_conn as con
import models.sa_models.ytchannelsubscribers_samodels as sam
from models.gen_models.YtVideosPageMod import YtVideosPage
import config

_, logfilename = os.path.split(__file__)
logfilename = str(datetime.date.today()) + '_' + logfilename[:-3] + '.log'
logfilepath = os.path.join(config.get_logfolder_abspath(), logfilename)
logging.basicConfig(filename=logfilepath, filemode='w', format='%(name)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def download_n_save_to_folder(videopage, entry_abspath):
  log_msg = 'Downloading ' + videopage.videospageurl
  print(log_msg)
  logger.info(log_msg)
  res = requests.get(videopage.videospageurl, allow_redirects=True)
  if res.status_code != 200:
    error_msg = 'Page [%s] returned a not 200 status response' % videopage.videospageurl
    print(error_msg)
    logger.error(error_msg)
    return
    # instead of raising an exception, log message to a file
    # raise IOError(error_msg)
  log_msg = 'Saving ' + entry_abspath
  print(log_msg)
  logger.info(log_msg)
  fp = open(entry_abspath, 'w')
  fp.write(res.text)
  fp.close()


class ChannelsVideoPageDownloader:

  def __init__(self, ytchannel):
    self.ytchannel = ytchannel
    self.videopage = YtVideosPage(ytchannel.ytchannelid, ytchannel.nname)

  def download_n_save_to_folder(self, check_dld_on_date=False):
    if check_dld_on_date:
      if not self.ytchannel.downloadable_on_date:
        return False
    download_n_save_to_folder(self.videopage, self.videopage.datedpage_filepath)


def find_by_likename(likename):
  session = con.Session()
  ytchannel = session.query(sam.YTChannelSA).\
      filter(sam.YTChannelSA.nname.like("%" + likename + "%")).first()
  # print(ytchannel)
  session.close()
  return ytchannel


def find_by_likenames(likenames):
  ytchannels = []
  for likename in likenames:
    ytchannel = find_by_likename(likename)
    ytchannels.append(ytchannel)
  return ytchannels


def fetch_ytchannels_n_process():
  likenames = [
    'portal do josé',
    'villa',
    'henry bug',
  ]
  # likenames.append('plantão brasil')
  for ytchannel in find_by_likenames(likenames):
    print('fetch_ytchannelsprocess', ytchannel)
    downloader = ChannelsVideoPageDownloader(ytchannel)
    downloader.download_n_save_to_folder()


def process():
  fetch_ytchannels_n_process()


if __name__ == '__main__':
  process()
