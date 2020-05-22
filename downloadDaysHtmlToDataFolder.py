#!/usr/bin/python3
import datetime, os, requests
import bs4
import datefunctions.datefs as dtfs
import readjson
import YtChannelMod

SUBSCRIBERS_NUMBER_HTMLCLASSNAME = 'yt-subscription-button-subscriber-count-branded-horizontal'
DATA_LOCALFOLDERNAME = 'data'

class DownloadYtVideoPages:

  def __init__(self):
    self.ytchannels = []
    self.from_json_to_ytchannel()
    # self.download_ytvideopages()

  def from_json_to_ytchannel(self):
    channelsdatareader = readjson.YtChannelYielder()
    for channeldict in channelsdatareader.loopthru():
      nname = channeldict['nname']
      murl  = channeldict['murl']
      ytchannel = YtChannelMod.YtChannel(nname, murl)
      self.ytchannels.append(ytchannel)

  def download_ytvideopages(self):
    seq = 0
    for ytchannel in self.ytchannels:
      entry_abspath = ytchannel.absfilepath
      if os.path.isfile(entry_abspath):
        print ('<<< EXISTS', entry_abspath)
        continue
      seq += 1
      print(seq, '>>> Going to download', ytchannel.murl)
      res = requests.get(ytchannel.videospageurl, allow_redirects=True)
      if res.status_code != 200:
        error_msg = 'Page [%s] returned a not 200 status response' %ytchannel.videospageurl
        raise IOError(error_msg)
      fp = open(ytchannel.absfilepath, 'w')
      fp.write(str(res.content))
      print('Written ', ytchannel.datedpage_filename)
      fp.close()

  def parse_htmls_on_data_folder(self):
    n = len(self.ytchannels); seq = 0
    print('Number of channels =>', n)
    for ytchannel in self.ytchannels:
      if not os.path.isfile(ytchannel.absfilepath):
        continue
      filename = ytchannel.datedpage_filename
      # print('Parsing =>', filename)
      extlessname = os.path.splitext(filename)[0]
      content = open(ytchannel.absfilepath).read()
      bsoup = bs4.BeautifulSoup(content, 'html.parser')
      # result, if found, is a bs4.element.Tag object
      result = bsoup.find('span', attrs={'class':SUBSCRIBERS_NUMBER_HTMLCLASSNAME})
      if result is None:
        print('Subscribers number not found for', extlessname)
        continue
      try:
        arialabel = result['aria-label']
        seq += 1
        print (seq, '=>', extlessname, 'has', arialabel)
      except IndexError:
        print('Subscribers number not found for', extlessname)

def process():
  downloader = DownloadYtVideoPages()
  downloader.download_ytvideopages()
  downloader.parse_htmls_on_data_folder()

if __name__ == '__main__':
  process()