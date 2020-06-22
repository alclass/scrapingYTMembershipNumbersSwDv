#!/usr/bin/python3
from models.procdb.SubscriberInsertorMod import Session
import models.sa_models.ytchannelsubscribers_samodels as samodels

def process():
  session = Session()
  ytchannel = session.query(samodels.YTChannelSA). \
    filter(samodels.YTChannelSA.ytchannelid=='ueduardoamoreira'). \
    first()
  print(ytchannel)
  print('get_videos_per_day', ytchannel.get_videos_per_day())

if __name__ == '__main__':
  process()
