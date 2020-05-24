#!/usr/bin/python3
import datetime, os
import datefunctions.datefs as dtfs
import filefunctions.pathfunctions as pathfs
SUBSCRIBERS_NUMBER_HTMLCLASSNAME = 'yt-subscription-button-subscriber-count-branded-horizontal'

'''
<span class="yt-subscription-button-subscriber-count-branded-horizontal subscribed yt-uix-tooltip" 
  title="433 mil" tabindex="0" aria-label="433 mil inscritos">433 mil</span> 
'''


class YtVideoPagesTraversal:

  def __init__(self, refdate=None):
    self.refdate = dtfs.get_refdate(refdate)
    self.strdate = dtfs.get_strdate(self.refdate)
    self.files_w_abspath = []
    self.get_abspathfiles_list()

  def get_abspathfiles_list(self):
    # look up data folder
    datafolder_abspath = pathfs.get_datebased_ythtmlfiles_folderabspath(self.refdate)
    entries = os.listdir(datafolder_abspath)
    for entry in entries:
      if not entry.startswith(self.strdate):
        continue
      entry_abspath = os.path.join(datafolder_abspath, entry)
      if os.path.isfile(entry_abspath):
        self.files_w_abspath.append(entry_abspath)
    # return files_w_abspath

  def yield_htmlfilename_n_content_one_by_one(self):
    for htmlfile_abspath in self.files_w_abspath:
      htmlfilename = os.path.split(htmlfile_abspath)[-1]
      content = open(htmlfile_abspath).read()
      yield (htmlfilename, content)

  def print_filepaths(self):
    for filepath in self.files_w_abspath:
      print(filepath)

def process():
  refdate = datetime.date(2020,5,22)
  traversor = YtVideoPagesTraversal(refdate)
  traversor.print_filepaths()
  refdate = None
  traversor = YtVideoPagesTraversal(refdate)
  traversor.print_filepaths()

if __name__ == '__main__':
  process()