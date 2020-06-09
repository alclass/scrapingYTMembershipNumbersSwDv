#!/usr/bin/python3
import copy, datetime, os
import fs.datefunctions.datefs as dtfs
import fs.filefunctions.pathfunctions as pathfs
import fs.textfunctions.regexp_helpers as regexp

lambdaentryhashtmlext  = lambda word : pathfs.does_filename_have_ext_from_extlist(word, extlist=['htm', 'html'])

class InvalidNamedHtmlOnFolder(ValueError):
  '''
  A helper exception-class that is used from some points below
  '''
  pass

class HtmlInDateFolder:

  def __init__(self, filename):
    self.filename = filename
    self.verify_filename()
    # properties derivable from filename and instanced, ie, built once:
    self._refdate = None
    self._sname = None
    self._ytchannelid = None
    self.filename_is_out_of_convention = False
    self.instanciate_derivable()

  def verify_filename(self):
    if self.filename is None:
      error_msg = 'Error: HtmlInDateFolder received parameter filename as None'
      raise ValueError(error_msg)
    if os.sep in self.filename: # filename can not have os.sep in it
      _, self.filename = os.path.split(self.filename)

  def instanciate_derivable(self):
    '''
    # properties derivable from filename and not-instanced, ie, built once are:
      refdate, sname and ytchannelid
    Obs: it suffices to issue one of them that the others are instanced too

    # properties derivable from filename and not-instanced, ie, built per request:
    # => file_abspath
    # => foldername
    # => folder_abspath
    :return:
    '''
    _ = self._ytchannelid

  def set_date_sname_n_ytchannelid(self):
    name_without_ext, _ = os.path.splitext(self.filename)
    strdate = name_without_ext[:10]
    self._refdate = dtfs.get_refdate_from_strdate(strdate)
    ytchannelid = regexp.find_ytchannelid_within_brackets_in_filename(name_without_ext)
    if ytchannelid is None:
      self.filename_is_out_of_convention = True
      return
      # error_msg = 'Error: datedhtml could not find ytchannelid (%s)' %(self.filename) # do not use str(self) here for it enters an infinite recursion
      # raise InvalidNamedHtmlOnFolder(error_msg)
    ytchannelid = ytchannelid.lstrip('[').rstrip(']')
    self._ytchannelid = ytchannelid
    sname = name_without_ext[11: -(len(ytchannelid)+2)] # plus 2 is for [] (brackets)
    _sname = sname.strip(' ')
    if len(_sname) > 10:
      error_msg = 'Error: when trying to extract sname (%s) from filename (%s) it came out bigger than 10 characters.' %(sname, self.filename)
      raise ValueError(error_msg)
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

  @property
  def infodate(self):
    return self.refdate

  # derivable : foldername
  @property
  def foldername(self):
    '''
    This is 2nd level (and last) foldername
    :return:
    '''
    if self.refdate is None:
      error_msg = 'Error: HtmlInDateFolder has refdate as None; refdate is fundamental for knowing foldername nad folderpath.'
      raise InvalidNamedHtmlOnFolder(error_msg)
      # return None
    try:
      yyyymmdd = str(self.refdate)
      return yyyymmdd
    except IndexError:
      pass
    return None

  @property
  def foldername_level1(self):
    '''
    This is 2nd level (and last) foldername
    :return:
    '''
    if self.refdate is None:
      error_msg = 'Error: HtmlInDateFolder has refdate as None; refdate is fundamental for knowing foldername nad folderpath.'
      raise InvalidNamedHtmlOnFolder(error_msg)
      # return None
    try:
      yyyymm = str(self.refdate)[:7]
      return yyyymm
    except IndexError:
      pass
    return None

  # derivable : folder_abspath
  @property
  def folder_abspath(self):
    '''
      folder_abspath is level2_abspath
    :return:
    '''
    basedir_abspath = pathfs.get_ytvideo_htmlfiles_baseabsdir()
    if self.foldername is None:
      return None
    level1_abspath = os.path.join(basedir_abspath, self.foldername_level1)
    if not os.path.isdir(level1_abspath):
      os.makedirs(level1_abspath)
    level2_abspath = os.path.join(level1_abspath, self.foldername)
    if not os.path.isdir(level2_abspath):
      os.makedirs(level2_abspath)
    return level2_abspath

  # derivable : file_abspath
  @property
  def file_abspath(self):
    if self.folder_abspath is None:
      return None
    return os.path.join(self.folder_abspath, self.filename)

  def asdict(self):
    asdict = {}
    asdict['filename'] = self.filename
    asdict['refdate']  = self.refdate
    asdict['sname']    = self.sname
    asdict['ytchannelid'] = self.ytchannelid
    asdict['foldername']  = self.foldername
    asdict['folder_abspath'] = self.folder_abspath
    asdict['file_abspath']   = self.file_abspath
    return asdict

  def __str__(self):
    outstr = '''HtmlInDateFolder:
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

  def __init__(self, dateini=None, datefim=None):
    self.dateini = None
    self.datefim = None
    self.datepointer = None
    self.init_dates(dateini, datefim)
    self.files_on_current_folder = []
    self.n_of_htmls_processed_day_by_day = []
    # self.traverse()

  def init_dates(self, dateini=None, datefim=None):
    '''
    Conditions:
      1) if ini is greater than fim, an exception (error) will be raised;
      2) if fim is greater than today, an exception (error) will also be raised;
      3) if a date not in format yyyy-mm-dd is entered, an exception (error) will be raised;
      4) if a wrong date is entered, an exception (error) will also be raised.

    :param dateini:
    :param datefim:
    :return:
    '''
    if dateini is None and datefim is None:
      self.dateini = dtfs.return_refdate_as_datetimedate_or_today()
      self.datefim = dtfs.return_refdate_as_datetimedate_or_today()
    elif dateini is None:
      rdatefim = dtfs.get_refdate_from_strdate_or_None(datefim)
      if rdatefim is None:
        error_msg = 'parameter datefim (%s) is an invalid date. Please, retry with a valid date.' %rdatefim
        raise ValueError(error_msg)
      self.datefim = rdatefim
      self.dateini = copy.copy(rdatefim)
    elif datefim is None:
      rdateini = dtfs.get_refdate_from_strdate_or_None(dateini)
      if rdateini is None:
        error_msg = 'parameter dateini (%s) is an invalid date. Please, retry with a valid date.' %rdateini
        raise ValueError(error_msg)
      self.dateini = rdateini
      self.datefim = copy.copy(rdateini)
    else:
      rdateini = dtfs.get_refdate_from_strdate_or_None(dateini)
      if rdateini is None:
        error_msg = 'parameter dateini (%s) is an invalid date. Please, retry with a valid date.' %rdateini
        raise ValueError(error_msg)
      self.dateini = rdateini
      rdatefim = dtfs.get_refdate_from_strdate_or_None(datefim)
      if rdatefim is None:
        error_msg = 'parameter datefim (%s) is an invalid date. Please, retry with a valid date.' %rdatefim
        raise ValueError(error_msg)
      self.datefim = rdatefim

    today = datetime.date.today()
    if self.datefim > today:
      error_msg = 'Error: datafim is greater than today: self.datefim (%s) > today (%s). Please, correct datafim and retry.' %(self.dateini, self.datefim)
      raise ValueError(error_msg)
    if self.dateini > self.datefim:
      error_msg = 'Error: dataini is greater than datafim: self.dateini (%s) > self.datefim (%s). Please, invert them and retry.' %(self.dateini, self.datefim)
      raise ValueError(error_msg)
    self.datepointer = copy.copy(self.dateini)

  def fill_in_current_folder(self):
    folder_abspath = pathfs.get_level2_folder_abspath_from_refdate(self.datepointer)
    if not os.path.isdir(folder_abspath):
      self.files_on_current_folder = []
      return
    self.files_on_current_folder = os.listdir(folder_abspath)
    self.files_on_current_folder = list(filter(lambdaentryhashtmlext, self.files_on_current_folder))

  def traverse(self):
    while self.datepointer <= self.datefim:
      self.fill_in_current_folder()
      if len(self.files_on_current_folder) == 0:
        self.datepointer = self.datepointer + datetime.timedelta(days=1)
        continue
      n_html_files = len(self.files_on_current_folder)
      self.n_of_htmls_processed_day_by_day.append(n_html_files)
      while len(self.files_on_current_folder) > 0:
        popped_filename = self.files_on_current_folder.pop()
        # print('popped_filename', popped_filename)
        htmlfileobj = HtmlInDateFolder(popped_filename)
        if htmlfileobj.filename_is_out_of_convention:
          continue
        yield htmlfileobj
      self.datepointer = self.datepointer + datetime.timedelta(days=1)
    print ('Traverse is finished')

    # to adhoc-test if range works with datetime
    # for i, datenamedfolder in enumerate(range(self.dateini, self.datefim)):
    total = 0
    for i, n_of_htmls_processed_day_by_day in enumerate(self.n_of_htmls_processed_day_by_day):
      datenamedfolder = self.dateini + datetime.timedelta(days=i)
      current_n = self.n_of_htmls_processed_day_by_day[i]
      print (datenamedfolder, 'with', current_n)
      total += current_n
    print('Total of HTML files:', sum(self.n_of_htmls_processed_day_by_day), '/', total)
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
  traversor = DatedHtmlsTraversor('2020-06-03', None)
  print('traversor', traversor)
  for datedhtml in traversor.traverse():
    print(datedhtml)

def process():
  '''
    adhoc_test's are found in adhoctasks.fs.autofind_adhoctests.py
  :return:
  '''
  adhoc_test()

if __name__ == '__main__':
  process()
