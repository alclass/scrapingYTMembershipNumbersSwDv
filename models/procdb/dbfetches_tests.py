#!/usr/bin/env python3
from sqlalchemy.orm import sessionmaker
import models.sa_models.ytchannelsubscribers_samodels as samodels
from models.sa_models.ytchannelsubscribers_samodels import YTChannelSA
from models.sa_models.ytchannelsubscribers_samodels import YTVideoViewsSA
from fs.db.sqlalchdb.sqlalchemy_conn import sqlalchemy_engine
Session = sessionmaker(bind=sqlalchemy_engine)


def output_ytchannel_videos(ytchannelid):  # , session

  session = Session()

  ytchannel = session.query(samodels.YTChannelSA, samodels.YTVideoItemInfoSA). \
      filter(samodels.YTChannelSA.ytchannelid == samodels.YTVideoItemInfoSA.ytchannelid). \
      first()
  print(ytchannel)

  videoviewsobj = session.query(samodels.YTVideoItemInfoSA, samodels.YTVideoViewsSA). \
      filter(samodels.YTVideoItemInfoSA.ytchannelid == ytchannelid). \
      filter(samodels.YTVideoViewsSA.ytvideoid == samodels.YTVideoItemInfoSA.ytvideoid). \
      order_by(samodels.YTVideoViewsSA.infodate). \
      all()
  session.close()
  return videoviewsobj


def test_backref_top_to_bottom(ytchannelid):
  session = Session()
  o = session.query(YTChannelSA).filter(YTChannelSA.ytchannelid == ytchannelid).first()
  # session.close()
  print(o)
  for i, subs in enumerate(o.daily_subscribers):
    print(i+1, subs)
  totviews = 0
  for i, vinfo in enumerate(o.vinfolist):
    print(i+1, vinfo)
    print('URL', vinfo.ytvideo_url)
    for j, vview in enumerate(vinfo.vviewlist):
      totviews += 1
      print(j+1, totviews, vview)


def test_backref_to_bottom_to_top(ytvideoid):
  session = Session()
  vview = session.query(YTVideoViewsSA).filter(YTVideoViewsSA.ytvideoid == ytvideoid).first()
  # session.close()
  print(vview)
  vinfo = vview.vinfo
  print(vinfo)
  ytchannel = vinfo.ytchannel
  print(ytchannel)
  print('counter', ytchannel.daily_subscribers.count())
  print('type', type(ytchannel.daily_subscribers))
  print('type', type(reversed(list(ytchannel.daily_subscribers))))
  first = ytchannel.daily_subscribers.first()
  print('first', first)
  '''
  second = ytchannel.daily_subscribers.ext()
  print(second)
  for subs in reversed(list(ytchannel.daily_subscribers)): #.order_by('desc'):
    print(subs)
  '''


def process():
  """
  videoviewsobj = output_ytchannel_videos(ytchannelid) # , session
  for e in videoviewsobj:
    print(e)
  :return:
  """
  ytchannelid = 'ueduardoamoreira'
  test_backref_top_to_bottom(ytchannelid)
  ytvideoid = 'hzFhJCxlLeQ'  # Por que Bolsonaro não cai e mais com Portal do José on 2020-06-14
  test_backref_to_bottom_to_top(ytvideoid)


if __name__ == '__main__':
  process()
