#!/usr/bin/python3
import os
import datefunctions.datefs as dtfs

import config # get_ytvideo_htmlfiles_absdir

def get_ytvideos_url(murl):
  return config.YT_URL_PREFIX + murl + config.YT_URL_SUFIX

def get_ytvideo_htmlfiles_absdir():
  return config.get_ytvideo_htmlfiles_absdir()

def get_datebased_ythtmlfiles_folderabspath(refdate=None):
  strdate = dtfs.get_strdate(refdate)
  datafolder_abspath = get_ytvideo_htmlfiles_absdir()
  return os.path.join(datafolder_abspath, strdate)

def get_fileabspath(filename):
  datafolder_abspath = get_ytvideo_htmlfiles_absdir()
  if datafolder_abspath is None:
    error_msg = 'datafolder_abspath was not found.  Please, fill in config.py with the YTVIDEO_HTMLFILES_DIR list.'
    raise OSError(error_msg)
  fileabspath = os.path.join(datafolder_abspath, filename)
  if not os.path.isfile(fileabspath):
    return None
  return fileabspath

def get_jsondata_absdir():
  ytvideo_htmlfiles_absdir = get_ytvideo_htmlfiles_absdir()
  if ytvideo_htmlfiles_absdir is None:
    return None
  return os.path.join(ytvideo_htmlfiles_absdir, config.JSONRELFOLDER)

def adhoc_test():
  result = get_fileabspath('test')
  print (result)
  result = get_fileabspath('test.txt')
  print (result)
  folderabspath = get_datebased_ythtmlfiles_folderabspath()
  print (folderabspath)

def process():
  adhoc_test()

if __name__ == '__main__':
  process()