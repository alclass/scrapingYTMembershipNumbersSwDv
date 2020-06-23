#!/usr/bin/python3
from models.procdb.SubscriberInsertorMod import Session
import models.sa_models.ytchannelsubscribers_samodels as samodels
import config, os

def update_each_n_days_for_dld():
  session = Session()
  jsonabspath = config.get_ytchannels_jsonfolderabspath()
  filepath = os.path.join(jsonabspath, 'nname_n_each_n_days_for_dld.dict.txt')
  fp = open(filepath, 'r', encoding='utf8')
  indicttext = fp.read()
  indictlist = eval(indicttext)
  n_update = 0
  for indict in indictlist:
    ytchannel = session.query(samodels.YTChannelSA). \
      filter(samodels.YTChannelSA.nname == indict['nname']). \
      first()
    if ytchannel.each_n_days_for_dld != indict['each_n_days_for_dld']:
      ytchannel.each_n_days_for_dld = indict['each_n_days_for_dld']
      n_update += 1
      print ('UPDATING ytchannel.each_n_days_for_dld =', indict['each_n_days_for_dld'])
      session.commit()
  session.close()

def printout_each_n_days_for_dld():
  session = Session()
  ytchannels = session.query(samodels.YTChannelSA). \
    order_by(samodels.YTChannelSA.nname). \
    all()
  outtext = '[\n'
  for ytchannel in ytchannels:
    outdict = {'nname': ytchannel.nname, 'each_n_days_for_dld':ytchannel.each_n_days_for_dld}
    outtext += str(outdict) + ',\n'
  outtext += ']'
  print(outtext)
  session.close()

def test_videos_per_day():
  session = Session()
  ytchannel = session.query(samodels.YTChannelSA). \
    filter(samodels.YTChannelSA.ytchannelid=='ueduardoamoreira'). \
    first()
  print(ytchannel)
  print('get_videos_per_day', ytchannel.get_videos_per_day())
  session.close()

def process():
  # printout_each_n_days_for_dld()
  update_each_n_days_for_dld()

if __name__ == '__main__':
  process()
