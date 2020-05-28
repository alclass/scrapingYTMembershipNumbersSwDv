#!/usr/bin/python3
import os
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

def adhoc_test():
  pass

def process():
  adhoc_test()

if __name__ == '__main__':
  process()