#!/usr/bin/python3
import os, requests, time
import readjson
import YtChannelMod
import datefunctions.datefs as dtfs

class DownloadYtVideoPages:

  def __init__(self):
    self.ytchannels = []
    self.n_exists = 0; self.n_downloaded = 0; self.n_fail_200 = 0; self.total_channels = 0
    self.from_json_to_ytchannel()

  def from_json_to_ytchannel(self):
    channelsdatareader = readjson.JsonYtChannel()
    for channeldict in channelsdatareader.loopthru():
      nname  = channeldict['nname']
      ytchid = channeldict['ytchid']
      ytchannel = YtChannelMod.YtChannel(ytchid, nname)
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
        # raise IOError(error_msg)
      self.n_downloaded += 1
      fp = open(entry_abspath, 'w')
      fp.write(res.text) # fp.write(str(res.content)) # it was observed that res.text goes UTF8, before res.content went non-UTF8
      fp.close()
      wait_secs = dtfs.get_random_config_download_wait_nsecs()
      print(self.n_downloaded, ' => written ', ytchannel.datedpage_filename, ': wait', wait_secs, 'seconds.')
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