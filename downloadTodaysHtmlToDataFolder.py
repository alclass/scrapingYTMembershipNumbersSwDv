#!/usr/bin/python3
import os, requests, time
import readjson
import YtChannelMod

class DownloadYtVideoPages:

  def __init__(self):
    self.ytchannels = []
    self.from_json_to_ytchannel()

  def from_json_to_ytchannel(self):
    channelsdatareader = readjson.JsonYtChannel()
    for channeldict in channelsdatareader.loopthru():
      nname  = channeldict['nname']
      ytchid = channeldict['ytchid']
      ytchannel = YtChannelMod.YtChannel(ytchid, nname)
      self.ytchannels.append(ytchannel)

  def download_ytvideopages(self):
    seq = 0
    for ytchannel in self.ytchannels:
      entry_abspath = ytchannel.datedpage_filepath
      if os.path.isfile(entry_abspath):
        print ('<<< EXISTS', entry_abspath)
        continue
      seq += 1
      print(seq, '>>> Going to download', ytchannel.murl)
      res = requests.get(ytchannel.videospageurl, allow_redirects=True)
      if res.status_code != 200:
        error_msg = 'Page [%s] returned a not 200 status response' %ytchannel.videospageurl
        print(error_msg)
        # raise IOError(error_msg)
      fp = open(entry_abspath, 'w')
      fp.write(res.text) # fp.write(str(res.content)) # it was observed that res.text goes UTF8, before res.content went non-UTF8
      fp.close()
      print('Written ', ytchannel.datedpage_filename, ': wait 3 seconds.')
      time.sleep(3)

def process():
  downloader = DownloadYtVideoPages()
  downloader.download_ytvideopages()

if __name__ == '__main__':
  process()