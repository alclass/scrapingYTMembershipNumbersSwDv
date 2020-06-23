#!/usr/bin/python3
from models.procdb.SubscriberInsertorMod import Session
import models.sa_models.ytchannelsubscribers_samodels as samodels
import config, os

EACH_N_DAYS_DICTLIST_FILENAME = 'nname_n_each_n_days_for_dld.dict.txt'

class EachNDays:

  def __init__(self):
    pass

  def show_dowloadables(self):
    self.n_update = 0
    session = Session()
    ytchannels = session.query(samodels.YTChannelSA).all()
    for ytchannel in ytchannels:
      is_downloadable = ytchannel.is_downloadable_on_date()
      print (is_downloadable, ytchannel)

  def read_each_n_days_dictlist_from_file(self, filename=None):
    if filename is None or not os.path.isfile(filename):
      filename = EACH_N_DAYS_DICTLIST_FILENAME
    if not os.path.isfile(filename):
      error_msg = 'filename %s for EACH_N_DAYS_DICTLIST_FILENAME does not exist.'
      raise ValueError(error_msg)
    jsonabspath = config.get_ytchannels_jsonfolderabspath()
    filepath = os.path.join(jsonabspath, filename)
    fp = open(filepath, 'r', encoding='utf8')
    each_n_days_dictlist_text = fp.read()
    indictlist = eval(each_n_days_dictlist_text)
    return indictlist

  def update_each_n_days_for_dld(self):
    self.n_update = 0
    session = Session()
    for each_n_days_dict in self.read_each_n_days_dictlist_from_file():
      ytchannel = session.query(samodels.YTChannelSA). \
        filter(samodels.YTChannelSA.nname == each_n_days_dict['nname']). \
        first()
      if ytchannel.each_n_days_for_dld != each_n_days_dict['each_n_days_for_dld']:
        ytchannel.each_n_days_for_dld = each_n_days_dict['each_n_days_for_dld']
        self.n_update += 1
        print (self.n_update, 'UPDATING ytchannel.each_n_days_for_dld =', each_n_days_dict['each_n_days_for_dld'])
        session.commit()
    session.close()

  def get_text_version_of_each_n_days_dictlist(self):
    session = Session()
    ytchannels = session.query(samodels.YTChannelSA). \
      order_by(samodels.YTChannelSA.nname). \
      all()
    outtext = '[\n'
    for ytchannel in ytchannels:
      outdict = {'nname': ytchannel.nname, 'each_n_days_for_dld':ytchannel.each_n_days_for_dld}
      outtext += str(outdict) + ',\n'
    outtext += ']'
    session.close()
    return outtext

  def printout_each_n_days_for_dld(self):
    outtext = self.get_text_version_of_each_n_days_dictlist()
    print(outtext)

  def save_to_file_each_n_days_for_dld(self, filename=None):
    if filename is None or not os.path.isfile(filename):
      filename = EACH_N_DAYS_DICTLIST_FILENAME
    jsonabspath = config.get_ytchannels_jsonfolderabspath()
    filepath = os.path.join(jsonabspath, filename)
    outtext = self.get_text_version_of_each_n_days_dictlist()
    try:
      fp = open(filepath, 'w', encoding='utf8')
      fp.write(outtext)
      fp.close()
    except IOError:
      return False
    return True

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
  EachNDays().update_each_n_days_for_dld()

if __name__ == '__main__':
  process()
