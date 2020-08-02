#!/usr/bin/env python3
"""
  docstring
"""
from collections import OrderedDict
import os
import config
import fs.datefunctions.datefs as dtfs
import fs.filefunctions.pathfunctions as pathfs


def endswith_htmls_n_startswith_date(filename):
  if filename is None:
    return False
  name, ext = os.path.splitext(filename)
  if ext is None or len(ext) == 0:
    return False
  if ext not in config.HTML_EXTLIST:
    return False
  try:
    strdate = name[:10]
  except IndexError:
    return False
  pdate = dtfs.get_refdate_from_strdate_or_none(strdate)
  if pdate is None:
    return False
  return True


def joinabspath_with_tuple(path_n_entry_tuple):
  """
    Former lambda
  :param path_n_entry_tuple:
  :return:
  """
  return os.path.join(path_n_entry_tuple[0], path_n_entry_tuple[1])


def is_entry_a_folder(ppath):
  """
    Former lambda lambdaentryisfolder
  :param ppath:
  :return:
  """
  return os.path.isdir(ppath)


def does_str_form_date(word):
  """
    Former lambda lambdastrformdate & lambdafilterinyyyymmdd
  :param word:
  :return:
  """
  return dtfs.str_is_inversed_date(word)


def is_str_year_slash_month(word):
  """
    Former lambda lambdafilterinyyyymm
    lambdafilterinyyyymm   = lambda word : dtfs.str_is_inversed_year_month(word)

  :param word:
  :return:
  """
  return dtfs.str_is_inversed_year_month(word)


def get_level1folderabspath(pdate=None):
  """

  :param pdate:
  :return:
  """
  refdate = dtfs.return_refdate_as_datetimedate_or_today(pdate)
  level0baseabspath = pathfs.get_ytvideo_htmlfiles_baseabsdir()
  level1foldername = str(refdate)[:7]
  level1folderabspath = os.path.join(level0baseabspath, level1foldername)
  if not os.path.isdir(level1folderabspath):
    os.makedirs(level1folderabspath)
  return level1folderabspath


def does_str_form_yyyydate(word):
  if word is None:
    return False
  strdate = word + '-1-1'
  if dtfs.get_refdate_from_strdate_or_none(strdate):
    return True
  return False


def does_str_form_yyyymmdate(word):
  if word is None:
    return False
  strdate = word + '-1'
  if dtfs.get_refdate_from_strdate_or_none(strdate):
    return True
  return False


def find_1stlevel_yyyy_dir_foldernames(level1abspath=None):
  """
  First level name entries that are named as yyyy-mm:
    obs:
      1) If the baseabsdir does not exist, it is created;
      2) if this dir creation happens, an empty foldername list will return;
      3) it may be empty if even it already existed;
      4) return foldernames are those with the yyyy-mm pattern;
      5) notice that filenames may be returned, the filtering will be done by the caller when paths are joint;

  :return:
  """
  if level1abspath is None:
    level1abspath = pathfs.get_ytvideo_htmlfiles_baseabsdir()
  if not os.path.isdir(level1abspath):
    os.makedirs(level1abspath)
  entries = os.listdir(level1abspath)
  entries = list(filter(does_str_form_yyyydate, entries))
  return entries


def find_0thlevel_dir_abspaths(level0abspath=None):
  """
    The configpath is created if it does not exist. The level0abspath is returned only if it exists.
  :param level0abspath:
  :return:
  """
  if level0abspath is None or not os.path.isdir(level0abspath):
    configpath = pathfs.get_ytvideo_htmlfiles_baseabsdir()
    if not os.path.isdir(configpath):
      os.makedirs(configpath)
    return configpath
  return level0abspath


def find_1stlevel_yyyy_dir_abspaths(plevel0abspath=None):
  """
  First level path entries that are named as yyyy and are directories:
    obs:
      1) this routine used the names returned by find_1stlevel_yyyy_dir_foldernames();
      2) as some names may be files, it filters in only dirpaths;
      3) then returns this dirpath list;

  :return:
  """
  level0abspath = find_0thlevel_dir_abspaths(plevel0abspath)
  entries = find_1stlevel_yyyy_dir_foldernames(level0abspath)
  if len(entries) == 0:
    return []
  zippedforlambda = list(zip([level0abspath]*len(entries), entries))
  abspath_entries = list(map(joinabspath_with_tuple, zippedforlambda))
  yyyy_level1_abspath_entries = list(filter(is_entry_a_folder, abspath_entries))
  return yyyy_level1_abspath_entries


def find_2ndlevel_yyyymm_dir_foldernames(level1abspath=None):
  """
  First level name entries that are named as yyyy-mm:
    obs:
      1) If the baseabsdir does not exist, it is created;
      2) if this dir creation happens, an empty foldername list will return;
      3) it may be empty if even it already existed;
      4) return foldernames are those with the yyyy-mm pattern;
      5) notice that filenames may be returned, the filtering will be done by the caller when paths are joint;

  :return:
  """
  l2abspaths = find_1stlevel_yyyy_dir_abspaths(level1abspath)
  l2foldernames = []
  for l2abspath in l2abspaths:
    entries = os.listdir(l2abspath)
    entries = list(filter(does_str_form_yyyymmdate, entries))
    l2foldernames += entries
  return l2foldernames


def find_2ndlevel_yyyymm_dir_abspaths(level1abspath=None):
  """

  :param level2abspathentry:
  :param level2entries:
  :return:
  """
  l2abspaths = find_1stlevel_yyyy_dir_abspaths(level1abspath)
  l2foldernames = []
  total_l2paths = []
  for l2abspath in l2abspaths:
    entries = os.listdir(l2abspath)
    entries = list(filter(does_str_form_yyyymmdate, entries))
    l2foldernames += entries
    l2paths = []
    for entry in entries:
      l2path = os.path.join(l2abspath, entry)
      l2paths.append(l2path)
    l2paths = list(filter(lambda e: os.path.isdir(e), l2paths))
    total_l2paths += l2paths
  return total_l2paths


def find_3rdlevel_yyyymmdd_dir_abspaths_from_a_2ndlevel(level2abspathentry, level2entries):
  """

  :param level2abspathentry:
  :param level2entries:
  :return:
  """
  level2entries = list(filter(does_str_form_yyyymmdate, level2entries))
  if len(level2entries) == 0:
    return
  zippedforlambda = zip([level2abspathentry]*len(level2entries), level2entries)
  level2_abspath_entries = list(map(joinabspath_with_tuple, zippedforlambda))
  level2_abspath_entries = list(filter(is_entry_a_folder, level2_abspath_entries))
  return level2_abspath_entries


def find_all_3rdlevel_yyyymmdd_dir_abspaths():
  """
  Second level path entries that are named as yyyy-mm-dd and are directories:
    obs:
      1) it takes all paths across all first level directories;

  :return:
  """
  yyyymm_level2_abspath_entries = find_2ndlevel_yyyymm_dir_abspaths()
  total_yyyymmdd_level2abspathentries = []
  for level2_abspath_entry in yyyymm_level2_abspath_entries:
    level2entries = os.listdir(level2_abspath_entry)
    level2_abspath_entries = find_3rdlevel_yyyymmdd_dir_abspaths_from_a_2ndlevel(level2_abspath_entry, level2entries)
    total_yyyymmdd_level2abspathentries += level2_abspath_entries
  return total_yyyymmdd_level2abspathentries


def find_yyyymmdd_level3_foldernames():
  total_level2_abspath_entries = find_2ndlevel_yyyymm_dir_abspaths()
  total_yyyymmdd_foldernames = []
  for pathentry in total_level2_abspath_entries:
    entries = os.listdir(pathentry)
    entries = list(filter(lambda e: dtfs.get_refdate_from_strdate_or_none(e), entries))
    total_yyyymmdd_foldernames += entries
  return total_yyyymmdd_foldernames


def get_ordered_dict_with_dates_n_abspaths():
  """

  :return:
  """
  level3_yyyymmdd_dir_abspaths = find_all_3rdlevel_yyyymmdd_dir_abspaths()
  yyyymmdd_list = []
  dates_n_paths_dict = {}
  for yyyymmdd_dir_abspath in level3_yyyymmdd_dir_abspaths:
    _, strdate = os.path.split(yyyymmdd_dir_abspath)
    yyyymmdd_list.append(strdate)
    dates_n_paths_dict[strdate] = yyyymmdd_dir_abspath
  yyyymmdd_list = sorted(yyyymmdd_list)
  dates_n_paths_od = OrderedDict()
  for yyyymmdd in yyyymmdd_list:
    dates_n_paths_od[yyyymmdd] = dates_n_paths_dict[yyyymmdd]
  return dates_n_paths_od


def does_edgedate_folder_exist(pdate):
  """
    Notice the different between this function and get_level2folderabspath_or_todays()
    This one aims at finding if an edgedate folder exists, the other will do two extra things:
      1) the other will treat a non-date to be today's date
      2) the other will also create an edge date folder if it does not exist;
    That said, this one will return True if edge date folder exists and False otherwise.

  :param pdate:
  :return:
  """
  if pdate is None or len(str(pdate)) < 10:
    return False
  strdate = str(pdate)
  stryear = strdate[:4]
  stryearmonth = strdate[:7]
  middlepath = stryear + '/' + stryearmonth + '/' + strdate
  level0baseabspath = pathfs.get_ytvideo_htmlfiles_baseabsdir()
  level3abspath = os.path.join(level0baseabspath, middlepath)
  if os.path.isdir(level3abspath):
    return True
  return False


def mount_level3folderabspath_with_date(pdate=None, plevel0baseabspath=None):
  indate = pdate
  if indate is None or len(str(indate)) < 10:
    indate = dtfs.get_refdate_from_strdate_or_today()
  strdate = str(indate)
  stryear = strdate[:4]
  stryearmonth = strdate[:7]
  middlepath = stryear + '/' + stryearmonth + '/' + strdate
  level0baseabspath = find_0thlevel_dir_abspaths(plevel0baseabspath)
  level3abspath = os.path.join(level0baseabspath, middlepath)
  if not os.path.isdir(level3abspath):
    os.makedirs(level3abspath)
  return level3abspath


def generate_all_ytvideopages_abspath_asc_date():
  # dates_n_paths_od = get_ordered_dict_with_dates_n_abspaths()
  dateini, datefin = find_dateini_n_dateend_thru_yyyymmdd_level2_folders()
  for pdate in dtfs.generate_daterange_with_dateini_n_datefin(dateini, datefin):
    yyyymmdd_dir_abspath = mount_level3folderabspath_with_date(pdate)
    if yyyymmdd_dir_abspath is None:
      continue
    entries = os.listdir(yyyymmdd_dir_abspath)
    entries = filter(lambda f: endswith_htmls_n_startswith_date(f), entries)
    entries = sorted(entries)
    if len(entries) == 0:
      continue
    for entry in entries:
      entry_abspath = os.path.join(yyyymmdd_dir_abspath, entry)
      yield entry_abspath
  return None


def get_level3folderabspath_or_todays(pdate=None):
  """

  :param pdate:
  :return:
  """
  refdate = dtfs.return_refdate_as_datetimedate_or_today(pdate)
  level3foldername = str(refdate)
  level2foldername = str(refdate)[:7]
  level1folderabspath = get_level1folderabspath(refdate)
  level2folderabspath = os.path.join(level1folderabspath, level2foldername)
  level3folderabspath = os.path.join(level2folderabspath, level3foldername)
  if not os.path.isdir(level3folderabspath):
    os.makedirs(level3folderabspath)
  return level2folderabspath


def get_entries_in_level3abspath_from_date(pdate=None, p_level3folderabspath=None):
  """

  :param pdate:
  :param p_level2folderabspath:
  :return:
  """
  level3folderabspath = p_level3folderabspath
  if p_level3folderabspath is None:
    level3folderabspath = get_level3folderabspath_or_todays(pdate)
  files = os.listdir(level3folderabspath)
  return files


def get_htmlfilenames_from_date(pdate=None,  p_level3folderabspath=None):
  """

  :param pdate:
  :param p_level2folderabspath:
  :return:
  """
  level3folderabspath = p_level3folderabspath
  if p_level3folderabspath is None:
    level3folderabspath = get_level3folderabspath_or_todays(pdate)
  files = get_entries_in_level3abspath_from_date(pdate, level3folderabspath)
  htmlfiles = list(filter(lambda word: word.endswith('.html'), files))
  return htmlfiles


def get_len_htmlfilenames_from_date(pdate=None,  p_level2folderabspath=None):
  return len(get_htmlfilenames_from_date(pdate, p_level2folderabspath))


def is_todays_videospagehtml_folder_empty():
  if get_len_htmlfilenames_from_date() == 0:
    return True
  return False


def get_htmlfilepaths_from_date(pdate=None):
  """

  :param pdate:
  :return:
  """
  level3folderabspath = get_level3folderabspath_or_todays(pdate)
  htmlfile_abspath_list = []
  htmlfiles = get_htmlfilenames_from_date(pdate, level3folderabspath)
  for htmlfile in htmlfiles:
    htmlfile_abspath = os.path.join(level3folderabspath, htmlfile)
    htmlfile_abspath_list.append(htmlfile_abspath)
  return htmlfile_abspath_list


def find_dateini_n_dateend_thru_yyyymmdd_level2_folders():
  """

  :return:
  """
  total_yyyymmdd_foldernames = find_yyyymmdd_level3_foldernames()
  if len(total_yyyymmdd_foldernames) == 0:
    return None, None
  total_yyyymmdd_foldernames = sorted(total_yyyymmdd_foldernames)
  oldest = total_yyyymmdd_foldernames[0]
  newest = total_yyyymmdd_foldernames[-1]
  oldestdate = dtfs.get_refdate_from_strdate(oldest)
  newestdate = dtfs.get_refdate_from_strdate(newest)
  # the exception below, logically assessing, not never be raised but it is placed here for protection
  if oldestdate is None or newestdate is None:
    # error_msg = 'Error: oldestdate (%s) is None or newestdate (%s) is None' %(oldestdate, newestdate)
    return None, None
  return oldestdate, newestdate


def adhoc_test1():
  result = get_htmlfilepaths_from_date()
  for eachfile in result:
    print(eachfile)
  print('total', len(result))


def adhoc_test2():
  """
  generate_all_ytvideopages_abspath_asc_date
  :return:
  """
  for i, ytvideopage_abspath in enumerate(generate_all_ytvideopages_abspath_asc_date()):
    print(i+1, 'ytvideopage_abspath', ytvideopage_abspath)
  print('find_1stlevel_yyyy_dir_foldernames()', find_1stlevel_yyyy_dir_foldernames())
  print('find_2ndlevel_yyyymm_dir_foldernames()', find_2ndlevel_yyyymm_dir_foldernames())
  print('find_2ndlevel_yyyymm_dir_abspaths()', find_2ndlevel_yyyymm_dir_abspaths())
  print('find_yyyymmdd_level3_foldernames()', find_yyyymmdd_level3_foldernames())
  print('mount_level3folderabspath_with_date()', mount_level3folderabspath_with_date())
  pdate = dtfs.get_refdate_from_strdate_or_today()
  print('does_edgedate_folder_exist(%s)' %pdate, does_edgedate_folder_exist(pdate))

def process():
  """
    adhoc_test's are found in adhoctasks.fs.autofind_adhoctests.py

  :return:
  """
  adhoc_test2()


if __name__ == '__main__':
  process()
