#!/usr/bin/python3
from models.procdb.SubscriberInsertorMod import Session
import models.sa_models.ytchannelsubscribers_samodels as samodels
import fs.collectionfunctions.collfunctions as collfs
import config, json, os

EACH_N_DAYS_DICTLIST_FILENAME = 'nname_n_each_n_days_for_dld.dict.txt'
EACH_N_DAYS_JSON_FILENAME     = 'nname_n_each_n_days_for_dld.json'



class StaticEachNDays:

  @staticmethod
  def dbfetch_each_n_days_dictlist():
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

  @classmethod
  def read_from_db_each_n_days_n_return_dictlist(cls):
    return cls.dbfetch_each_n_days_dictlist()

  @staticmethod
  def make_textversion_of_each_n_days_from_dictlist(dictlist):
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

  @staticmethod
  def read_from_jsonfile_each_n_days_n_return_dictlist(filename=None):
    if filename is None or not os.path.isfile(filename):
      filename = EACH_N_DAYS_JSON_FILENAME
    if not os.path.isfile(filename):
      error_msg = 'filename [%s] for EACH_N_DAYS_DICTLIST_FILENAME does not exist.'
      raise ValueError(error_msg)
    jsonabspath = config.get_ytchannels_jsonfolderabspath()
    filepath = os.path.join(jsonabspath, filename)
    fp = open(filepath, 'r', encoding='utf8')
    each_n_days_dictlist_text = fp.read()
    indictlist = json.loads(each_n_days_dictlist_text)
    return indictlist

  @classmethod
  def write_to_dictfile_each_n_days_from_dictlist(cls, filename=None, dictlist=[]):
    if len(dictlist) == 0:
      return False
    text = cls.make_textversion_of_each_n_days_from_dictlist(dictlist)
    if filename is None or not os.path.isfile(filename):
      filename = EACH_N_DAYS_DICTLIST_FILENAME
    jsonabspath = config.get_ytchannels_jsonfolderabspath()
    filepath = os.path.join(jsonabspath, filename)
    try:
      fp = open(filepath, 'r', encoding='utf8')
      fp.write(text)
      fp.close()
    except IOError:
      return False
    return True

  @staticmethod
  def write_to_jsonfile_each_n_days_from_dictlist(filename=None, dictlist=[]):
    if len(dictlist) == 0:
      return False
    if filename is None or not os.path.isfile(filename):
      filename = EACH_N_DAYS_JSON_FILENAME
    jsonabspath = config.get_ytchannels_jsonfolderabspath()
    filepath = os.path.join(jsonabspath, filename)
    try:
      fp = open(filepath, 'r', encoding='utf8')
      text = json.dumps(dictlist)
      fp.write(text)
      fp.close()
    except IOError:
      return False
    return True

  @classmethod
  def write_to_db_each_n_days_from_dictlist(cls, dictlist=[]):
    if len(dictlist) == 0:
      return False
    nOfUpdatedRows = cls.dbupdate_each_n_days_for_dld_from_dictlist(dictlist)
    if nOfUpdatedRows > 0:
      return True
    return False

  @staticmethod
  def dbupdate_each_n_days_for_dld_from_dictlist(dictlist):
    n_update = 0
    session = Session()
    for each_n_days_dict in dictlist:
      ytchannel = session.query(samodels.YTChannelSA). \
        filter(samodels.YTChannelSA.nname == each_n_days_dict['nname']). \
        first()
      if ytchannel.each_n_days_for_dld != each_n_days_dict['each_n_days_for_dld']:
        ytchannel.each_n_days_for_dld = each_n_days_dict['each_n_days_for_dld']
        n_update += 1
        print (n_update, 'UPDATING ytchannel.each_n_days_for_dld =', each_n_days_dict['each_n_days_for_dld'])
        session.commit()
    session.close()
    return n_update

  @staticmethod
  def read_from_dictfile_each_n_days_n_return_dictlist(filename=None):
    if filename is None: # or not os.path.isfile(filename):
      filename = EACH_N_DAYS_DICTLIST_FILENAME
    jsonabspath = config.get_ytchannels_jsonfolderabspath()
    filepath = os.path.join(jsonabspath, filename)
    if not os.path.isfile(filepath):
      error_msg = 'filename %s for EACH_N_DAYS_DICTLIST_FILENAME does not exist.'
      raise ValueError(error_msg)
    # TO-DO think-about try / except
    fp = open(filepath, 'r', encoding='utf8')
    each_n_days_dictlist_text = fp.read()
    indictlist = eval(each_n_days_dictlist_text)
    return indictlist

  @classmethod
  def read_from_dictfile_each_n_days_n_return_textversion(cls):
    dictlist = cls.read_from_dictfile_each_n_days_n_return_dictlist()
    return cls.make_textversion_of_each_n_days_from_dictlist(dictlist)

  @classmethod
  def read_from_jsonfile_each_n_days_n_return_textversion(cls):
    dictlist = cls.read_from_jsonfile_each_n_days_n_return_dictlist()
    return cls.make_textversion_of_each_n_days_from_dictlist(dictlist)

  @classmethod
  def read_from_db_each_n_days_n_return_textversion(cls):
    dictlist = cls.read_from_db_each_n_days_n_return_dictlist()
    return cls.make_textversion_of_each_n_days_from_dictlist(dictlist)

  @classmethod
  def print_from_dictfile_each_n_days_for_dld(cls):
    outtext = cls.read_from_dictfile_each_n_days_n_return_textversion()
    print(outtext)

  @classmethod
  def print_from_jsonfile_each_n_days_for_dld(cls):
    outtext = cls.read_from_jsonfile_each_n_days_n_return_textversion()
    print(outtext)

  @classmethod
  def print_from_db_each_n_days_for_dld(cls):
    outtext = cls.read_from_db_each_n_days_n_return_textversion()
    print(outtext)

  @staticmethod
  def show_dowloadables_at_moment():
    session = Session()
    ytchannels = session.query(samodels.YTChannelSA).all()
    outline = '\nshow_dowloadables\n'; n_of_dlds = 0
    for i, ytchannel in enumerate(ytchannels):
      is_downloadable = ytchannel.downloadable_on_date()
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

class EachNDaysForDownloadSyncer:
  '''
  This class offers functionality for getting and setting
    attribute/field each_n_days_for_dld which determines
    how many days should pass for a new download for its related channel.
  Example:
      => if each_n_days_for_dld is 1, there'll be one download every day for related channel
      => if each_n_days_for_dld is 2,  there'll be one download every other day
      => if each_n_days_for_dld is 30,  30 days will pass for a new download
  '''

  EACH_N_DAYS_ORIGIN_DICTFILE = 'EACH_N_DAYS_ORIGIN_DICTFILE'
  EACH_N_DAYS_ORIGIN_JSONFILE = 'EACH_N_DAYS_ORIGIN_JSONFILE'
  EACH_N_DAYS_ORIGIN_DB       = 'EACH_N_DAYS_ORIGIN_DB'
  EACH_N_DAYS_TARGET_DICTFILE = 'EACH_N_DAYS_TARGET_DICTFILE'
  EACH_N_DAYS_TARGET_JSONFILE = 'EACH_N_DAYS_TARGET_JSONFILE'
  EACH_N_DAYS_TARGET_DB       = 'EACH_N_DAYS_TARGET_DB'

  EACH_N_DAYS_ORIGIN_DEFAULT = EACH_N_DAYS_ORIGIN_DICTFILE
  EACH_N_DAYS_TARGET_DEFAULT = EACH_N_DAYS_TARGET_DB

  def __init__(self, from_means, to_means):
    self.instance_dictlist = []
    self.from_means, self.to_means = from_means, to_means
    self.treat_from_to_means()

  def get_values_for_from_means(self):
    values_for_from_means = []
    values_for_from_means.append(self.EACH_N_DAYS_ORIGIN_DICTFILE)
    values_for_from_means.append(self.EACH_N_DAYS_ORIGIN_JSONFILE)
    values_for_from_means.append(self.EACH_N_DAYS_ORIGIN_DB)
    return values_for_from_means

  def get_values_for_to_means(self):
    values_for_to_means = []
    values_for_to_means.append(self.EACH_N_DAYS_TARGET_DICTFILE)
    values_for_to_means.append(self.EACH_N_DAYS_TARGET_JSONFILE)
    values_for_to_means.append(self.EACH_N_DAYS_TARGET_DB)
    return values_for_to_means

  def treat_from_to_means(self):
    self.treat_from_means()
    self.treat_to_means()
    return self.check_same_means_from_to_if_so_raise()

  def check_same_means_from_to_if_so_raise(self):
    error_msg = None
    if self.from_means == self.EACH_N_DAYS_ORIGIN_DICTFILE and \
       self.to_means   == self.EACH_N_DAYS_TARGET_DICTFILE:
      error_msg = 'Equal means from/to =  %s and %s' %(self.from_means, self.to_means)
    elif self.from_means == self.EACH_N_DAYS_ORIGIN_JSONFILE and \
       self.to_means   == self.EACH_N_DAYS_TARGET_JSONFILE:
      error_msg = 'Equal means from/to =  %s and %s' %(self.from_means, self.to_means)
    elif self.from_means == self.EACH_N_DAYS_ORIGIN_DB and \
       self.to_means   == self.EACH_N_DAYS_TARGET_DB:
      error_msg = 'Equal means from/to =  %s and %s' %(self.from_means, self.to_means)
    if error_msg is not None:
      raise ValueError(error_msg)
    return

  def treat_from_means(self):
    '''
    Alternative to setting a DEFAULT is raising an exception:
      error_msg = 'from_means (%s) should be one of the following values ' + self.get_values_for_from_means()
      raise ValueError(error_msg)

    :return:
    '''
    if self.from_means == self.EACH_N_DAYS_ORIGIN_DICTFILE:
      return
    elif self.from_means == self.EACH_N_DAYS_ORIGIN_JSONFILE:
      return
    elif self.from_means == self.EACH_N_DAYS_ORIGIN_DB:
      return
    else:
      self.from_means = self.EACH_N_DAYS_ORIGIN_DEFAULT

  def treat_to_means(self):
    '''
    Alternative to setting a DEFAULT is raising an exception:
      error_msg = 'from_means (%s) should be one of the following values ' + self.get_values_for_from_means()
      raise ValueError(error_msg)

    :return:
    '''
    if self.to_means == self.EACH_N_DAYS_TARGET_DICTFILE:
      return
    elif self.to_means == self.EACH_N_DAYS_TARGET_JSONFILE:
      return
    elif self.to_means == self.EACH_N_DAYS_TARGET_DB:
      return
    else:
      self.to_means = self.EACH_N_DAYS_TARGET_DEFAULT

  def fillin_instance_dictlist(self):
    '''

    :return:
    '''
    if self.from_means == self.EACH_N_DAYS_ORIGIN_DICTFILE:
      self.read_from_dictfile_each_n_days_into_instancedictlist()
    elif self.from_means == self.EACH_N_DAYS_ORIGIN_JSONFILE:
      self.read_from_jsonfile_each_n_days_into_instancedictlist()
    elif self.from_means == self.EACH_N_DAYS_ORIGIN_DB:
      self.read_from_db_each_n_days_into_instancedictlist()

  def read_from_dictfile_each_n_days_into_instancedictlist(self):
    self.instance_dictlist = StaticEachNDays.read_from_dictfile_each_n_days_n_return_dictlist()

  def read_from_jsonfile_each_n_days_into_instancedictlist(self):
    self.instance_dictlist = StaticEachNDays.read_from_jsonfile_each_n_days_n_return_dictlist()

  def read_from_db_each_n_days_into_instancedictlist(self):
    self.instance_dictlist = StaticEachNDays.read_from_db_each_n_days_n_return_dictlist()

  def transpose_instance_dictlist(self):
    if self.to_means == self.EACH_N_DAYS_TARGET_DICTFILE:
      self.write_to_dictfile_each_n_days_dictlist()
    elif self.to_means == self.EACH_N_DAYS_TARGET_JSONFILE:
      self.write_to_jsonfile_each_n_days_dictlist()
    elif self.to_means == self.EACH_N_DAYS_TARGET_DB:
      self.write_to_db_each_n_days_dictlist()

  def write_to_dictfile_each_n_days_dictlist(self, filename=None):
    was_file_written = StaticEachNDays.write_to_dictfile_each_n_days_from_dictlist(filename, self.instance_dictlist)
    return was_file_written

  def write_to_jsonfile_each_n_days_dictlist(self):
    was_file_written = StaticEachNDays.write_to_jsonfile_each_n_days_from_dictlist(None, self.instance_dictlist)
    return was_file_written

  def write_to_db_each_n_days_dictlist(self):
    was_file_written = StaticEachNDays.write_to_db_each_n_days_from_dictlist(self.instance_dictlist)
    return was_file_written

  def analyze_equality_from_to_means_recsize(self):
    self.fillin_instance_dictlist()
    from_recsize = len(self.instance_dictlist)
    print ('ORIGIN_DICTFILE has', from_recsize, 'records')
    # back up self.from_means because to_means will reuse its fillin() method
    from_means_backup = self.from_means
    to_means_backup = self.to_means
    self.from_means = self.to_means
    self.to_means = None # just in case to avoid another instance to run
    self.fillin_instance_dictlist()
    from_nnames = list(map(lambda e : e['nname'], self.instance_dictlist))
    to_recsize = len(self.instance_dictlist)
    print ('TARGET_DICTFILE has', to_recsize, 'records')
    to_nnames = list(map(lambda e : e['nname'], self.instance_dictlist))
    # if from_recsize != to_recsize:
    print ('from_nnames')
    print (from_nnames)
    print ('to_nnames')
    print (to_nnames)
    # clean up from_nnames
    missing_from, missing_to = collfs.return_cross_missing_elements_from_l1_l2(from_nnames, to_nnames)
    print ('missing_from', missing_from)
    print('missing_to', missing_to)

    # empty dictlist and restore original values
    self.instance_dictlist = []
    self.from_means = from_means_backup
    self.from_means = to_means_backup


  def sync_means(self):
    '''
    This is the Class' processor method, ie, from a client caller,
      after instanciated an object, it suffices to call this method
      for a sync'ing to happen (json to db, db to json, dictfile to json etc.)
    :return:
    '''
    self.instance_dictlist = []
    self.fillin_instance_dictlist()
    if len(self.instance_dictlist) == 0:
      print ('Nothing to sync: len(instance_dictlist) is 0')
      return
    self.transpose_instance_dictlist()

  def __str__(self):
    outstr = 'EachNDaysForDownloadSyncer Object\n'
    outstr += '  from_means = %s, to_means = %s\n' %(self.from_means, self.to_means)
    outstr += str(self.instance_dictlist)
    return outstr

def test_videos_per_day():
  session = Session()
  ytchannel = session.query(samodels.YTChannelSA). \
    filter(samodels.YTChannelSA.ytchannelid=='ueduardoamoreira'). \
    first()
  print(ytchannel)
  print('get_videos_per_day', ytchannel.get_videos_per_day())
  session.close()

def process():
  # StaticEachNDays.show_dowloadables_at_moment()
  from_means = EachNDaysForDownloadSyncer.EACH_N_DAYS_ORIGIN_DICTFILE
  to_means = EachNDaysForDownloadSyncer.EACH_N_DAYS_TARGET_DB
  syncer = EachNDaysForDownloadSyncer(from_means, to_means)
  syncer.sync_means()
  print ('syncer.sync_means()')
  print (syncer)

if __name__ == '__main__':
  process()
