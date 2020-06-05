#!/usr/bin/python3
import copy, datetime, os, re
import fs.datefunctions.datefs as dtfs
import fs.filefunctions.pathfunctions as pathfs
import fs.textfunctions.regexp_helpers as regexp
from collections import OrderedDict

lambdajoinabspath      = lambda path_n_entry : os.path.join(path_n_entry[0], path_n_entry[1])
lambdaentryisfolder    = lambda ppath : os.path.isdir(ppath)
lambdastrformdate      = lambda word : dtfs.str_is_inversed_date(word)
lambdafilterinyyyymm   = lambda word : dtfs.str_is_inversed_year_month(word)
lambdafilterinyyyymmdd = lambda word : dtfs.str_is_inversed_date(word)

def find_1stlevel_yyyymm_dir_foldernames(level1abspath):
  '''
  First level folder entries that are named as yyyy-mm

  :return:
  '''
  entries = os.listdir(level1abspath)
  entries = list(filter(lambdafilterinyyyymm, entries))
  return entries

def find_1stlevel_yyyymm_dir_abspaths():
  level1abspath = pathfs.get_ytvideo_htmlfiles_baseabsdir()
  entries = find_1stlevel_yyyymm_dir_foldernames(level1abspath)
  if len(entries) == 0:
    return []
  zippedforlambda = list(zip([level1abspath]*len(entries), entries))
  abspath_entries  = list(map(lambdajoinabspath, zippedforlambda))
  yyyymm_level1_abspath_entries = list(filter(lambdaentryisfolder, abspath_entries))
  return yyyymm_level1_abspath_entries

def find_2ndlevel_yyyymmdd_dir_abspaths():
  yyyymm_level1_abspath_entries = find_1stlevel_yyyymm_dir_abspaths()
  total_yyyymmdd_level2abspathentries = []
  for level2abspathentry in yyyymm_level1_abspath_entries:
    level2entries = os.listdir(level2abspathentry)
    level2entries = list(filter(lambdafilterinyyyymmdd, level2entries))
    if len(level2entries) == 0:
      continue
    zippedforlambda = zip([level2abspathentry]*len(level2entries), level2entries)
    level2abspathentries = list(map(lambdajoinabspath, zippedforlambda))
    level2abspathentries = list(filter(lambdaentryisfolder, level2abspathentries))
    total_yyyymmdd_level2abspathentries += level2abspathentries
  return total_yyyymmdd_level2abspathentries

def find_yyyymmdd_level2_foldernames():
  total_level2_abspath_entries = find_2ndlevel_yyyymmdd_dir_abspaths()
  total_yyyymmdd_foldernames =  []
  for pathentry in total_level2_abspath_entries:
    _, strdate = os.path.split(pathentry)
    total_yyyymmdd_foldernames.append(strdate)
  return total_yyyymmdd_foldernames

def find_dateini_n_dateend_thru_yyyymmdd_level2_folders():
  total_yyyymmdd_foldernames = find_yyyymmdd_level2_foldernames()
  if len(total_yyyymmdd_foldernames) == 0:
    return (None, None)
  total_yyyymmdd_foldernames = sorted(total_yyyymmdd_foldernames)
  oldest = total_yyyymmdd_foldernames[0]
  newest = total_yyyymmdd_foldernames[-1]
  oldestdate = dtfs.get_refdate_from_strdate(oldest)
  newestdate = dtfs.get_refdate_from_strdate(newest)
  # the if below should never happen considering filter tasks above
  '''
  if oldestdate is None or newestdate is None:
    return (None, None)
  '''
  return (oldestdate, newestdate)

def get_ordered_dict_with_dates_n_abspaths():
  level2_yyyymmdd_dir_abspaths = find_2ndlevel_yyyymmdd_dir_abspaths()
  yyyymmdd_list = []
  dates_n_paths_dict = {}
  for yyyymmdd_dir_abspath in level2_yyyymmdd_dir_abspaths:
    _, strdate = os.path.split(yyyymmdd_dir_abspath)
    yyyymmdd_list.append(strdate)
    dates_n_paths_dict[strdate] = yyyymmdd_dir_abspath
  yyyymmdd_list = sorted(yyyymmdd_list)
  dates_n_paths_od = OrderedDict()
  for yyyymmdd in yyyymmdd_list:
    dates_n_paths_od[yyyymmdd] = dates_n_paths_dict[yyyymmdd]
  return dates_n_paths_od

class HtmlInDateFolder:

  def __init__(self, filename):
    self.filename = filename
    # properties derivable from filename and instanced, ie, built once:
    self._refdate = None
    self._sname  = None
    self._ytchannelid = None
    # properties derivable from filename and not-instanced, ie, built per request:
    # => file_abspath
    # => foldername
    # => folder_abspath

  def set_date_sname_n_ytchannelid(self):
    name_without_ext, _ = os.path.splitext(self.filename)
    ytchannelid = regexp.find_ytchannelid_within_brackets_in_filename(name_without_ext)
    if ytchannelid is None:
      return
    self._ytchannelid = ytchannelid
    strdate = name_without_ext[:10]
    self._refdate = dtfs.get_refdate_from_strdate(strdate)
    sname = name_without_ext[11: -(len(ytchannelid)+2-1)] # plus 2 is for [] (brackets)
    sname = sname.strip(' ')
    if len(sname) > 10:
      error_msg = 'Error: when trying to extract sname (%s) from filename (%s) it came out bigger than 10 characters.' %(sname, self.filename)
      raise ValueError
    self._sname = sname

  @property
  def sname(self):
    if self._sname is None:
      self.set_date_sname_n_ytchannelid()
    return self._sname

  @property
  def ytchannelid(self):
    if self._ytchannelid is None:
      self.set_date_sname_n_ytchannelid()
    return self._ytchannelid

  @property
  def refdate(self):
    if self._refdate is None:
      self.set_date_sname_n_ytchannelid()
    return self._refdate

  # derivable : foldername
  @property
  def foldername(self):
    if self.refdate is None:
      return None
    try:
      yyyymm = str(self.refdate)[:7]
      return yyyymm
    except IndexError:
      pass
    return None

  # derivable : folder_abspath
  @property
  def folder_abspath(self):
    basedir_abspath = pathfs.get_ytvideo_htmlfiles_baseabsdir()
    if self.foldername is None:
      return None
    return os.path.join(basedir_abspath, self.foldername)

  # derivable : file_abspath
  @property
  def file_abspath(self):
    return os.path.join(self.folder_abspath, self.filename)

  def asdict(self):
    asdict = {}
    asdict['filename'] = self.filename
    asdict['refdate'] = self.refdate
    asdict['sname'] = self.sname
    asdict['ytchannelid'] = self.ytchannelid
    asdict['foldername'] = self.foldername
    asdict['folder_abspath'] = self.folder_abspath
    asdict['file_abspath'] = self.file_abspath
    return asdict

  def __str__(self):
    outstr = '''DateHtmlsTraversor:
  filename = %(filename)s
  refdate  = %(refdate)s 
  sname    = %(sname)s 
  ytchannelid    = %(ytchannelid)s
  foldername     = %(foldername)s
  folder_abspath = %(folder_abspath)s
  file_abspath   = %(file_abspath)s 
''' %self.asdict()
    return outstr

class DatedHtmlsTraversor:

  def __init__(self, dateini, datefim):
    self.dateini = dtfs.get_refdate_from_strdate(dateini)
    self.datefim = dtfs.get_refdate_from_strdate(datefim)
    self.datepointer = copy.copy(self.dateini)
    self.files_on_current_folder = []
    # self.fill_in_current_folder()
    self.traverse()

  def fill_in_current_folder(self):
    folder_abspath = pathfs.get_level2_folder_abspath_from_refdate(self.datepointer)
    if not os.path.isdir(folder_abspath):
      self.files_on_current_folder = []
      return
    self.files_on_current_folder = os.listdir()

  def traverse(self):
    print('traverse datepointer =', self.datepointer)
    while self.datepointer <= self.datefim:
      self.fill_in_current_folder()
      if len(self.files_on_current_folder) == 0:
        self.datepointer = self.datepointer + datetime.timedelta(days=1)
        continue
      while len(self.files_on_current_folder) > 0:
        popped_filename = self.files_on_current_folder.pop()
        print('popped_filename', popped_filename)
        htmlfileobj = HtmlInDateFolder(popped_filename)
        yield htmlfileobj
      self.datepointer = self.datepointer + datetime.timedelta(days=1)
    print ('Traverse is finished')
    return None

  def asdict(self):
    asdict = {}
    asdict['dateini'] = self.dateini
    asdict['datefim'] = self.datefim
    return asdict

  def __str__(self):
    outstr = '''DatedHtmlsTraversor:
  dateini  = %(dateini)s 
  dateini  = %(datefim)s 
''' % self.asdict()
    return outstr

def adhoc_test():
  tupl = find_dateini_n_dateend_thru_yyyymmdd_level2_folders()
  level1abspathentries = find_1stlevel_yyyymm_dir_abspaths()
  print('level1abspathentries', level1abspathentries)
  print (tupl)
  dateini_n_dateend = find_dateini_n_dateend_thru_yyyymmdd_level2_folders()
  print ('dateini_n_dateend', dateini_n_dateend)

def test1():
  # lambdajoinabspath = lambda abspath, entry: os.path.join(abspath, entry)
  abspath = '/this/path/is/test'
  entries = ['adfa', 'mkmfkgçsmf', 'oiopipo']
  zipped = list(zip([abspath]*len(entries), entries))
  print ('zipped', zipped)
  absentries = list(map(lambdajoinabspath, zipped)) # abspath, entries
  print('absentries via map-lambda', absentries)
  testpath = lambdajoinabspath ((abspath, 'adfa2'))
  print('testpath', testpath)
  absentries = []
  for e in entries:
    absentry = os.path.join(abspath, e)
    absentries.append(absentry)
  print('absentries via for-loop', absentries)

def test_HtmlInDateFolder():
  '''
  filename = '2020-05-22 Eduardo Mo [ueduardoamoreira].html'
  dht = HtmlInDateFolder(filename)
  print('HtmlInDateFolder(filename)', dht)
  '''
  print ("DatedHtmlsTraversor('2020-05-22', '2020-06-05')")
  traversor = DatedHtmlsTraversor('2020-05-22', '2020-06-05')
  print(traversor)
  for obj in traversor.traverse():
    print (obj)

def process():
  test_HtmlInDateFolder()
  # test1()
  # adhoc_test()

if __name__ == '__main__':
  process()