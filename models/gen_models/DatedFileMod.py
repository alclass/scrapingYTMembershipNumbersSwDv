#!/usr/bin/python3
import hashlib, os, shutil
import config
import fs.datefunctions.datefs as dtfs
import fs.filefunctions.pathfunctions as pathfs
import fs.db.sqlalchdb.sqlalchemy_conn as saconn
from models.sa_models.ytchannelsubscribers_samodels import TreeBaseAbsPath
from models.sa_models.ytchannelsubscribers_samodels import NewsArticlesSA

def get_abspaths_from_config():
  '''
    Returns the abspaths that are registered in config.py
  :return:
  '''
  KEY_FOR_DIRS = config.BASE_ABSPATHS_KEYS[config.NEWSARTICLES_BASEFOLDERNAME_AS_KEY] # supposed to be 'NEWSPAPERS_BASE_ABSPATHS'
  BASEDIRS = eval('config.' + KEY_FOR_DIRS) # it's like config.NEWSPAPERS_BASE_ABSPATHS
  return BASEDIRS

def get_newsarticles_base_abspath_from_cfg_lookup_strict(lookup_order, strict=True):
  base_abspaths = get_abspaths_from_config()
  if lookup_order is None or type(lookup_order) != int:
    error_msg = 'Error: The lookup_order (%s) does not exist in get_newsarticles_base_abspath_from_cfg_lookup_strict()' %str(lookup_order)
    raise ValueError(error_msg)
  try:
    idx = lookup_order - 1
    tpath = base_abspaths[idx]
    if os.path.isdir(tpath):
      base_abspath = tpath
      return base_abspath
  except IndexError:
    pass
  if strict:
    error_msg = 'Error: The lookup_order (%s) does not exist in get_newsarticles_base_abspath_from_cfg_lookup_strict()' %str(lookup_order)
    raise ValueError(error_msg)
  return None

def get_newsarticles_base_abspath_from_cfg(lookup_order=None):
  '''
    Returns either the abspath that is the lookup_order-th, if it is config.py and exists in OS,
      or another one in config.py that exists in OS
    Will return None if no abspaths exist or if config.py has None of them
  :param lookup_order:
  :return:
  '''
  base_abspath = None
  base_abspaths = get_abspaths_from_config()
  if lookup_order is not None and type(lookup_order) == int:
    base_abspath = get_newsarticles_base_abspath_from_cfg_lookup_strict(lookup_order, strict=False)
    if base_abspath is not None:
      return base_abspath
  for tpath in base_abspaths:
    if os.path.isdir(tpath):
      base_abspath = tpath
      break
  return base_abspath

def get_abspaths_from_db():
  base_abspaths = []
  session = saconn.Session()
  newsarticles_basefoldername_as_key = get_newsarticles_basefoldername_as_key()
  treebase_abspath_recs = session.query(TreeBaseAbsPath). \
    filter(TreeBaseAbsPath.app_tree_strkey==newsarticles_basefoldername_as_key). \
    order_by(TreeBaseAbsPath.lookup_order). \
    all()
  for treebase_abspath_rec in treebase_abspath_recs:
    base_abspath = treebase_abspath_rec.abspath
    base_abspaths.append(base_abspath)
  session.close()
  return base_abspaths

def get_newsarticles_basefoldername_as_key():
  try:
    newsarticles_basefoldername_as_key = config.NEWSARTICLES_BASEFOLDERNAME_AS_KEY
  except AttributeError as e:
    error_msg = 'Missing parameter NEWSARTICLES_BASEFOLDERNAME_AS_KEY (%s) in config.py (cannot continue to find base_abspath for news articles): '%newsarticles_basefoldername_as_key + str(e)
    raise AttributeError(error_msg)
  return newsarticles_basefoldername_as_key

def get_newsarticles_base_abspath_from_db_lookup_strict(lookup_order=None, strict=True):
  base_abspath = None
  session = saconn.Session()
  newsarticles_basefoldername_as_key = get_newsarticles_basefoldername_as_key()
  treebase_abspath_rec = session.query(TreeBaseAbsPath). \
    filter(TreeBaseAbsPath.app_tree_strkey==newsarticles_basefoldername_as_key). \
    filter(TreeBaseAbsPath.lookup_order == lookup_order). \
    first()
  if treebase_abspath_rec:
    if os.path.isdir(treebase_abspath_rec.abspath):
      base_abspath = treebase_abspath_rec.abspath
  session.close()
  if base_abspath is None and strict:
    error_msg = 'Error: The lookup_order (%s) does not exist in get_newsarticles_base_abspath_from_db_lookup_strict()' %str(lookup_order)
    raise ValueError(error_msg)
  return base_abspath

def get_newsarticles_base_abspath_from_db(lookup_order=None):
  if lookup_order is None or type(lookup_order) != int:
    lookup_order = 1
  base_abspath = get_newsarticles_base_abspath_from_db_lookup_strict(lookup_order, strict=False)
  if base_abspath is None:
    # try first available, ie, one that exists in OS
    session = saconn.Session()
    newsarticles_basefoldername_as_key = get_newsarticles_basefoldername_as_key()
    treebase_abspath_recs = session.query(TreeBaseAbsPath). \
      filter(TreeBaseAbsPath.app_tree_strkey==newsarticles_basefoldername_as_key). \
      order_by(TreeBaseAbsPath.lookup_order). \
      all()
    for treebase_abspath_rec in treebase_abspath_recs:
      if os.path.isdir(treebase_abspath_rec.abspath):
        base_abspath = treebase_abspath_rec.abspath
        break
    session.close()
  return base_abspath

def get_newsarticles_base_abspath_from_db_or_cfg(lookup_order=None):
  base_abspath = get_newsarticles_base_abspath_from_db(lookup_order)
  if base_abspath is None or not os.path.isdir(base_abspath):
    base_abspath = get_newsarticles_base_abspath_from_cfg(lookup_order)
  if base_abspath is None or not os.path.isdir(base_abspath):
    error_msg = 'Could not find base_abspath (cannot continue to fetch/get news articles):: in get_newsarticles_base_abspath_from_db_or_cfg()'
    raise AttributeError(error_msg)
  return base_abspath

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
    refdate = dtfs.get_refdate_from_strdate_or_none(strdate)
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

  def __init__(self, base_abspath, fromplace_abspath, filename):
    super().__init__(base_abspath, filename)
    self.fromplace_abspath = fromplace_abspath

  def move(self):
    if len(self.filename) < 11:
      return False
    source_abspath = os.path.join(self.fromplace_abspath, self.filename)
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

class HTMLDatedFileInsertDB(DatedFile):

  def __init__(self, base_abspath, filename):
    super().__init__(base_abspath, filename)
    if pathfs.is_htmldatedfilename_under_convention(filename):
      error_msg = 'In init HTMLDatedFileInsertDB filename %s is not under convention' %filename
      raise ValueError(error_msg)

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
    print ("Addimg ", newsarticle)
    session.add(newsarticle)
    session.commit()
    session.close()
    return True

def adhoc_test():
  lookup_order = 'blah'
  base_abspath = get_newsarticles_base_abspath_from_db(lookup_order=lookup_order)
  print ('db lookup_order =', lookup_order, '; base_abspath =', base_abspath)
  base_abspath = get_newsarticles_base_abspath_from_cfg(lookup_order=lookup_order)
  print ('cfg lookup_order =', lookup_order, '; base_abspath =', base_abspath)
  paths = get_abspaths_from_config()
  print ('paths from cfg =', paths)
  paths = get_abspaths_from_db()
  print ('paths from db =', paths)
  lookup_order = 2
  base_abspath = get_newsarticles_base_abspath_from_db_lookup_strict(lookup_order)
  print ('strict db lookup_order =', lookup_order, '; base_abspath =', base_abspath)
  lookup_order = 2
  #base_abspath = get_newsarticles_base_abspath_from_db_lookup_strict(lookup_order)
  #print ('strict db lookup_order =', lookup_order, '; base_abspath =', base_abspath)
  base_abspath = get_newsarticles_base_abspath_from_cfg_lookup_strict(lookup_order)
  print ('strict cfg lookup_order =', lookup_order, '; base_abspath =', base_abspath)
  lookup_order = 'bla'
  base_abspath = get_newsarticles_base_abspath_from_cfg(lookup_order)
  print ('cfg lookup_order =', lookup_order, '; base_abspath =', base_abspath)
  base_abspath = get_newsarticles_base_abspath_from_db(lookup_order)
  print ('db lookup_order =', lookup_order, '; base_abspath =', base_abspath)
  base_abspath = get_newsarticles_base_abspath_from_db_or_cfg()
  print ('get_newsarticles_base_abspath_from_db_or_cfg() =', base_abspath)

def process():
  adhoc_test()

if __name__ == '__main__':
  process()
