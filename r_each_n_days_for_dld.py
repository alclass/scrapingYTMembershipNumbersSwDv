#!/usr/bin/python3
from models.procdb.SubscriberInsertorMod import Session
import models.sa_models.ytchannelsubscribers_samodels as samodels
import config, os

EACH_N_DAYS_DICTLIST_FILENAME = 'nname_n_each_n_days_for_dld.dict.txt'

class EachNDaysForDownload:

  def __init__(self):
    pass

  def show_dowloadables(self):
    self.n_update = 0
    session = Session()
    ytchannels = session.query(samodels.YTChannelSA).all()
    outline = '\nshow_dowloadables\n'; n_of_dlds = 0
    for i, ytchannel in enumerate(ytchannels):
      is_downloadable = ytchannel.is_downloadable_on_date()
      nextdate = ytchannel.find_next_download_date()
      print (i+1, is_downloadable, nextdate, '<=', ytchannel.each_n_days_for_dld, '+', ytchannel.scrapedate, ytchannel.nname)
      if is_downloadable:
        n_of_dlds += 1
        outline += '%d %s to download \n' %(i+1, ytchannel.nname)
    print(outline)
    if n_of_dlds == 0:
      print ('=> no downloable pages for today.')
    else:
      print (n_of_dlds, 'downloable pages for today.')

  def read_from_dictfile_each_n_days_dictlist(self, filename=None):
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

  def dbupdate_each_n_days_for_dld_from_dictlist(self, dictlist):
    self.n_update = 0
    session = Session()
    for each_n_days_dict in dictlist:
      ytchannel = session.query(samodels.YTChannelSA). \
        filter(samodels.YTChannelSA.nname == each_n_days_dict['nname']). \
        first()
      if ytchannel.each_n_days_for_dld != each_n_days_dict['each_n_days_for_dld']:
        ytchannel.each_n_days_for_dld = each_n_days_dict['each_n_days_for_dld']
        self.n_update += 1
        print (self.n_update, 'UPDATING ytchannel.each_n_days_for_dld =', each_n_days_dict['each_n_days_for_dld'])
        session.commit()
    session.close()

  def dbupdate_from_dictfile_each_n_days_for_dld(self):
    dictlist = self.read_from_dictfile_each_n_days_dictlist()
    return self.dbupdate_each_n_days_for_dld_from_dictlist(dictlist)

  def dbfetch_each_n_days_dictlist(self):
    session = Session()
    ytchannels = session.query(samodels.YTChannelSA). \
      order_by(samodels.YTChannelSA.nname). \
      all()
    dictlist = []
    for ytchannel in ytchannels:
      outdict = {'nname': ytchannel.nname, 'each_n_days_for_dld':ytchannel.each_n_days_for_dld}
      dictlist.append(outdict)
    session.close()
    return dictlist

  def make_text_version_of_each_n_days_from_dictlist(self, dictlist):
    '''
      This method is implement with a for-loop
        where a dictlist ends up as a string that can be loaded back with eval().
      An alternative to the for-loop would be:
       1) list(map(lambda, iter))
       2) then '\n'.join(list) to text
       3) then wrap-up text with '[' (prefix) , ']' (postfix)
    :param dictlist:
    :return:
    '''
    outtext = '[\n'
    for indict in dictlist:
      outtext += str(indict) + ',\n'
    outtext += ']'
    return outtext

  def make_from_db_text_version_of_each_n_days_dictlist(self):
    dictlist = self.dbfetch_each_n_days_dictlist()
    return self.make_text_version_of_each_n_days_from_dictlist(dictlist)

  def print_from_db_each_n_days_for_dld(self):
    outtext = self.make_from_db_text_version_of_each_n_days_dictlist()
    print(outtext)

  def make_from_file_text_version_of_each_n_days_dictlist(self):
    dictlist = self.read_from_dictfile_each_n_days_dictlist()
    return self.make_text_version_of_each_n_days_from_dictlist(dictlist)

  def print_from_file_each_n_days_for_dld(self):
    outtext = self.make_from_file_text_version_of_each_n_days_dictlist()
    print(outtext)

  def save_to_file_from_db_each_n_days_for_dld(self, filename=None):
    if filename is None or not os.path.isfile(filename):
      filename = EACH_N_DAYS_DICTLIST_FILENAME
    jsonabspath = config.get_ytchannels_jsonfolderabspath()
    filepath = os.path.join(jsonabspath, filename)
    outtext = self.make_from_db_text_version_of_each_n_days_dictlist()
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
  # EachNDaysForDownload().update_each_n_days_for_dld()
  EachNDaysForDownload().show_dowloadables()

if __name__ == '__main__':
  process()
