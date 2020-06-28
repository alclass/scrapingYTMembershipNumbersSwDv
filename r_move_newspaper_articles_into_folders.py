#!/usr/bin/python3
import hashlib, os, shutil
import config
import fs.datefunctions.datefs as dtfs
import fs.db.sqlalchdb.sqlalchemy_conn as saconn
from models.sa_models.ytchannelsubscribers_samodels import TreeBaseAbsPath
from models.sa_models.ytchannelsubscribers_samodels import NewsArticlesSA

BASE_FOLDERNAME_AS_KEY = '001_BRA_pol_newspapers'

def get_app_tree_key():
  return BASE_FOLDERNAME_AS_KEY

def get_abspaths_from_config():
  KEY_FOR_DIRS = config.BASE_ABSPATHS_KEYS[get_app_tree_key()] # supposed to be 'NEWSPAPERS_BASE_ABSPATHS'
  BASEDIRS = eval('config.' + KEY_FOR_DIRS) # it's like config.NEWSPAPERS_BASE_ABSPATHS
  return BASEDIRS

def get_abspath_from_config(is_alternative=False):
  KEY_FOR_DIRS = config.BASE_ABSPATHS_KEYS[get_app_tree_key()] # supposed to be 'NEWSPAPERS_BASE_ABSPATHS'
  BASEDIRS = eval('config.' + KEY_FOR_DIRS) # it's like config.NEWSPAPERS_BASE_ABSPATHS
  if is_alternative:
    base_abspath = BASEDIRS[1]
    if not os.path.isdir(base_abspath):
      error_msg = 'Error: base_abspath (%s) does not exist.' %base_abspath
      raise OSError(error_msg)
    return base_abspath
  for basedir in BASEDIRS:
    if os.path.isdir(basedir):
      return basedir
  error_msg = 'Error: base_abspaths (%s) do not exist.' %BASEDIRS
  raise OSError(error_msg)

def get_base_abspath_from_db(is_alternative=False):
  app_tree_key = get_app_tree_key()
  session = saconn.Session()
  dirtree = session.query(TreeBaseAbsPath).filter(TreeBaseAbsPath.app_tree_strkey==app_tree_key).first()
  print(dirtree)
  if not is_alternative:
    abspath = dirtree.abspath
  else:
    abspath = dirtree.alternative_abspath
  session.close()
  return abspath

class DatedFile:
  '''
  This class is parent for classes below (InsertDB & MoveableFile)
  '''

  def __init__(self, base_abspath, filename):
    self.base_abspath = base_abspath
    self.filename     = filename
    self._canon_filefolder_abspath = None
    self._canon_file_abspath = None
    self._refdate = None
    self._sha1 = None

  def set_refdate(self):
    if len(self.filename) < 11:
      error_msg = 'Error: len(self.filename) < 11 (%s) when trying to derive strdate.' %str(self.filename)
      raise ValueError(error_msg)
    strdate = self.filename[:10]
    refdate = dtfs.get_refdate_from_strdate_or_None(strdate)
    if refdate is None:
      error_msg = 'Error: refdate %s has not been found; filename %s.' %(str(strdate), self.filename)
      raise ValueError(error_msg)
    self._refdate = refdate

  @property
  def refdate(self):
    if self._refdate is None:
      self.set_refdate() # exception will be raised if it's not able to set it
    return self._refdate

  @property
  def strdate(self):
    return str(self.refdate)

  def set_canon_folderabspath(self):
    '''
      The DatedFolder scheme is the following:
        1) top is base_abspath (given to __init__ constructor)
        2) subsequent folders are:
          abspath/yyyy/yyyy-mm/yyyy-mm-dd/
        This convention above is the "canonical" (canon) abspath
    :return:
    '''
    # 1st level (mount yyyy on top of base_abspath)
    stryear = self.strdate[:4] # eg returns 2020 from 2020-05-01
    level1 = os.path.join(self.base_abspath, stryear)
    # 2nd level (mount yyyy-mm on top of base_abspath/yyyy)
    stryearmonth = self.strdate[:7] # eg returns 2020-05 from 2020-05-01
    level2 = os.path.join(level1, stryearmonth)
    # 3rd level (mount yyyy-mm-dd on top of base_abspath/yyyy/yyyy-mm)
    level3 = os.path.join(level2, self.strdate)
    if not os.path.isdir(level3):
      os.makedirs(level3)
    self._canon_filefolder_abspath = level3

  @property
  def canon_filefolder_abspath(self):
    '''
    :return:
    '''
    if self._canon_filefolder_abspath is None:
      self.set_canon_folderabspath()
    return self._canon_filefolder_abspath

  @property
  def canon_file_abspath(self):
    '''
    This is the "should be" position derived from base abspath, date-related folders, and filename,
      because one conceptual use-case is to create it later on, os.path.isfile() is not applied
    :return:
    '''
    if self._canon_file_abspath is None:
      self._canon_file_abspath = os.path.join(self.canon_filefolder_abspath, self.filename)
    return self._canon_file_abspath

  def get_n_set_sha1_for_file_on_datedfolder_or_None(self):
    if not os.path.isfile(self.canon_file_abspath):
      error_msg = 'Error: for SHA1, file %s does not exist' %self.canon_file_abspath
      raise ValueError(error_msg)
    m = hashlib.sha1()
    fp = open(self.canon_file_abspath, 'r', encoding='utf8')
    try:
      text = fp.read()
    except UnicodeDecodeError:
      print ('UnicodeDecodeError for', self.filename)
      return None
    m.update(text.encode()) # an encoding parameter is not given, TO-DO research problems of mix encoding, eg. utf8 and latin1
    digest = m.digest()
    self._sha1 = digest
    return digest

  def set_sha1_for_file_on_datedfolder(self):
    if self._sha1 is None:
      _ = self.get_n_set_sha1_for_file_on_datedfolder_or_None()
      if self._sha1 is None:
        error_msg = 'Error: sha1 is None the second time (text probably is not utf8) %s' %self.filename
        raise ValueError(error_msg)
    return self._sha1

  @property
  def sha1(self):
    if self._sha1 is None:
      self.set_sha1_for_file_on_datedfolder()
    return self._sha1

  def __str__(self):
    return '<DatedFile %s>' %self.filename


class MoveableFile(DatedFile):

  def __init__(self, base_abspath, onplace_abspath, filename):
    super().__init__(base_abspath, filename)
    self.onplace_abspath = onplace_abspath

  def move(self):
    if len(self.filename) < 11:
      return False
    source_abspath = os.path.join(self.onplace_abspath, self.filename)
    target_abspath = self.canon_file_abspath
    print ('Moving')
    print ('source', source_abspath)
    print ('target', target_abspath)
    if source_abspath == target_abspath:
      return False
    if os.path.isfile(source_abspath) and not os.path.isfile(target_abspath):
      shutil.move(source_abspath, target_abspath)
      return True
    return False

class InsertDB(DatedFile):

  def __init__(self, base_abspath, filename):
    super().__init__(base_abspath, filename)

  def insert(self):
    shouldbe_abspath = os.path.join(self.canon_filefolder_abspath, self.filename)
    if not os.path.isfile(shouldbe_abspath):
      print ('filename', self.filename, 'is not in folder', shouldbe_abspath)
      return False
    digest = self.get_n_set_sha1_for_file_on_datedfolder_or_None()
    if digest is None:
      return False
    session = saconn.Session()
    newsarticle = session.query(NewsArticlesSA).filter(NewsArticlesSA.sha1==digest).first()
    if newsarticle:
      print ('newsarticle with sha1 %s already in db' %str(digest))
      session.close()
      return False
    newsarticle = NewsArticlesSA()
    newsarticle.title    = self.filename
    newsarticle.filename = self.filename
    newsarticle.sha1 = self.sha1
    newsarticle.publishdate = self.refdate
    newsarticle.tree_id = 1
    print ("Addimg ", newsarticle)
    session.add(newsarticle)
    session.commit()
    session.close()
    return True

def is_filename_under_convention(filename):
  if len(filename) < 11:
    return False
  isNone = dtfs.get_refdate_from_strdate_or_None(filename[:10])
  if isNone is None:
    return False
  _, ext = os.path.splitext(filename)
  if ext not in ['.ht', '.htm', '.html', '.shtml']:
    return False
  return True

def walk_up_tree(is_alternative=False):
  base_abspath = get_base_abspath_from_db(is_alternative);  count = 0; moved = 0; n_insert = 0
  for onplace_abspath, folders, files in os.walk(base_abspath):
    for filename in files:
      if not is_filename_under_convention(filename):
        continue
      count += 1
      print (moved, '/', count, 'MoveableFile')
      mover = MoveableFile(base_abspath, onplace_abspath, filename)
      if mover.move():
        moved += 1
      insertor = InsertDB(base_abspath, filename)
      boolresult = insertor.insert()
      if not boolresult:
        print ('Insertor failed: ', insertor)
      else:
        n_insert += 1
  print (moved, ' moved /', count, str(['.ht','.htm','.html','.shtml']), 'insert', n_insert)

def process():
  walk_up_tree()
  # result = get_abspaths_from_config()
  # print (result)

if __name__ == '__main__':
  process()
