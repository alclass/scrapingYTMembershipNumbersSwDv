#!/usr/bin/python3
"""
  docstring
"""
import os
import re
import config
import fs.datefunctions.datefs as dtfs


def get_ytchannelvideospage_url_from_murl(murl):
  return config.YT_URL_PREFIX + murl + config.YT_URL_SUFIX


def get_murl_from_ytchid(ytchid):
  if ytchid is None or len(ytchid) < 6:  # at least 'user/1'
    return None
  firstchar = ytchid[0]
  if firstchar == 'a':
    return 'c/' + ytchid[1:]
  elif firstchar == 'c':
    return 'channel/' + ytchid[1:]
  elif firstchar == 'u':
    return 'user/' + ytchid[1:]
  return None


def get_ytchannelvideospage_url_from_ytchid(ytchid):
  murl = get_murl_from_ytchid(ytchid)
  return get_ytchannelvideospage_url_from_murl(murl)


def get_ytvideo_htmlfiles_baseabsdir():
  return config.get_ytvideo_datafolderbase_absdir()


def form_conventioned_datedvideopage_filename(refdate, sname, ytchannelid):
  """
  Eg
    "2020-08-22 Henry Buga [uhenrybugalho].html"
  :param refdate:
  :param sname:
  :param ytchannelid:
  :return:
  """
  pdate = dtfs.get_refdate_from_strdate_or_today(refdate)
  filename = '%(refdate)s %(sname)s [%(ytchannelid)s].html' % {'refdate': pdate, 'sname': sname, 'ytchannelid': ytchannelid}
  return filename


def is_htmldatedfilename_under_convention(filename):
  """
    Convention is "(10-char-strdate) ([publisher-nname]) (title-or-slug)(.ext)"
  :param filename:
  :return:
  """
  if len(filename) < 11:
    return False
  may_be_none = dtfs.get_refdate_from_strdate_or_none(filename[:10])
  if may_be_none is None:
    return False
  pos_open_squarebracket = filename.find('[')
  if pos_open_squarebracket > -1:
    return False
  pos_close_squarebracket = filename.find(']')
  if pos_close_squarebracket > -1:
    return False
  if pos_open_squarebracket > pos_close_squarebracket:
    return False
  _, ext = os.path.splitext(filename)
  if ext not in config.HTML_EXTLIST:
    return False
  return True


ytchid_from_filename_regexp_str = r'\[(.+)\]'
ytchid_from_filename_compiled_re = re.compile(ytchid_from_filename_regexp_str)


def extract_ytchid_from_filename(filename):
  re_match_obj = ytchid_from_filename_compiled_re.search(filename)
  if re_match_obj:
    ytchid = re_match_obj.group(1)
    return ytchid
  return None


def extract_middlepath_from_mountpoint_n_abspath(mountpoint, abspath):
  """
  if not abspath.startswith(mountpoint):
    return None
  if mountpoint != '/':
    if abspath.find('/') > -1 and mountpoint.find('/') > -1:
      mm = mountpoint.split('/')
      aa = abspath.split('/')
      if len(aa) < len(mm):
        return None
      if mm[-1] != aa[len(mm)-1]:
        return None

  :param mountpoint:
  :param abspath:
  :return:
  """
  if len(abspath) < len(mountpoint):
    return None
  if not abspath.startswith(mountpoint):
    return None
  if len(abspath) == len(mountpoint):
    return ''
  middlepath = abspath[len(mountpoint):]
  middlepath = middlepath.strip('/')
  return middlepath


def get_fileabspath_ontopof_basedir(filename):
  datafolder_abspath = get_ytvideo_htmlfiles_baseabsdir()
  if datafolder_abspath is None:
    error_msg = 'datafolder_abspath was not found.  Please, fill in config.py with the YTVIDEO_HTMLFILES_DIR list.'
    raise OSError(error_msg)
  fileabspath = os.path.join(datafolder_abspath, filename)
  return fileabspath


def get_level2_folder_abspath_from_refdate(refdate):
  yyyymmdd10char = str(refdate)
  if len(yyyymmdd10char) != 10:
    return None
  basedir_abspath = get_ytvideo_htmlfiles_baseabsdir()
  yyyymm7char = str(yyyymmdd10char)[:7]
  is_good = dtfs.is_stryyyydashmm_good(yyyymm7char)
  if not is_good:
    return None
  level1folder_abspath = os.path.join(basedir_abspath, yyyymm7char)
  level2folder_abspath = os.path.join(level1folder_abspath, yyyymmdd10char)
  return level2folder_abspath


def does_filename_have_ext_from_extlist(filename, extlist=None):
  if extlist is None:
    extlist = ['htm', 'html']
  elif type(extlist) == str:
    extlist = [extlist]
  elif type(extlist) != list:
    extlist = ['htm', 'html']
  _, ext = os.path.splitext(filename)
  ext = ext.lstrip('.')
  if ext in extlist:
    return True
  return False


def get_sname_from_filename(filename):
  if filename is None or len(filename) < 12:
    return None
  pos = filename.find('[')
  if pos < 12:
    return None
  # strips yyyy-mm-dd at the beginning
  trunk = filename[11: pos]
  # strips enclosing ' ' (left [lstrip] and right [rstrip])
  trunk = trunk.strip(' ')
  if len(trunk) == 0:
    return None
  return trunk


def get_statichtml_folderabspath():
  baseabspath = config.get_ytvideo_datafolderbase_absdir()
  return os.path.join(baseabspath, config.STATICHTML_FOLDERNAME)


def get_statichtml_filename():
  return config.STATICHTML_FILENAME


def get_statichtml_fileabspath():
  return os.path.join(get_statichtml_folderabspath(), get_statichtml_filename())


def get_fileabspath_ontopof_basedir_ifexists(filename):
  fileabspath = os.path.join(get_fileabspath_ontopof_basedir(filename))
  if not os.path.isfile(fileabspath):
    return None
  return fileabspath


def adhoc_test():
  result = get_fileabspath_ontopof_basedir('test.txt')
  print(result)
  result = get_fileabspath_ontopof_basedir_ifexists('test')
  print(result)
  result = get_fileabspath_ontopof_basedir('test')
  print(result)
  filename = 'blah [cUCWE75Qq5ExU0qlwQSkx18wQ].html'  # Clayson's channel
  extracted_ytchid = extract_ytchid_from_filename(filename)
  print('extracted_ytchid', extracted_ytchid)
  mountpoint = '/a/b/c/d/science'
  abspath = '/a/b/c/d/science/physics/relativity///'
  middlepath = extract_middlepath_from_mountpoint_n_abspath(mountpoint, abspath)
  print('middlepath', middlepath)


def process():
  adhoc_test()


if __name__ == '__main__':
  process()
