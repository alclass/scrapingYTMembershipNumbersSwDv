from sqlalchemy.orm import sessionmaker
import models.sa_models.ytchannelsubscribers_samodels as samodels
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

def process():
  ytchannelid = 'ueduardoamoreira'
  videoviewsobj = output_ytchannel_videos(ytchannelid) # , session
  for e in videoviewsobj:
    print(e)

if __name__ == '__main__':
  process()
