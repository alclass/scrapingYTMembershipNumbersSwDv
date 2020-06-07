#!/usr/bin/python3
from sqlalchemy.orm import sessionmaker
from models.gen_models.YtVideosPageMod import YtVideosPage
from models.sa_models.ytchannelsubscribers_samodels import YTChannelSA
from fs.db.sqlalchdb.sqlalchemy_conn import sqlalchemy_engine

Session = sessionmaker(bind=sqlalchemy_engine)

def FetchYtVideosPageByItsIdInDB(ytchannelid):
  session = Session()
  ytchannel = session.query(YTChannelSA) \
    .filter(YTChannelSA.ytchannelid == ytchannelid) \
    .first()
  ytvideospage = None
  if ytchannel:
    ytvideospage = YtVideosPage(ytchannel.ytchannelid, ytchannel.nname)
  session.close()
  return ytvideospage

def adhoc_test():
  pass

def process():
  adhoc_test()

if __name__ == '__main__':
  process()
