#!/usr/bin/python3
import os, requests, time
from fs.db.jsondb import readjson
import models.gen_models.YtVideosPageMod as ytvidpagesmod
import fs.datefunctions.datefs as dtfs

from models.scrapers.SubscriberScraperMod import HTMLScraper

class DownloadYtVideoPages:

  def __init__(self):
    self.ytchannels = []
    self.n_exists = 0; self.n_downloaded = 0; self.n_fail_200 = 0; self.total_channels = 0
    self.from_json_to_ytchannel()

  def from_json_to_ytchannel(self):
    channelsdatareader = readjson.JsonYtChannel()
    for channeldict in channelsdatareader.loopthru():
      nname  = channeldict['nname']
      ytchid = channeldict['ytchannelid']
      ytchannel = ytvidpagesmod.YtVideosPage(ytchid, nname)
      self.ytchannels.append(ytchannel)

  def download_ytvideopages(self):
    self.total_channels = len(self.ytchannels)
    for i, ytchannel in enumerate(self.ytchannels):
      entry_abspath = ytchannel.datedpage_filepath
      if os.path.isfile(entry_abspath):
        self.n_exists += 1
        print (self.n_exists, '[EXISTS]', entry_abspath)
        continue
      seq = i+1
      print(seq, '>>> Going to download', ytchannel.murl)
      res = requests.get(ytchannel.videospageurl, allow_redirects=True)
      if res.status_code != 200:
        self.n_fail_200 += 1
        error_msg = 'Page [%s] returned a not 200 status response' %ytchannel.videospageurl
        print(error_msg)
        # instead of raising an exception, log message to a file
        # raise IOError(error_msg)
      self.n_downloaded += 1
      fp = open(entry_abspath, 'w')
      fp.write(res.text) # fp.write(str(res.content)) # it was observed that res.text goes UTF8, before res.content went non-UTF8
      fp.close()

      # TO-DO: method scraper.scrape_by_whole_html(text) should be able to scrape all items once top to bottom
      #scraper = HTMLScraper(ytchannel) # ytvideopagesobj is ytchannel
      #scraper.scrape_by_whole_html(res.text)
      #qty = scraper.ytvideopageobj.nOfSubscribers

      wait_secs = dtfs.get_random_config_download_wait_nsecs() # takes a different one every moment
      datedpagefn = ytchannel.datedpage_filename
      print(self.n_downloaded, ' => written ', datedpagefn) # ,': %d inscritos' %qty
      print(':: wait', wait_secs, 'seconds.')
      time.sleep(wait_secs)

  def report(self):
    print('Report:')
    print('n_exists =', self.n_exists, '; n_downloaded =', self.n_downloaded, '; n_fail_200 =', self.n_fail_200, '; total_channels =', self.total_channels)

def process():
  downloader = DownloadYtVideoPages()
  downloader.download_ytvideopages()
  downloader.report()

if __name__ == '__main__':
  process()