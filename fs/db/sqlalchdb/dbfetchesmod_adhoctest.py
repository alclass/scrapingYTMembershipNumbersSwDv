#!/usr/bin/env python3
"""
  docstring
"""
from models.gen_models.YtVideosPageMod import YtVideosPage
import fs.db.sqlalchdb.dbfetchesmod as dbfetch


def adhoc_test():
  ytchannelid = 'ueduardoamoreira'
  nname = 'Eduardo Moreira'
  ytvideopage = YtVideosPage(ytchannelid, nname)
  ytvideopage.sname = nname[:10]

  boolresult = dbfetch.fetch_ytchannel_by_ytchannelid_n_transpose(ytchannelid, ytvideopage)
  print('boolresult', boolresult)
  print(ytvideopage)
  print(ytvideopage.sname, ' downloadable_on_date =', ytvideopage.downloadable_on_date)


def process():
  adhoc_test()


if __name__ == '__main__':
  process()
