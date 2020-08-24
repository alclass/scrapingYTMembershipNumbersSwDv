#!/usr/bin/env python3
"""
"""
import datetime
import logging
import os
import fs.datefunctions.datefs as dtfs
import fs.filefunctions.autofinders as autof
import fs.filefunctions.pathfunctions as pathfs
import config

_, logfilename = os.path.split(__file__)
logfilename = str(datetime.date.today()) + '_' + logfilename[:-3] + '.log'
logfilepath = os.path.join(config.get_logfolder_abspath(), logfilename)
logging.basicConfig(filename=logfilepath, filemode='w', format='%(name)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def traverse(src_abspath, trg_abspath):
  src_ini, src_fin = autof.find_dateini_n_datefin_thru_yyyymmdd_level3_folders(src_abspath)
  trg_ini, trg_fin = autof.find_dateini_n_datefin_thru_yyyymmdd_level3_folders(trg_abspath)
  print(src_abspath)
  print(src_ini, src_fin)
  print(trg_abspath)
  print(trg_ini, trg_fin)

gcounter = 0


def sync_dirs():
  """

  """
  # global gcounter
  datadirs_abspaths = config.YTVIDEO_HTMLFILES_DIRS
  src_mnt_abspath = datadirs_abspaths[0]
  trg_mnt_abspath = datadirs_abspaths[1]
  traverse(src_mnt_abspath, trg_mnt_abspath)
  autof.find_all_3rdlevel_yyyymmdd_dir_abspaths()
  seq = 0
  src_abspath = None
  trg_abspath = None
  src_mdt = None
  trg_mdt = None
  for src_abspath in autof.generate_all_ytvideopages_abspath_asc_date(src_mnt_abspath):
    _, filename = os.path.split(src_abspath)
    complement_path = pathfs.extract_middlepath_from_mountpoint_n_abspath(src_mnt_abspath, src_abspath)
    trg_abspath = os.path.join(trg_mnt_abspath, complement_path)
    src_t = os.stat(src_abspath)
    trg_t = os.stat(trg_abspath)
    seq += 1
    src_mdt = datetime.datetime.fromtimestamp(src_t.st_mtime)
    trg_mdt = datetime.datetime.fromtimestamp(src_t.st_mtime)
    src_mdt = dtfs.zero_microsec_in_datetime(src_mdt)
    trg_mdt = dtfs.zero_microsec_in_datetime(trg_mdt)
    if src_mdt != trg_mdt:
      print(seq, filename, 'src', src_t.st_mtime, 'trg', trg_t.st_mtime)
  print('total', seq)
  print('src_abspath', src_abspath)
  print('trg_abspath', trg_abspath)
  print('src', src_mdt, 'trg', trg_mdt)


def adhoc_test():
  """
  list atime ctime & mtime for Villa's videopage on 2020-08-23
  :return:
  """
  filepath = '/media/friend/SAMSUNG/Ytvideos BRA Politics/z Other ytchannels/000_scrape_ytdata/' \
             '2020/2020-08/2020-08-23/2020-08-23 Marco Vill [cUCVqNUy4-FTLMwMKX-krfB6A].html'
  t = os.stat(filepath)
  adt = datetime.datetime.fromtimestamp(t.st_atime)
  cdt = datetime.datetime.fromtimestamp(t.st_ctime)
  mdt = datetime.datetime.fromtimestamp(t.st_mtime)
  text = open(filepath).read()
  text = text if len(text) < 81 else text[:80]
  print('text', text)
  print('a', adt)
  print('c', cdt)
  print('m', mdt)

def process():
  # sync_dirs()
  adhoc_test()


if __name__ == '__main__':
  process()
