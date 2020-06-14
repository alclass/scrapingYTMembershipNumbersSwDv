from sqlalchemy.orm import sessionmaker
import models.sa_models.ytchannelsubscribers_samodels as samodels
from models.sa_models.ytchannelsubscribers_samodels import YTChannelSA
from fs.db.sqlalchdb.sqlalchemy_conn import sqlalchemy_engine

Session = sessionmaker(bind=sqlalchemy_engine)

def output_ytchannel_videos(ytchannelid): # , session

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

def test_backref(ytchannelid):
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

def process():
  '''
  videoviewsobj = output_ytchannel_videos(ytchannelid) # , session
  for e in videoviewsobj:
    print(e)
  :return:
  '''
  ytchannelid = 'ueduardoamoreira'
  test_backref(ytchannelid)

if __name__ == '__main__':
  process()
