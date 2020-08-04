#!/usr/bin/env python3
"""
This script downloads YouTube video pages (*) that belong to channels
  in the database.

(*) The URL pattern for these pages are youtu.be/<channelsid>/videos and
    they are found via the [videos] tab from the YouTube channel's home page.

  This script is planned to download pages once a day
  as each html file is named per day and kept in a configured folder.

Obs:
  1) files may be deleted on days afterwards but should be kept on the
     day's download that so that a second dowload does not happen or,
     alternatively, deleted for a renewed download on that same day;
  2) attribute each_n_days, if used, will make some videopages to be download
     <each_n_days> after its last download;

When this script was first written (May 2020) it was possible to find scrapeable data
  in the DOM. About in July 2020, all downloaded videopages did not have
  info in the DOM anymore,
  but they were found in the JavaScript in the page. So after June/July 2020 this system
  was updated to scrape data directly from the JavaScript source text.

When previously scraping was against the DOM,
  library BeautifulSoup was used. When data moved
  to the JavaScript source, BeautifulSoup was changed for a home-solution that
  used string.find() to cut off pre-string and post-string,
  and load the middle string into
  a Json object that, in turn, was casts into a dict.
  The sought-for info hopefully was in the dict.

Script's Usage:
==============
  #<scriptname> [--allactive=<boolean>]
obs:
  --allactive  => downloads all active channels in db, if False,
    it downloads according to dld_each_days parameter in db;
  if --allactive is not given, the default will be used. (At the time of this writing, it's ', ie, True.)

DEPRECATED:
  1) The param arg --maxtries=<number> defined how many times
  a redownload roll may happen.  Its DEFAULT is 3.
  --maxtries  => maximum number of tries when download file does not have data-extractable;
  if --maxtries is not given, the default will be used. (At the time of this writing, it's 7.)

  [It's not used anymore because redownloads do not happen when a 200 OK status code was gotten.]
"""
import datetime
import logging
import os
import requests
import time
import sys
import models.gen_models.YtVideosPageMod as ytvidpagesMod
from models.scrapers.YTVideoItemBsoupIsEmptyMod import RunEmtpyFinderThuFolder
from models.procdb.SubscriberInsertorMod import Session
import models.sa_models.ytchannelsubscribers_samodels as samodels
import fs.datefunctions.datefs as dtfs
from fs.db.jsondb import readjson
import drill_down_json as drill
import config

_, logfilename = os.path.split(__file__)
logfilename = str(datetime.date.today()) + '_' + logfilename[:-3] + '.log'
logfilepath = os.path.join(config.get_logfolder_abspath(), logfilename)
logging.basicConfig(filename=logfilepath, filemode='w', format='%(name)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class DownloadYtVideoPages:

  def __init__(self, n_of_download_rolls=None, download_all_active_ones=True):
    self.download_all_active_ones = download_all_active_ones
    self.ytchannels = []
    self.n_exists = 0
    self.n_downloaded = 0
    self.n_fail_200 = 0
    self.total_channels = 0
    self.n_of_download_rolls = None
    self.set_n_of_download_rolls(n_of_download_rolls)
    self.from_db_to_ytchannel()

  def set_n_of_download_rolls(self, n_of_download_rolls):
    self.n_of_download_rolls = n_of_download_rolls
    if self.n_of_download_rolls is None or type(self.n_of_download_rolls) != int:
      self.n_of_download_rolls = 1

  def fallback_from_json_to_ytchannel(self):
    """
      Deactivated

    :return:
    """
    channelsdatareader = readjson.JsonYtChannel()
    for channeldict in channelsdatareader.loopthru():
      nname = channeldict['nname']
      ytchid = channeldict['ytchannelid']
      ytchannel = ytvidpagesMod.YtVideosPage(ytchid, nname)
      self.ytchannels.append(ytchannel)

  def from_db_to_ytchannel(self):
    """
      Deactivated
    :return:
    """
    session = Session()
    dbytchannels = session.query(samodels.YTChannelSA). \
        order_by(samodels.YTChannelSA.nname). \
        all()
    for ytchannel in dbytchannels:
      if not self.download_all_active_ones:
        if not ytchannel.is_downloadable_on_date():
          continue
      ytchannelpage = ytvidpagesMod.YtVideosPage(ytchannel.ytchannelid, ytchannel.nname)
      ytchannelpage.is_downloadable_on_date = True
      ytchannelpage.set_sname_by_nname()
      self.ytchannels.append(ytchannelpage)
    session.close()

  def download_ytvideopages(self):
    """

    :return:
    """
    self.total_channels = len(self.ytchannels)
    today = datetime.date.today()
    for i, ytchannel in enumerate(self.ytchannels):
      if not self.download_all_active_ones:
        if not ytchannel.is_downloadable_on_date:
          log_msg = 'File ' + ytchannel.filename + 'not be downloaded today. Continuing...'
          print(log_msg)
          logger.info(log_msg)
          continue
      entry_abspath = ytchannel.datedpage_filepath
      if os.path.isfile(entry_abspath):
        self.n_exists += 1
        print(self.n_exists, '[EXISTS]', entry_abspath)
        continue
      seq = i+1
      n_of_m = '%d/%d/%d' % (seq, self.total_channels, self.n_of_download_rolls)
      log_msg = n_of_m + ' >>> Going to download ' + ytchannel.murl
      print(log_msg)
      logger.info(log_msg)
      # DOWNLOAD happens here
      res = requests.get(ytchannel.videospageurl, allow_redirects=True)
      if res.status_code != 200:
        self.n_fail_200 += 1
        error_msg = 'Page [%s] returned a not 200 status response' % ytchannel.videospageurl
        print(error_msg)
        logger.error(error_msg)
        # instead of raising an exception, log message to a file
        # raise IOError(error_msg)
        continue
      self.n_downloaded += 1
      fp = open(entry_abspath, 'w')
      fp.write(res.text)
      fp.close()

      wait_secs = dtfs.get_random_config_download_wait_nsecs()
      datedpagefn = ytchannel.datedpage_filename
      log_msg = ' => written ' + datedpagefn
      print(log_msg)
      print(':: wait', wait_secs, 'seconds.')
      logger.info(log_msg)
      drill.extract_videoitems_from_videopage(ytchannel.ytchannelid, today)

      time.sleep(wait_secs)

  def report(self):
    """

    :return:
    """
    log_msg = 'Report:          n_of_download_rolls = ' + str(self.n_of_download_rolls)
    print(log_msg)
    logger.info(log_msg)
    log_msg = 'n_exists = %d ; n_downloaded = %d ; n_fail_200 = %d ; total_channels = %d' \
              % (self.n_exists, self.n_downloaded, self.n_fail_200, self.total_channels)
    print(log_msg)
    logger.info(log_msg)


class DownloadProcessOption:

  WAIT_MINS_FOR_DOWNLOAD_ROLL = 3

  def __init__(self, run_with_emptyfinder_option=None, download_all_active_ones=True):
    self.download_all_active_ones = download_all_active_ones
    self.run_with_emptyfinder_option = run_with_emptyfinder_option
    if self.run_with_emptyfinder_option not in [None, True]:
      self.run_with_emptyfinder_option = False
    self.n_download_rolls = 1
    self._max_download_rolls = None
    self.do_a_download_roll()

  @property
  def max_download_rolls(self):
    return self._max_download_rolls

  @max_download_rolls.setter
  def max_download_rolls(self, max_dld_rolls):
    self._max_download_rolls = max_dld_rolls

  def process(self):
    outdict = {'run_with_emptyfinder_option': self.run_with_emptyfinder_option}
    if self.run_with_emptyfinder_option:
      self.run_emptyfinder_n_redownload_n_times()
    else:
      self.do_a_download_roll()
      emptyfinder = RunEmtpyFinderThuFolder()
      emptyfinder.run_thu_folder_htmls(False)
      emptyfinder.report()
      outdict = {'n_of_empties': emptyfinder.n_of_empties}
    return outdict

  def do_a_download_roll(self):
    downloader = DownloadYtVideoPages(self.n_download_rolls, self.download_all_active_ones)
    downloader.download_ytvideopages()
    downloader.report()
    logging.shutdown()  # to close all files/handlers
    self.n_download_rolls += 1

  def run_emptyfinder_n_redownload_n_times(self):
    """
      The first dodownload() does not redownload if files are in folder.
      The redownload happens after files are erased from it resulting in non-scrapeable.
    :param :
    :return:
    """
    self.do_a_download_roll()
    print(' [End of Processing] n_download_rolls =', self.n_download_rolls, '| max rolls =', self.max_download_rolls)


DEFAULT_MAX_DOWNLOAD_ROLLS = 7


def get_args():
  pdict = {'maxtries': DEFAULT_MAX_DOWNLOAD_ROLLS, 'dld_all_active': True}
  for arg in sys.argv:
    if arg.startswith('--help'):
      print(__doc__)
      sys.exit()
    elif arg.startswith('--maxtries='):
      maxtries = int(arg[len('--maxtries='):])
      pdict['maxtries'] = maxtries
    elif arg.startswith('--allactive='):
      allactive = int(arg[len('--allactive='):])
      allactive = bool(allactive)
      pdict['dld_all_active'] = allactive
  return pdict


def get_args_n_run_downloads_n_check_empties_if_so():
  """
   # if True, all active ones are to be downloaded otherwise just those "on date" (defined by dld_each_days on db)
  :return:
  """
  argsdict = get_args()
  _ = argsdict['maxtries']
  download_all_active_ones = argsdict['dld_all_active']
  print('-'*50)
  print('Starting downloading process: download_all_active_ones =', download_all_active_ones)
  print('-'*50)
  run_with_emptyfinder_option = False
  dld_o = DownloadProcessOption(run_with_emptyfinder_option, download_all_active_ones)
  pdict = dld_o.process()
  print('process dict', pdict)


def test1():
  pass


def process():
  get_args_n_run_downloads_n_check_empties_if_so()
  # test1()


if __name__ == '__main__':
  process()
