#!/usr/bin/python3
import copy, datetime, json, os
import datefunctions.datefs as dtfs
import filefunctions.pathfunctions as pathfs

YT_URL_PREFIX = "https://www.youtube.com/"
YT_URL_SUFIX  = "/videos"

def get_ytvideos_url(murl):
  return YT_URL_PREFIX + murl + YT_URL_SUFIX

class YtChannel:

  def __init__(self, nname, murl, refdate=None):
    self.refdate = dtfs.get_refdate(refdate)
    self.strdate = dtfs.get_strdate(refdate)
    self.nname = nname
    self.murl = murl
    if refdate is None:
      refdate = datetime.date.today()
    self.refdate = refdate
    self._refdate_str = None
    self._absfilepath = None

  @property
  def datedpage_filename(self):
    return self.refdate_str + ' ' + self.nname + '.html'

  @property
  def absfilepath(self):
    if self._absfilepath is None:
      self._absfilepath = pathfs.get_datebased_ythtmlfiles_folderabspath()
    return self._absfilepath

  @property
  def videospageurl(self):
    if self.refdate_str != dtfs.UtilDater.get_refdate_inverted_fields_str():
      return 'n/a (older date)'
    ytvideosurl = get_ytvideos_url(self.murl)
    return ytvideosurl

  def __str__(self):
    strdict = {'nname':self.nname, 'murl':self.murl,'videospageurl':self.videospageurl,
               'datedpage_filename':self.datedpage_filename,
               'absfilepath':self.absfilepath}
    outstr = '''  nname          = %(nname)s
  murl           = %(murl)s  
  videospageurl  = %(videospageurl)s
  dtdpg_filename = %(datedpage_filename)s
  absfilepath    = %(absfilepath)s  
''' %(strdict)
    return outstr


def test():
  channel = YtChannel('Gabriela Prioli', 'channel/UCxKWYA49k16BoF8YzS1VbvA')
  print (channel)
  dt = datetime.date(2020, 5, 19)
  channel = YtChannel('Gabriela Prioli', 'channel/UCxKWYA49k16BoF8YzS1VbvA', dt)
  print (channel)

def process():
  test()

if __name__ == '__main__':
  process()