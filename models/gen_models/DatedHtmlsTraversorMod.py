#!/usr/bin/python3
import copy, datetime, os
import fs.datefunctions.datefs as dtfs
import fs.filefunctions.pathfunctions as pathfs
from models.gen_models.HtmlInDateFolderMod import HtmlInDateFolder
# import fs.textfunctions.regexp_helpers as regexp

lambdaentryhashtmlext  = lambda word : pathfs.does_filename_have_ext_from_extlist(word, extlist=['htm', 'html'])

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
      rdatefim = dtfs.get_refdate_from_strdate_or_none(datefim)
      if rdatefim is None:
        error_msg = 'parameter datefim (%s) is an invalid date. Please, retry with a valid date.' %rdatefim
        raise ValueError(error_msg)
      self.datefim = rdatefim
      self.dateini = copy.copy(rdatefim)
    elif datefim is None:
      rdateini = dtfs.get_refdate_from_strdate_or_none(dateini)
      if rdateini is None:
        error_msg = 'parameter dateini (%s) is an invalid date. Please, retry with a valid date.' %rdateini
        raise ValueError(error_msg)
      self.dateini = rdateini
      self.datefim = copy.copy(rdateini)
    else:
      rdateini = dtfs.get_refdate_from_strdate_or_none(dateini)
      if rdateini is None:
        error_msg = 'parameter dateini (%s) is an invalid date. Please, retry with a valid date.' %rdateini
        raise ValueError(error_msg)
      self.dateini = rdateini
      rdatefim = dtfs.get_refdate_from_strdate_or_none(datefim)
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
