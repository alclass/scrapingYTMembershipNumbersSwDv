#!/usr/bin/python3
'''
This script downloads YouTube video pages that belong to channels
  in the database.  It will only download pages once a day
  as each html file is named per day.

Statistically, some of these downloaded video pages will be DOM-empty,
  ie, they can not be scraped by the technique in this system,
  which uses the DOM.

The searched info in this case is observed to be found in the Javascript,
  but this system unfortunately does not look into the Javascript,
  so a redownload may solve the issue.
  (Some times more than one redownload may be necessary.)

Thus as a downloaded file is DOM-empty, it's deleted and then put in
  a list for later redownloading. (It takes some seconds delay.)

The param arg --maxtries=<number> defines how many times
  a redownload roll may happen.  Its DEFAULT is 3.

At the end, a print message will show how many files are still empty,
  and, after 3 tries, it's expected that no remaining files
  will still be DOM-empty, ie, they will all be DOM-scrapeable.

Usage:
  #<scriptname> [--maxtries=<number>]
obs: if --maxtries is not given, the default will be used.
'''
import os, requests, time, sys
from fs.db.jsondb import readjson
import models.gen_models.YtVideosPageMod as ytvidpagesmod
import fs.datefunctions.datefs as dtfs
from models.scrapers.YTVideoItemBsoupIsEmptyMod import RunEmtpyFinderThuFolder
from models.procdb.SubscriberInsertorMod import Session
import models.sa_models.ytchannelsubscribers_samodels as samodels

class DownloadYtVideoPages:

  def __init__(self, n_of_download_rolls=None):
    self.ytchannels = []
    self.n_exists = 0; self.n_downloaded = 0; self.n_fail_200 = 0; self.total_channels = 0
    self.set_n_of_download_rolls(n_of_download_rolls)
    self.from_json_to_ytchannel()

  def set_n_of_download_rolls(self, n_of_download_rolls):
    self.n_of_download_rolls = n_of_download_rolls
    if self.n_of_download_rolls is None or type(self.n_of_download_rolls) != int:
      self.n_of_download_rolls = 1

  def from_json_to_ytchannel(self):
    '''
      Deactivated
    :return:
    '''
    channelsdatareader = readjson.JsonYtChannel()
    for channeldict in channelsdatareader.loopthru():
      nname  = channeldict['nname']
      ytchid = channeldict['ytchannelid']
      ytchannel = ytvidpagesmod.YtVideosPage(ytchid, nname)
      self.ytchannels.append(ytchannel)

  def from_db_to_ytchannel(self):
    '''
      Deactivated
    :return:
    '''
    session = Session()
    ytchannels = session.query(samodels.YTChannelSA). \
      order_by(samodels.YTChannelSA.nname). \
      all()
    for ytchannel in ytchannels:
      if ytchannel.is_downloadable_on_date():
        continue
      ytchannelpage = ytvidpagesmod.YtVideosPage(ytchannel.ytchannel, ytchannel.nname)
      self.ytchannels.append(ytchannelpage)
    session.close()

  def download_ytvideopages(self):
    self.total_channels = len(self.ytchannels)
    for i, ytchannel in enumerate(self.ytchannels):
      entry_abspath = ytchannel.datedpage_filepath
      if os.path.isfile(entry_abspath):
        self.n_exists += 1
        print (self.n_exists, '[EXISTS]', entry_abspath)
        continue
      seq = i+1
      n_of_m = '%d/%d/%d' %(seq, self.total_channels, self.n_of_download_rolls)
      print(n_of_m, '>>> Going to download', ytchannel.murl)
      res = requests.get(ytchannel.videospageurl, allow_redirects=True)
      if res.status_code != 200:
        self.n_fail_200 += 1
        error_msg = 'Page [%s] returned a not 200 status response' %ytchannel.videospageurl
        print(error_msg)
        # instead of raising an exception, log message to a file
        # raise IOError(error_msg)
        continue
      self.n_downloaded += 1
      fp = open(entry_abspath, 'w')
      fp.write(res.text) # fp.write(str(res.content)) # it was observed that res.text goes UTF8, before res.content went non-UTF8
      fp.close()

      wait_secs = dtfs.get_random_config_download_wait_nsecs() # takes a different one every moment
      datedpagefn = ytchannel.datedpage_filename
      print(' => written ', datedpagefn) # ,': %d inscritos' %qty
      print(':: wait', wait_secs, 'seconds.')
      time.sleep(wait_secs)

  def report(self):
    print('Report:          n_of_download_rolls =', self.n_of_download_rolls)
    print('n_exists =', self.n_exists, '; n_downloaded =', self.n_downloaded, '; n_fail_200 =', self.n_fail_200, '; total_channels =', self.total_channels)

def dodownload(n_of_download_rolls=None):
  downloader = DownloadYtVideoPages(n_of_download_rolls=n_of_download_rolls)
  downloader.download_ytvideopages()
  downloader.report()

WAIT_MINS_FOR_DOWNLOAD_ROLL = 3
def run_emptyfinder_n_redownload_n_times(max_download_rolls):
  '''
    The first dodownload() does not redownload if files are in folder.
    The redownload happens after files are erased from it resulting in non-scrapeable.
  :param n_tries:
  :return:
  '''
  n_of_download_rolls = 1
  dodownload()
  print('Checking for DOM-empty files. Please, wait.')
  emptyfinder = RunEmtpyFinderThuFolder()
  emptyfinder.run_thu_folder_htmls()
  emptyfinder.report()
  if emptyfinder.n_of_empties > 0:
    while n_of_download_rolls < max_download_rolls:
      n_of_download_rolls += 1
      print (' ::: Waiting', WAIT_MINS_FOR_DOWNLOAD_ROLL, 'minutes for a redownload roll of ', emptyfinder.n_of_empties, ' empties.')
      time.sleep(WAIT_MINS_FOR_DOWNLOAD_ROLL*60)
      dodownload(n_of_download_rolls)
      print('Checking for DOM-empty files. Please, wait.')
      emptyfinder.run_thu_folder_htmls()
      emptyfinder.report()
      if emptyfinder.n_of_empties == 0:
        break
  print (' [End of Processing] n_of_download_rolls =', n_of_download_rolls, '| max rolls =', max_download_rolls)

DEFAULT_MAX_DOWNLOAD_ROLLS = 7
def get_ntries_arg():
  for arg in sys.argv:
    if arg.startswith('--help'):
      print(__doc__)
      sys.exit()
    elif arg.startswith('--maxtries='):
      return int(arg[len('--maxtries='):])
  return None

def run_downloads_n_check_empties():
  max_download_rolls = get_ntries_arg() or DEFAULT_MAX_DOWNLOAD_ROLLS
  print ('Starting downloading process: n_tries =', max_download_rolls)
  print ('-'*50)
  run_emptyfinder_n_redownload_n_times(max_download_rolls)

def test1():
  max_tries = get_ntries_arg() or DEFAULT_MAX_DOWNLOAD_ROLLS
  print ('max_download_rolls', max_tries)

def process():
  run_downloads_n_check_empties()
  # test1()

if __name__ == '__main__':
  process()