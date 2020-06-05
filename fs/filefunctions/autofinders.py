#!/usr/bin/python3
import datetime, os, re
import fs.datefunctions.datefs as dtfs
import fs.filefunctions.pathfunctions as pathfs
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

def process():
  # test1()
  adhoc_test()

if __name__ == '__main__':
  process()