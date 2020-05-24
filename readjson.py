#!/usr/bin/python3
import json, os
# from collections import namedtuple, OrderedDict

CHANNEL_URLS_FILENAME = 'channelvideosytpages.json'

YT_URL_PREFIX = "https://www.youtube.com/"
YT_URL_SUFIX  = "/videos"
def get_url_from_murl(murl):
  return YT_URL_PREFIX + murl + YT_URL_SUFIX

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
  channeldict = {} # ChannelNT = namedtuple('ChannelNT', 'nname url')
  channels = YtChannelYielder()
  for channeldictitem in channels.loopthru():
    nname = channeldictitem['nname']
    murl = channeldictitem['murl']
    url = get_url_from_murl(murl)
    channeldict[nname] = url
  nnames = channeldict.keys()
  nnames = sorted(nnames)
  for i, nname in enumerate(nnames):
    url = channeldict[nname]
    print (i+1, nname, url)

if __name__ == '__main__':
  process()
