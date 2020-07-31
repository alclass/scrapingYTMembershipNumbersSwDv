#!/usr/bin/env python3
"""
  docstring
"""
import json
import config
import fs.filefunctions.pathfunctions as pathfs

JSON_KEY_FOR_YTCHANNELID = 'ytchid'


class JsonYtChannel:

  def __init__(self):
    self.channelsdata = []
    self.nnames_set = set()
    self.readin_jsondata()

  def readin_jsondata(self):
    try:
      ytchannels_jsonabspath = config.get_ytchannels_jsonabspath()
    except OSError:
      return
    content = open(ytchannels_jsonabspath, 'r').read()
    jsondictlist = json.loads(content)
    for i, d in enumerate(jsondictlist):
      nname = d['nn']
      if nname in self.nnames_set:
        error_msg = '"name" %s is already in json database. ' % nname
        raise KeyError(error_msg)
      self.nnames_set.add(nname)
      channeldict = {'nname': nname}
      ytchid = d[JSON_KEY_FOR_YTCHANNELID]
      if ytchid is None or len(ytchid) < 2:  # at least 'u1'
        continue
      elif '/' in ytchid:
        error_msg = 'ytchannelid has a forward slash (/)'
        raise ValueError(error_msg)
      channeldict['ytchannelid'] = ytchid
      self.channelsdata.append(channeldict)
      # print(i+1, '=>', channeldict)

  def loopthru(self):
    for i, record_dict in enumerate(self.channelsdata):
      yield record_dict


def process():
  channeldict = {}  # ChannelNT = namedtuple('ChannelNT', 'nname url')
  channels = JsonYtChannel()
  for channeldictitem in channels.loopthru():
    nname = channeldictitem['nname']
    ytchid = channeldictitem['ytchannelid']
    url = pathfs.get_ytchannelvideospage_url_from_ytchid(ytchid)
    channeldict[nname] = url
  nnames = channeldict.keys()
  nnames = sorted(nnames)
  for i, nname in enumerate(nnames):
    url = channeldict[nname]
    print(i+1, nname, url)


if __name__ == '__main__':
  process()
