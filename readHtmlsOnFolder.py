#!/usr/bin/python3
import datetime, os, re
import datefunctions.datefs as dtfs
import filefunctions.pathfunctions as pathfs
from YtVideosPageMod import YtVideosPage

class YtVideoPagesTraversal:

  def __init__(self, refdate=None):
    self.refdate = dtfs.get_refdate(refdate)
    self._ytvideopageobj_list = []
    self.n_tries_in_producing_list = 0 # it has only 3 tries to fill-in list for it may be empty anyways

  @property
  def strdate(self):
    return dtfs.get_strdate(self.refdate)

  @property
  def ytvideopageobj_list(self):
    if len(self._ytvideopageobj_list) == 0 and self.n_tries_in_producing_list < 3:
      self.n_tries_in_producing_list += 1
      self.produce_ytvideopageobj_list()
    return self._ytvideopageobj_list

  @property
  def n_of_pages(self):
    return len(self.ytvideopageobj_list)

  def produce_ytvideopageobj_list(self):
    # look up data folder
    self._ytvideopageobj_list = []
    datafolder_abspath = pathfs.get_datebased_ythtmlfiles_folderabspath(self.refdate)
    entries = os.listdir(datafolder_abspath)
    for entry in entries:
      if not entry.startswith(self.strdate):
        continue
      ytchid = pathfs.extract_ytchid_from_filename(entry)
      if ytchid is None:
        continue
      ytvideopagesobj = YtVideosPage(ytchid, None, self.refdate)
      self._ytvideopageobj_list.append(ytvideopagesobj)
    return self._ytvideopageobj_list

  def print_ytvideopages_list(self):
    for ytvideopageobj in self.ytvideopageobj_list:
      print(ytvideopageobj)

def process():
  refdate = datetime.date(2020,5,22)
  traversor = YtVideoPagesTraversal(refdate)
  traversor.print_ytvideopages_list()
  refdate = None
  traversor = YtVideoPagesTraversal(refdate)
  traversor.print_ytvideopages_list()
  traversor = YtVideoPagesTraversal()
  traversor.print_ytvideopages_list()
  print ('len =', len(traversor.ytvideopageobj_list))

if __name__ == '__main__':
  process()