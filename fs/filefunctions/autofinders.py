#!/usr/bin/python3
import datetime, os, re
import fs.datefunctions.datefs as dtfs
import fs.filefunctions.pathfunctions as pathfs

lambdaentryisfolder = lambda x : os.path.isdir(x)
lambdastrformyearmonth = lambda x : dtfs.str_is_inversed_year_month(x)
lambdastrformdate = lambda x : dtfs.str_is_inversed_date(x)

def find_data_dateini_n_dateend():
  totaldatedirentries =  []
  datafolder_abspath = pathfs.get_ytvideo_htmlfiles_baseabsdir()
  # first level entries
  entries = os.listdir(datafolder_abspath)
  if len(entries) == 0:
    return (None, None)
  datedirentries = list(filter(lambdaentryisfolder, entries))
  datedirentries = list(filter(lambdastrformyearmonth, datedirentries))
  for direntry in datedirentries:
    # second level entries (where leaf folders are)
    dir2ndlevelentry_abspath = os.path.join(datafolder_abspath, direntry)
    secondlevelentries = os.listdir(dir2ndlevelentry_abspath)
    seclev_datedirentries = list(filter(lambdaentryisfolder, entries))
    seclev_datedirentries = list(filter(lambdastrformdate, datedirentries))
    if len(seclev_datedirentries) == 0:
      continue
    seclev_datedirentries = sorted(seclev_datedirentries)
    totaldatedirentries += secondlevelentries

  if len(totaldatedirentries) == 0:
    return (None, None)
  oldest = totaldatedirentries[0]
  newest = totaldatedirentries[-1]
  oldestdate = dtfs.get_refdate(oldest)
  newestdate = dtfs.get_refdate(newest)
  if oldestdate is None or newestdate is None:
    return (None, None)
  return (oldestdate, newestdate)

def retrieve_html_videos_recipient_folder_for_date(refdate):
  pass

def adhoc_test():
  tupl = find_data_dateini_n_dateend()
  print (tupl)
  print ('autofinders module')

def process():
  adhoc_test()

if __name__ == '__main__':
  process()