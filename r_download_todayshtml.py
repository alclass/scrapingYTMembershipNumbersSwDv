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
  #<scriptname> [--maxtries=<number>] [--allactive=<boolean>]
obs:
  --maxtries  => maximum number of tries when download file does not have data-extractable;
  if --maxtries is not given, the default will be used. (At the time of this writing, it's 7.)

  --allactive  => downloads all active channels in db, if False, it downloads according to dld_each_days parameter in db;
  if --allactive is not given, the default will be used. (At the time of this writing, it's ', ie, True.)
'''
import os, requests, time, sys
from fs.db.jsondb import readjson
import models.gen_models.YtVideosPageMod as ytvidpagesmod
import fs.datefunctions.datefs as dtfs
from models.scrapers.YTVideoItemBsoupIsEmptyMod import RunEmtpyFinderThuFolder
from models.procdb.SubscriberInsertorMod import Session
import models.sa_models.ytchannelsubscribers_samodels as samodels

class DownloadYtVideoPages:

  def __init__(self, n_of_download_rolls=None, download_all_active_ones=True):
    self.download_all_active_ones = download_all_active_ones
    self.ytchannels = []
    self.n_exists = 0; self.n_downloaded = 0; self.n_fail_200 = 0; self.total_channels = 0
    self.set_n_of_download_rolls(n_of_download_rolls)
    self.from_db_to_ytchannel()

  def set_n_of_download_rolls(self, n_of_download_rolls):
    self.n_of_download_rolls = n_of_download_rolls
    if self.n_of_download_rolls is None or type(self.n_of_download_rolls) != int:
      self.n_of_download_rolls = 1

  def fallback_from_json_to_ytchannel(self):
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
    dbytchannels = session.query(samodels.YTChannelSA). \
      order_by(samodels.YTChannelSA.nname). \
      all()
    for ytchannel in dbytchannels:
      if not self.download_all_active_ones:
        if not ytchannel.is_downloadable_on_date():
          continue
      ytchannelpage = ytvidpagesmod.YtVideosPage(ytchannel.ytchannelid, ytchannel.nname)
      ytchannelpage.downloadable_on_date = True
      ytchannelpage.set_sname_by_nname()
      self.ytchannels.append(ytchannelpage)
    session.close()

  def download_ytvideopages(self):
    self.total_channels = len(self.ytchannels)
    for i, ytchannel in enumerate(self.ytchannels):
      if not self.download_all_active_ones:
        try:
          if not ytchannel.downloadable_on_date:
            print('File', ytchannel.filename, 'not be downloaded today. Continuing...')
            continue
        except AttributeError as e:
          error_msg = 'Missing downloadable_on_date for knowing whether or not page is to be download today.\n' + str(e)
          raise AttributeError(error_msg)
      entry_abspath = ytchannel.datedpage_filepath
      if os.path.isfile(entry_abspath):
        self.n_exists += 1
        print (self.n_exists, '[EXISTS]', entry_abspath)
        continue
      seq = i+1
      n_of_m = '%d/%d/%d' %(seq, self.total_channels, self.n_of_download_rolls)
      print(n_of_m, '>>> Going to download', ytchannel.murl)
      # DOWNLOAD happens here
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
    self.n_download_rolls += 1

  def run_emptyfinder_n_redownload_n_times(self):
    '''
      The first dodownload() does not redownload if files are in folder.
      The redownload happens after files are erased from it resulting in non-scrapeable.
    :param n_tries:
    :return:
    '''
    self.do_a_download_roll()
    #print('Checking for DOM-empty files. Please, wait.')
    #emptyfinder = RunEmtpyFinderThuFolder()
    #emptyfinder.run_thu_folder_htmls()
    #emptyfinder.report()
    if False: # emptyfinder.n_of_empties > 0:
      while self.n_download_rolls < self.max_download_rolls:
        self.n_download_rolls += 1
        print (' ::: Waiting', self.WAIT_MINS_FOR_DOWNLOAD_ROLL, 'minutes for a redownload roll of ', emptyfinder.n_of_empties, ' empties.')
        time.sleep(self.WAIT_MINS_FOR_DOWNLOAD_ROLL*60)
        self.do_a_download_roll()
        #print('Checking for DOM-empty files. Please, wait.')
        #emptyfinder.run_thu_folder_htmls()
        #emptyfinder.report()
        if True or emptyfinder.n_of_empties == 0:
          break
    print (' [End of Processing] n_download_rolls =', self.n_download_rolls, '| max rolls =', self.max_download_rolls)

DEFAULT_MAX_DOWNLOAD_ROLLS = 7
def get_args():
  pdict = {'maxtries':DEFAULT_MAX_DOWNLOAD_ROLLS, 'dld_all_active':True}
  for arg in sys.argv:
    if arg.startswith('--help'):
      print(__doc__)
      sys.exit()
    elif arg.startswith('--maxtries='):
      maxtries = int(arg[len('--maxtries='):])
      pdict['maxtries'] = maxtries
    elif arg.startswith('--allactive='):
      allactive =  int(arg[len('--allactive='):])
      allactive = bool(allactive)
      pdict['dld_all_active'] = allactive
  return pdict

def get_args_n_run_downloads_n_check_empties_if_so():
  argsdict = get_args()
  _ = argsdict['maxtries']
  download_all_active_ones = argsdict['dld_all_active'] # if True, all active ones are to be downloaded otherwise just those "on date" (defined by dld_each_days on db)
  print ('-'*50)
  print ('Starting downloading process: download_all_active_ones =', download_all_active_ones)
  print ('-'*50)
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