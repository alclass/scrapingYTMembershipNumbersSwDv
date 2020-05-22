#!/usr/bin/python3
import copy, json, os
# import bs4
CHANNEL_URLS_FILENAME = 'channelvideosytpages.json'

YT_URL_PREFIX = "https://www.youtube.com/"
YT_URL_SUFIX  = "/videos"

class YtChannelYielder:

  def __init__(self):
    self.channelsdata = []
    self.nnames_set = set()
    self.readin_jsondata()

  def readin_jsondata(self):
    if not os.path.isfile(CHANNEL_URLS_FILENAME):
      return
    content = open(CHANNEL_URLS_FILENAME, 'r').read()
    jsondictlist = json.loads(content)
    for i, d in enumerate(jsondictlist):
      nname = d['nname']
      if nname in self.nnames_set:
        error_msg = '"name" %s is already in json database. ' %nname
        raise KeyError(error_msg)
      self.nnames_set.add(nname)
      channeldict = {}
      channeldict['nname'] = nname
      murl = d['murl']
      channeldict['murl'] = murl
      self.channelsdata.append(channeldict)
      print(i+1, '=>', channeldict)

  def loopthru(self):
    for i, record_dict in enumerate(self.channelsdata):
      yield record_dict

def process():
  channels = YtChannelYielder()
  # print ('after instanciation')
  for each in channels.loopthru():
    print(each)

if __name__ == '__main__':
  process()