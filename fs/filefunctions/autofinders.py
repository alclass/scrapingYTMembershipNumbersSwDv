#!/usr/bin/python3
import os
import fs.datefunctions.datefs as dtfs
import fs.filefunctions.pathfunctions as pathfs
from collections import OrderedDict

lambdajoinabspath      = lambda path_n_entry : os.path.join(path_n_entry[0], path_n_entry[1])
lambdaentryisfolder    = lambda ppath : os.path.isdir(ppath)
lambdastrformdate      = lambda word : dtfs.str_is_inversed_date(word)
lambdafilterinyyyymm   = lambda word : dtfs.str_is_inversed_year_month(word)
lambdafilterinyyyymmdd = lambda word : dtfs.str_is_inversed_date(word)

def find_1stlevel_yyyymm_dir_foldernames(level1abspath=None):
  '''
  First level name entries that are named as yyyy-mm:
    obs:
      1) If the baseabsdir does not exist, it is created;
      2) if this dir creation happens, an empty foldername list will return;
      3) it may be empty if even it already existed;
      4) return foldernames are those with the yyyy-mm pattern;
      5) notice that filenames may be returned, the filtering will be done by the caller when paths are joint;

  :return:
  '''
  if level1abspath is None:
    level1abspath = pathfs.get_ytvideo_htmlfiles_baseabsdir()
  if not os.path.isdir(level1abspath):
    os.makedirs(level1abspath)
  entries = os.listdir(level1abspath)
  entries = list(filter(lambdafilterinyyyymm, entries))
  return entries

def find_1stlevel_yyyymm_dir_abspaths():
  '''
  First level path entries that are named as yyyy-mm and are directories:
    obs:
      1) this routine used the names returned by find_1stlevel_yyyymm_dir_foldernames();
      2) as some names may be files, it filters in only dirpaths;
      3) then returns this dirpath list;

  :return:
  '''
  level1abspath = pathfs.get_ytvideo_htmlfiles_baseabsdir()
  entries = find_1stlevel_yyyymm_dir_foldernames(level1abspath)
  if len(entries) == 0:
    return []
  zippedforlambda = list(zip([level1abspath]*len(entries), entries))
  abspath_entries  = list(map(lambdajoinabspath, zippedforlambda))
  yyyymm_level1_abspath_entries = list(filter(lambdaentryisfolder, abspath_entries))
  return yyyymm_level1_abspath_entries

def find_2ndlevel_yyyymmdd_dir_abspaths_from_a_1stlevel(level2abspathentry, level2entries):
  level2entries = list(filter(lambdafilterinyyyymmdd, level2entries))
  if len(level2entries) == 0:
    return
  zippedforlambda = zip([level2abspathentry]*len(level2entries), level2entries)
  level2_abspath_entries = list(map(lambdajoinabspath, zippedforlambda))
  level2_abspath_entries = list(filter(lambdaentryisfolder, level2_abspath_entries))
  return level2_abspath_entries

def find_all_2ndlevel_yyyymmdd_dir_abspaths():
  '''
  Second level path entries that are named as yyyy-mm-dd and are directories:
    obs:
      1) it takes all paths across all first level directories;

  :return:
  '''
  yyyymm_level1_abspath_entries = find_1stlevel_yyyymm_dir_abspaths()
  total_yyyymmdd_level2abspathentries = []
  for level2_abspath_entry in yyyymm_level1_abspath_entries:
    level2entries = os.listdir(level2_abspath_entry)
    level2_abspath_entries = find_2ndlevel_yyyymmdd_dir_abspaths_from_a_1stlevel(level2_abspath_entry, level2entries)
    total_yyyymmdd_level2abspathentries += level2_abspath_entries
  return total_yyyymmdd_level2abspathentries

def find_all_yyyymmdd_level2_foldernames():
  total_level2_abspath_entries = find_all_2ndlevel_yyyymmdd_dir_abspaths()
  total_yyyymmdd_foldernames =  []
  for pathentry in total_level2_abspath_entries:
    _, strdate = os.path.split(pathentry)
    total_yyyymmdd_foldernames.append(strdate)
  return total_yyyymmdd_foldernames

def find_dateini_n_dateend_thru_yyyymmdd_level2_folders():
  total_yyyymmdd_foldernames = find_all_yyyymmdd_level2_foldernames()
  if len(total_yyyymmdd_foldernames) == 0:
    return (None, None)
  total_yyyymmdd_foldernames = sorted(total_yyyymmdd_foldernames)
  oldest = total_yyyymmdd_foldernames[0]
  newest = total_yyyymmdd_foldernames[-1]
  oldestdate = dtfs.get_refdate_from_strdate(oldest)
  newestdate = dtfs.get_refdate_from_strdate(newest)
  # the exception below, logically assessing, not never be raised but it is placed here for protection
  if oldestdate is None or newestdate is None:
    error_msg = 'Error: oldestdate (%s) is None or newestdate (%s) is None' %(oldestdate, newestdate)
    return (None, None)
  return (oldestdate, newestdate)

def get_ordered_dict_with_dates_n_abspaths():
  level2_yyyymmdd_dir_abspaths = find_all_2ndlevel_yyyymmdd_dir_abspaths()
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

def process():
  '''
    adhoc_test's are found in adhoctasks.fs.autofind_adhoctests.py

  :return:
  '''
  pass

if __name__ == '__main__':
  process()
