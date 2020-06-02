#!/usr/bin/python3
import datetime, os, re
import fs.datefunctions.datefs as dtfs

import config

def get_ytchannelvideospage_url_from_murl(murl):
  return config.YT_URL_PREFIX + murl + config.YT_URL_SUFIX

def get_murl_from_ytchid(ytchid):
  if ytchid is None or len(ytchid) < 6: # at least 'user/1'
    return None
  firstchar = ytchid[0]
  if firstchar == 'c':
    return 'channel/' + ytchid[1:]
  elif firstchar == 'u':
    return 'user/' + ytchid[1:]
  return None

def get_ytchannelvideospage_url_from_ytchid(ytchid):
  murl = get_murl_from_ytchid(ytchid)
  return get_ytchannelvideospage_url_from_murl(murl)

def get_ytvideo_htmlfiles_baseabsdir():
  return config.get_ytvideo_htmlfiles_baseabsdir()

def get_datebased_ythtmlfiles_folderabspath(p_refdate=None):
  refdate = dtfs.get_refdate(p_refdate)
  strdate = dtfs.get_strdate(refdate)
  datafolder_abspath = get_ytvideo_htmlfiles_baseabsdir()
  if datafolder_abspath is None:
    error_msg = 'datafolder_abspath options in config.py do not exist.'
    raise OSError(error_msg)
  # mount yyyy-mm as a subfolder
  subfolder = '%d-%s' %(refdate.year, str(refdate.month).zfill(2))
  datafolder_abspath = os.path.join(datafolder_abspath, subfolder)
  if not os.path.isdir(datafolder_abspath):
    # if os.makedirs() does not work, research whether or not an exception will be raised
    os.makedirs(datafolder_abspath)
  datafolder_abspath = os.path.join(datafolder_abspath, strdate)
  if not os.path.isdir(datafolder_abspath):
    # idem
    os.makedirs(datafolder_abspath)
  return datafolder_abspath

def datedpage_filename(strdate, nname, ytchid):
  if nname is None:
    refdate = dtfs.get_refdate_from_strdate(strdate)
    return find_datedpage_filename_on_folder(ytchid, refdate)
  truncatedname = nname
  if len(truncatedname) > 10: truncatedname = nname[:10]
  return strdate + ' ' + truncatedname + ' [' + ytchid + ']' + '.html'

def find_datedpage_filename_on_folder(ytchid, refdate=None):
  folderabspath = get_datebased_ythtmlfiles_folderabspath(refdate)
  entries = os.listdir(folderabspath)
  for entry in entries:
    if entry.find(ytchid) > -1:
      return entry
  return None

ytchid_from_filename_regexp_str = r'\[(.+)\]'
ytchid_from_filename_compiled_re = re.compile(ytchid_from_filename_regexp_str)
def extract_ytchid_from_filename(filename):
  re_match_obj = ytchid_from_filename_compiled_re.search(filename)
  if re_match_obj:
    ytchid = re_match_obj.group(1)
    return ytchid
  return None

def get_sname_from_filename(filename):
  if filename is None or len(filename) < 12:
    return None
  pos = filename.find('[')
  if pos < 12:
    return None
  trunk = filename[11 : pos]
  trunk = trunk.strip(' ')
  if len(trunk) == 0:
    return None
  return trunk

def get_fileabspath_ontopof_basedir(filename):
  datafolder_abspath = get_ytvideo_htmlfiles_baseabsdir()
  if datafolder_abspath is None:
    error_msg = 'datafolder_abspath was not found.  Please, fill in config.py with the YTVIDEO_HTMLFILES_DIR list.'
    raise OSError(error_msg)
  fileabspath = os.path.join(datafolder_abspath, filename)
  return fileabspath

def get_fileabspath_ontopof_basedir_ifexists(filename):
  fileabspath = os.path.join(get_fileabspath_ontopof_basedir(filename))
  if not os.path.isfile(fileabspath):
    return None
  return fileabspath

STATICHTML_FOLDERNAME = 'ytchannels_statichtml'
def get_statichtml_folderabspath():
  baseabspath = config.get_ytvideo_htmlfiles_baseabsdir()
  return os.path.join(baseabspath, STATICHTML_FOLDERNAME)

def adhoc_test():
  result = get_fileabspath_ontopof_basedir('test.txt')
  print (result)
  result = get_fileabspath_ontopof_basedir_ifexists('test')
  print (result)
  result = get_fileabspath_ontopof_basedir('test')
  print (result)
  folderabspath = get_datebased_ythtmlfiles_folderabspath()
  print (folderabspath)
  refdate = datetime.date(2020, 5, 19)
  folderabspath = get_datebased_ythtmlfiles_folderabspath(refdate)
  print (folderabspath)
  print (config.get_ytchannels_jsonabspath())
  ytchid = 'cUCWE75Qq5ExU0qlwQSkx18wQ' # Clayson's channel
  filename = find_datedpage_filename_on_folder(ytchid)
  print ('for today', ytchid, 'filename is', filename)
  filename = find_datedpage_filename_on_folder(ytchid, refdate)
  print ('for', str(refdate), ytchid, 'filename is', filename)
  filename = 'blah [cUCWE75Qq5ExU0qlwQSkx18wQ].html' # Clayson's channel
  extracted_ytchid = extract_ytchid_from_filename(filename)
  print ('extracted_ytchid', extracted_ytchid)

def process():
  adhoc_test()

if __name__ == '__main__':
  process()