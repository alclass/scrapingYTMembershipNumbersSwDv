#!/usr/bin/env python3
"""
  docstring
"""
from collections import OrderedDict
import datetime
import os
import config
import fs.datefunctions.datefs as dtfs
import fs.filefunctions.pathfunctions as pathfs


def find_datedpage_filename_on_folder(ytchid, refdate=None):
  entries = find_htmlfilenames_from_date(refdate)
  for entry in entries:
    if entry.find(ytchid) > -1:
      return entry
  return None


def form_datedpage_filename_with_triple(strdate, sname, ytchannelid):
  """
    datedpage_filename is a composition of 3 fields, ie:
      1) strdate which a 10-char yyyy-mm-dd
      2) sname which is a contraction of nname having 10 or less characters
      3) ytchannelid is the ytid preprend with a letter in {u, c, d}

  None cases that can be treated:
    1) if strdate is None (not given), it'll default to today's date
    2) if sname is None (not given), a search on datafolder will occurr
       see function find_datedpage_filename_on_folder(ytchannelid, refdate)
    3) if ytchannelid is None (not given), a ValueError exception will be raised

  :param strdate:
  :param sname:
  :param ytchannelid:
  :return:
  """
  if ytchannelid is None:
    error_msg = 'Error: ytchannelid is None in datedpage_filename(strdate, sname, ytchannelid)'
    raise ValueError(error_msg)

  ytchannelid = str(ytchannelid)
  if len(ytchannelid) == 0:
    error_msg = 'Error: ytchannelid is empty in datedpage_filename(strdate, sname, ytchannelid)'
    raise ValueError(error_msg)

  refdate = dtfs.get_refdate_from_strdate_or_today(strdate)
  if sname is None:
     return find_datedpage_filename_on_folder(ytchannelid, refdate)
  truncatedname = sname
  truncatedname = truncatedname.lstrip(' \t').rstrip(' \t\r\n')
  if len(truncatedname) > 10:
    truncatedname = sname[:10]
  if truncatedname.endswith(' '):
    truncatedname = truncatedname.strip(' ')
  return strdate + ' ' + truncatedname + ' [' + ytchannelid + ']' + '.html'


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


def joinabspath_with_abspath_n_filename(abspath, filename):
  """
    Former lambda
  :param abspath:
  :param filename:
  :return:
  """
  path_n_entry_tuple = abspath, filename
  return joinabspath_with_tuple(path_n_entry_tuple)


def find_level0folderabspath(level0folderabspath=None):
  if level0folderabspath is None or not os.path.isdir(level0folderabspath):
    level0folderabspath = pathfs.get_ytvideo_htmlfiles_baseabsdir()
  return level0folderabspath


def find_level1folderabspath(pdate=None, create_folder=False, level0folderabspath=None):
  """

  :param pdate:
  :param create_folder:
  :param level0folderabspath:
  :return:
  """
  level0baseabspath = find_level0folderabspath(level0folderabspath)
  refdate = dtfs.return_refdate_as_datetimedate_or_today(pdate)
  level1foldername = str(refdate)[:4]
  level1folderabspath = os.path.join(level0baseabspath, level1foldername)
  if create_folder and not os.path.isdir(level1folderabspath):
    os.makedirs(level1folderabspath)
  return level1folderabspath


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
  entries = list(filter(dtfs.is_stryyyy_good, entries))
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
  entries = filter(dtfs.is_stryyyy_good, entries)
  yyyy_level1_abspath_entries = [os.path.join(level0abspath, e) for e in entries]
  yyyy_level1_abspath_entries = list(filter(lambda f: os.path.isdir(f), yyyy_level1_abspath_entries))
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
    entries = list(filter(dtfs.does_str_form_yyyymm7chardate, entries))
    l2foldernames += entries
  return l2foldernames


def find_2ndlevel_yyyymm_dir_abspaths(level1abspath=None):
  """

  :param level1abspath:
  :return:
  """
  l2abspaths = find_1stlevel_yyyy_dir_abspaths(level1abspath)
  l2foldernames = []
  total_l2paths = []
  for l2abspath in l2abspaths:
    entries = os.listdir(l2abspath)
    entries = list(filter(dtfs.does_str_form_yyyymm7chardate, entries))
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
  level2entries = list(filter(dtfs.does_str_form_yyyymm7chardate, level2entries))
  if len(level2entries) == 0:
    return
  zippedforlambda = zip([level2abspathentry]*len(level2entries), level2entries)
  level2_abspath_entries = list(map(joinabspath_with_tuple, zippedforlambda))
  level2_abspath_entries = list(filter(lambda f: os.path.isdir(f), level2_abspath_entries))
  return level2_abspath_entries


def find_all_3rdlevel_yyyymmdd_dir_abspaths(level0abspath=None):
  """
  Third level path entries that are named as yyyy-mm-dd and are directories:
    obs:
      1) it takes all paths across all first level directories;
      2) this function is memory-greedy, to use a generator version see <generetor_version>

  :return:
  """
  yyyymm_level2_abspath_entries = find_2ndlevel_yyyymm_dir_abspaths(level0abspath)
  total_yyyymmdd_level2abspathentries = []
  for level2_abspath_entry in yyyymm_level2_abspath_entries:
    level2entries = os.listdir(level2_abspath_entry)
    level2_abspath_entries = [os.path.join(level2_abspath_entry, e) for e in level2entries]
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


def find_oldest_yyyymmdd_level3_foldername(l0abspath=None):
  l0abspath = find_0thlevel_dir_abspaths(l0abspath)
  foldernames = find_1stlevel_yyyy_dir_foldernames(l0abspath)
  if len(foldernames) == 0:
    return None
  foldernames = sorted(foldernames)
  oldest_foldername = foldernames[0]
  foldernames = find_l2foldernames_for_l1foldername(oldest_foldername)
  if len(foldernames) == 0:
    return None
  foldernames = sorted(foldernames)
  oldest_foldername = foldernames[0]
  foldernames = find_l3foldernames_for_l2foldername(oldest_foldername)
  if len(foldernames) == 0:
    return None
  foldernames = sorted(foldernames)
  oldest_foldername = foldernames[0]
  return oldest_foldername


def find_newest_yyyymmdd_level3_foldername(l0abspath=None):
  l0abspath = find_0thlevel_dir_abspaths(l0abspath)
  foldernames = find_1stlevel_yyyy_dir_foldernames(l0abspath)
  if len(foldernames) == 0:
    return None
  foldernames = sorted(foldernames)
  newest_foldername = foldernames[-1]
  foldernames = find_l2foldernames_for_l1foldername(newest_foldername)
  if len(foldernames) == 0:
    return None
  foldernames = sorted(foldernames)
  newest_foldername = foldernames[-1]
  foldernames = find_l3foldernames_for_l2foldername(newest_foldername)
  if len(foldernames) == 0:
    return None
  foldernames = sorted(foldernames)
  newest_foldername = foldernames[-1]
  return newest_foldername


def find_dateini_n_datefin_thru_yyyymmdd_level3_folders(level0abspath=None):
  level0abspath = find_level0folderabspath(level0abspath)
  strdate_ini = find_oldest_yyyymmdd_level3_foldername(level0abspath)
  strdate_fin = find_newest_yyyymmdd_level3_foldername(level0abspath)
  dateini = dtfs.get_refdate_from_strdate_or_none(strdate_ini)
  datefin = dtfs.get_refdate_from_strdate_or_none(strdate_fin)
  return dateini, datefin


def find_dateini_n_datefin_thru_yyyymmdd_level3_folders_olderversion():
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


def find_3rdlevel_yyyymm_files_abspaths_on_date(pdate=None, level0abspath=None):
  l3abspath = mount_level3folderabspath_with_date(pdate, create_folder=False, plevel0baseabspath=level0abspath)
  if l3abspath is None:
    return []
  entries = os.listdir(l3abspath)
  entries = filter(lambda f: endswith_htmls_n_startswith_date(f), entries)
  files_abspaths = [os.path.join(l3abspath, e) for e in list(entries)]
  return files_abspaths


def find_htmlfilepaths_from_date(pdate=None, level0folderabspath=None):
  """

  :param pdate:
  :param level0folderabspath:
  :return:
  """
  indate = dtfs.get_refdate_or_today(pdate)
  htmlfiles = find_htmlfilenames_from_date(pdate, level0folderabspath)
  if len(htmlfiles) == 0:
    return []
  level3datefolderabspath = mount_level3folderabspath_with_date(
    indate, create_folder=False, plevel0baseabspath=level0folderabspath
  )
  if level3datefolderabspath is None:
    return []
  htmls_abspaths = [os.path.join(level3datefolderabspath, str(e)) for e in htmlfiles]
  return htmls_abspaths


def find_level3folderabspath_or_todays(pdate=None, level0folderabspath=None):
  """

  :param pdate:
  :param level0folderabspath:
  :return:
  """
  refdate = dtfs.get_refdate_or_today(pdate)
  if refdate is None:
    return None
  l3abspath = mount_level3folderabspath_with_date(refdate, create_folder=False, plevel0baseabspath=level0folderabspath)
  if l3abspath is None:
    return None
  return l3abspath


def find_htmlfilenames_from_date(pdate=None, level0abspath=None):
  """

  :param pdate:
  :param level0abspath:
  :return:
  """
  indate = dtfs.get_refdate_or_today(pdate)
  l3abspath = mount_level3folderabspath_with_date(indate, create_folder=False, plevel0baseabspath=level0abspath)
  html_filenames = os.listdir(l3abspath)
  html_filenames = list(filter(lambda f: endswith_htmls_n_startswith_date(f), html_filenames))
  return html_filenames


def find_l1foldernames(l0abspath=None):
  l0abspath = find_0thlevel_dir_abspaths(l0abspath)
  foldernames = os.listdir(l0abspath)
  foldernames = list(filter(dtfs.is_strdate_a_dashed_8to10char_yyyymmdd, foldernames))
  zippedforlambda = list(zip([l0abspath]*len(foldernames), foldernames))
  path_n_foldernames = filter(lambda tupl: os.path.join, zippedforlambda)
  foldernames = list(map(lambda tupl: tupl[1], path_n_foldernames))
  foldernames = list(sorted(foldernames))
  return foldernames


def find_l2foldernames_for_l1foldername(stryyyfoldername, l0abspath=None):
  if stryyyfoldername is None:
    return []
  l0abspath = find_0thlevel_dir_abspaths(l0abspath)
  l1abspath = os.path.join(l0abspath, stryyyfoldername)
  foldernames = os.listdir(l1abspath)
  foldernames = list(filter(dtfs.does_str_form_yyyymm7chardate, foldernames))
  zippedforlambda = list(zip([l1abspath]*len(foldernames), foldernames))
  path_n_foldernames = filter(lambda tupl: os.path.join, zippedforlambda)
  foldernames = list(map(lambda tupl: tupl[1], path_n_foldernames))
  foldernames = list(sorted(foldernames))
  return foldernames


def find_l3foldernames_for_l2foldername(stryyymmfoldername, l0abspath=None):
  if stryyymmfoldername is None:
    return []
  if not dtfs.does_str_form_yyyymm7chardate(stryyymmfoldername):
    return []
  middlepath = stryyymmfoldername[:4] + '/' + stryyymmfoldername
  l0abspath = find_0thlevel_dir_abspaths(l0abspath)
  l2abspath = os.path.join(l0abspath, middlepath)
  foldernames = os.listdir(l2abspath)
  foldernames = list(filter(dtfs.is_strdate_a_dashed_8to10char_yyyymmdd, foldernames))
  zippedforlambda = list(zip([l2abspath]*len(foldernames), foldernames))
  path_n_foldernames = filter(lambda tupl: os.path.join, zippedforlambda)
  foldernames = list(map(lambda tupl: tupl[1], path_n_foldernames))
  foldernames = list(sorted(foldernames))
  return foldernames


def generate_asc_date_n_abspath_tuplelist_iter(level0abspath=None):
  """
  This function is a memory-friendly version of get_ordered_dict_with_dates_n_abspaths().
  The former function is also available in this module, but if datasize is "big",
    a lot of RAM will be used (memory-greedy). For this case ("big" dataset), use this one instead.

  :param level0abspath:
  :return:
  """
  dateini, datefin = find_dateini_n_datefin_thru_yyyymmdd_level3_folders(level0abspath)
  for pdate in dtfs.generate_daterange_with_dateini_n_datefin(dateini, datefin):
    l3_datefolder_abspath = mount_level3folderabspath_with_date(
      pdate, create_folder=False, plevel0baseabspath=level0abspath
    )
    if l3_datefolder_abspath is None:
      continue
    yield pdate, l3_datefolder_abspath


def get_ordered_dict_with_dates_n_abspaths(level0abspath=None):
  """
  ATTENTION: this function is memory-greedy, so if datasize is "big", use instead:
             generate_asc_date_n_abspath_tuplelist_iter()

  :param level0abspath:
  :return:
  """
  level3_yyyymmdd_dir_abspaths = find_all_3rdlevel_yyyymmdd_dir_abspaths(level0abspath)
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


def does_l3datefolder_exist_for_date(pdate):
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


def mount_level3folderabspath_with_date(pdate=None, create_folder=True, plevel0baseabspath=None):
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
    if create_folder:
      os.makedirs(level3abspath)
  return level3abspath


def generate_all_ytvideopages_abspath_asc_date(level0abspath=None):
  # dates_n_paths_od = get_ordered_dict_with_dates_n_abspaths()
  dateini, datefin = find_dateini_n_datefin_thru_yyyymmdd_level3_folders(level0abspath)
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


def len_htmlfilenames_from_date(pdate=None, p_level0folderabspath=None):
  return len(find_htmlfilenames_from_date(pdate, p_level0folderabspath))


def is_todays_videospagehtml_folder_empty():
  if len_htmlfilenames_from_date() == 0:
    return True
  return False


def adhoc_test1():
  result = find_htmlfilepaths_from_date()
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
  print('does_l3datefolder_exist_for_date(%s)' % pdate, does_l3datefolder_exist_for_date(pdate))
  foldernames = find_l3foldernames_for_l2foldername('2020-07')
  print('l3 foldernames', foldernames)
  foldernames = find_l2foldernames_for_l1foldername('2020')
  print('l2 foldernames', foldernames)
  foldernames = find_l1foldernames('2020')
  print('l1 foldernames', foldernames)
  dateini, datefin = find_dateini_n_datefin_thru_yyyymmdd_level3_folders()
  print('dateini, datefin', dateini, datefin)
  files_abspaths = find_3rdlevel_yyyymm_files_abspaths_on_date()
  print('dateini, datefin find_3rdlevel_yyyymm_files_abspaths_on_date()', files_abspaths)
  files_abspaths = find_1stlevel_yyyy_dir_abspaths()
  print('find_1stlevel_yyyy_dir_abspaths()', files_abspaths)


def adhoc_test3():
  oldest_yyyymmdd = find_oldest_yyyymmdd_level3_foldername()
  print('oldest_yyyymmdd', oldest_yyyymmdd)
  newest_yyyymmdd = find_newest_yyyymmdd_level3_foldername()
  print('newest_yyyymmdd', newest_yyyymmdd)
  pdate = dtfs.get_refdate_from_strdate_or_today()
  print('does_l3datefolder_exist_for_date(%s)' % pdate, does_l3datefolder_exist_for_date(pdate))
  pdate = '2020-05-22'
  print('does_l3datefolder_exist_for_date(%s)' % pdate, does_l3datefolder_exist_for_date(pdate))
  seq = 0
  for t in generate_asc_date_n_abspath_tuplelist_iter(level0abspath=None):
    strdate = str(t[0])
    l3abspath = t[1]
    seq += 1
    print(seq, strdate, l3abspath)


def adhoc_test():
  result = pathfs.get_fileabspath_ontopof_basedir('test.txt')
  print(result)
  result = pathfs.get_fileabspath_ontopof_basedir_ifexists('test')
  print(result)
  result = pathfs.get_fileabspath_ontopof_basedir('test')
  print(result)
  refdate = datetime.date(2020, 5, 19)
  print(config.get_ytchannels_jsonabspath())
  ytchid = 'cUCWE75Qq5ExU0qlwQSkx18wQ'  # Clayson's channel
  filename = find_datedpage_filename_on_folder(ytchid)
  print('for today', ytchid, 'filename is', filename)
  filename = find_datedpage_filename_on_folder(ytchid, refdate)
  print('for', str(refdate), ytchid, 'filename is', filename)
  filename = 'blah [cUCWE75Qq5ExU0qlwQSkx18wQ].html'  # Clayson's channel
  extracted_ytchid = pathfs.extract_ytchid_from_filename(filename)
  print('extracted_ytchid', extracted_ytchid)

def process():
  """
    adhoc_test's are found in adhoctasks.fs.autofind_adhoctests.py

  :return:
  """
  adhoc_test3()


if __name__ == '__main__':
  process()
