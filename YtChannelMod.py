#!/usr/bin/python3
import datetime, os
import datefunctions.datefs as dtfs
import filefunctions.pathfunctions as pathfs

class YtChannel:

  def __init__(self, ytchid, nname='No name', refdate=None):
    self.ytchid  = ytchid
    self.nname   = nname
    self.refdate = dtfs.get_refdate(refdate)

  @property
  def murl(self):
    murl = pathfs.get_murl_from_ytchid(self.ytchid)
    if murl is None:
      # should never get here, but...
      error_msg = 'A wrong ytchid [%s] (id for [u]ser or [c]hannel in YouTube) came from database. Please, correct data and rerun.' %str(self.ytchid)
      raise ValueError(error_msg)
    return murl

  @property
  def strdate(self):
    return dtfs.get_strdate(self.refdate)

  @property
  def absfolderpath(self):
      return pathfs.get_datebased_ythtmlfiles_folderabspath(self.refdate)

  @property
  def datedpage_filename(self):
    return pathfs.datedpage_filename(self.strdate, self.nname, self.ytchid)

  @property
  def datedpage_filepath(self):
    return os.path.join(self.absfolderpath, self.datedpage_filename)

  @property
  def datedpage_exists(self):
    if os.path.isfile(self.datedpage_filepath):
      return True
    return False

  @property
  def videospageurl(self):
    ytvideosurl = pathfs.get_ytchannelvideospage_url_from_murl(self.murl)
    return ytvideosurl

  def __str__(self):
    strdict = {
      'nname':self.nname, 'murl':self.murl,'videospageurl':self.videospageurl,
      'absfolderpath':self.absfolderpath, 'datedpage_filename':self.datedpage_filename,
      'datedpage_filepath':self.datedpage_filepath,'datedpage_exists':self.datedpage_exists,
    }
    outstr = '''  nname          = %(nname)s
  murl           = %(murl)s  
  videospageurl  = %(videospageurl)s
  absfolderpath  = %(absfolderpath)s  
  dtdpg_filename = %(datedpage_filename)s
  dtdpg_filepath = %(datedpage_filepath)s
  datedpg_exists = %(datedpage_exists)s  
''' %(strdict)
    return outstr

def test():
  channel = YtChannel('cUCxKWYA49k16BoF8YzS1VbvA', 'Gabriela Prioli')
  print (channel)
  dt = datetime.date(2020, 5, 19)
  channel = YtChannel('cUCxKWYA49k16BoF8YzS1VbvA', 'Gabriela Prioli', dt)
  print (channel)

def process():
  test()

if __name__ == '__main__':
  process()