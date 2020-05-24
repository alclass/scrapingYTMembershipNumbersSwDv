#!/usr/bin/python3
import datetime, os, re
import datefunctions.datefs as dtfs
import filefunctions.pathfunctions as pathfs

class YtVideosPage:

  def __init__(self, ytchid, nname=None, refdate=None):
    self.ytchid  = ytchid
    self.nname   = nname
    self.refdate = dtfs.get_refdate(refdate)

  @property
  def sname(self):
    if self.nname is None or len(self.nname) < 2:
      return pathfs.get_sname_from_filename(self.ytvideospagefilename)
    if len(self.nname) < 10:
      return self.nname
    return self.nname[:10]

  @property
  def strdate(self):
    return dtfs.get_strdate(self.refdate)

  @property
  def ytvideospagefilename(self):
    '''
    Notice an import difference here:
    1) if nname is None, filename should exist on folder and should be retrieve by dir lookup
    2) if nname is given, filename is returned even if it does not exist, for it is about to be created
    :return:
    '''
    if self.nname is None:
      filename = pathfs.find_datedpage_filename_on_folder(self.ytchid, self.refdate)
      if filename is None:
        error_msg = 'Could not establish filename for ' + str(self)
        raise OSError(error_msg)
    return pathfs.datedpage_filename(self.strdate, self.nname, self.ytchid)

  @property
  def ytvideospagefile_abspath(self):
    abspath = pathfs.get_datebased_ythtmlfiles_folderabspath(self.refdate)
    filename = self.ytvideospagefilename
    return os.path.join(abspath, filename)

  def get_html_text(self):
    return open(self.ytvideospagefile_abspath).read()

  def __str__(self):
    outdict = {
      'ytchid':self.ytchid,'nname':self.nname,'sname':self.sname,
      'filename':self.ytvideospagefilename, 'strdate': self.strdate
    }
    outstr = '''YtVideosPage:
  ytchid   = %(ytchid)s
  nname    = %(nname)s
  sname    = %(sname)s
  filename = %(filename)s
  refdate = %(strdate)s
    ''' %outdict
    return outstr

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