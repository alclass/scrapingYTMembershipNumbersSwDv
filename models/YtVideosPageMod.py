#!/usr/bin/python3
import datetime, os
import fs.datefunctions.datefs as dtfs
import fs.filefunctions.pathfunctions as pathfs
import config

class YtVideosPage:

  def __init__(self, ytchannelid, nname=None, refdate=None):
    self.ytchannelid     = ytchannelid
    self.nname           = nname
    self.sname           = None
    self.refdate = dtfs.get_refdate(refdate)
    self._nOfSubscribers = None
    self._days_n_subscribers = []

  @property
  def nOfSubscribers(self):
    return self._nOfSubscribers

  @nOfSubscribers.setter
  def nOfSubscribers(self, n):
    if n is None:
      return
    self._nOfSubscribers = n

  @property
  def days_n_subscribers(self):
    return self._days_n_subscribers

  @days_n_subscribers.setter
  def days_n_subscribers(self, alist):
    if alist is None:
      return
    self._days_n_subscribers = alist

  def has_nOfSubscribers_been_set(self):
    if self._nOfSubscribers is not None:
      return True
    return False

  def is_nOfSubscribers_known(self):
    if self._nOfSubscribers is not None and self._nOfSubscribers != -1:
      return True
    return False

  @property
  def sname(self):
    if self._sname is not None:
      return self._sname
    if self.nname is None:
      upto10chars = len(self.ytchannelid)
      upto10chars = upto10chars if upto10chars < 11 else 10
      return self.ytchannelid[:upto10chars]
      # return pathfs.get_sname_from_filename(self.ytvideospagefilename)
    if len(self.nname) < 11:
      self._sname = self.nname
      return self._sname
    self._sname = self.nname[:10]
    return self._sname

  @sname.setter
  def sname(self, shortname):
    if shortname is None:
      return
    if len(shortname) < 11:
      self._sname = shortname
    self._sname = shortname[:10]

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
      filename = pathfs.find_datedpage_filename_on_folder(self.ytchannelid, self.refdate)
      if filename is None:
        error_msg = 'Could not establish filename for ' + str(self)
        raise OSError(error_msg)
      return filename
    return pathfs.datedpage_filename(self.strdate, self.nname, self.ytchannelid)

  @property
  def ytvideospagefile_abspath(self):
    abspath = pathfs.get_datebased_ythtmlfiles_folderabspath(self.refdate)
    filename = self.ytvideospagefilename
    return os.path.join(abspath, filename)

  def get_html_text(self):
    if not os.path.isfile(self.ytvideospagefile_abspath):
      error_msg = 'File %s does not exist.' %self.ytvideospagefile_abspath
      raise OSError(error_msg)
    fp = open(self.ytvideospagefile_abspath, 'r', encoding='utf8')
    return fp.read()

  def find_set_n_get_sname_by_folder_or_None(self):
    ending = ' [%s].html' %self.ytchannelid
    abspath = pathfs.get_datebased_ythtmlfiles_folderabspath(self.refdate)
    entries = os.listdir(abspath)
    sought_entry = list(filter(lambda x : x.find(ending) > -1, entries))
    if len(sought_entry) != 1:
      return None
    filename = sought_entry[0]
    if len(filename) < 11 + 2 + len(ending):
      return None
    return filename[11 : - len(ending)]

  def get_htmltext_truncated(self, uptochar=50):
    htmltrun = self.get_html_text()
    if htmltrun is not None:
      if len(htmltrun) > uptochar:
        htmltrun = htmltrun[:uptochar]
    else:
      htmltrun = '[htmltext not found]'
    return htmltrun

  @property
  def murl(self):
    murl = pathfs.get_murl_from_ytchid(self.ytchannelid)
    if murl is None:
      # should never get here, but...
      error_msg = 'A wrong ytchannelid [%s] (id for [u]ser or [c]hannel in YouTube) came from database. Please, correct data and rerun.' % str(
        self.ytchannelid)
      raise ValueError(error_msg)
    return murl

  @property
  def absfolderpath(self):
    return pathfs.get_datebased_ythtmlfiles_folderabspath(self.refdate)

  @property
  def datedpage_filename(self):
    return pathfs.datedpage_filename(self.strdate, self.sname, self.ytchannelid)

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

  def get_dated_stat_fig_imgsrc_uptodate(self, ext='png'):
    htmlfilename = self.ytvideospagefilename
    name, _ = os.path.splitext(htmlfilename)
    imagefilename = name + '.' + ext
    return imagefilename

  @property
  def png_filename(self):
    return '%s.png' %self.ytchannelid

  @property
  def barchartpngfile_abspath(self):
    statichtml_folderabspath = pathfs.get_statichtml_folderabspath()
    png_abspath = os.path.join(statichtml_folderabspath, self.png_filename)
    return png_abspath

  @property
  def statimgfn(self):
    return self.get_dated_stat_fig_imgsrc_uptodate()

  def str2(self):
    strdict = {
      'nname': self.nname, 'murl': self.murl, 'videospageurl': self.videospageurl,
      'absfolderpath': self.absfolderpath, 'datedpage_filename': self.datedpage_filename,
      'datedpage_filepath': self.datedpage_filepath, 'datedpage_exists': self.datedpage_exists,
    }
    outstr = '''  nname          = %(nname)s
  murl           = %(murl)s  
  videospageurl  = %(videospageurl)s
  absfolderpath  = %(absfolderpath)s  
  dtdpg_filename = %(datedpage_filename)s
  dtdpg_filepath = %(datedpage_filepath)s
  datedpg_exists = %(datedpage_exists)s  
''' % (strdict)
    return outstr

  def __str__(self):
    htmltrun = self.get_htmltext_truncated(100)
    outdict = {
      'ytchannelid'  :self.ytchannelid, 'nname':self.nname, 'sname':self.sname,
      'filename':self.ytvideospagefilename,
      'ytvideospagefile_abspath':self.ytvideospagefile_abspath,
      'statimgfn': self.statimgfn,
      'htmltrun': htmltrun,
      'strdate' : self.strdate
    }
    outstr = '''YtVideosPage:
  ytchannelid = %(ytchannelid)s
  nname    = %(nname)s
  sname    = %(sname)s
  filename = %(filename)s
  abspath  = %(ytvideospagefile_abspath)s
  statimgfn= %(statimgfn)s 
  htmltrun = %(htmltrun)s
  refdate = %(strdate)s
    ''' %outdict
    return outstr

def transpose_sqlalchs_to_ytvideopages(sqlalch_ytchannels, refdate=None):
  ytvideopageobjs = []
  for sqlalch_channel in sqlalch_ytchannels:
    ytchannelid = sqlalch_channel.ytchannelid
    nname  = sqlalch_channel.nname
    ytvideospage = YtVideosPage(ytchannelid, nname, refdate)
    ytvideopageobjs.append(ytvideospage)
  return ytvideopageobjs

def adhoc_test():
  refdate = datetime.date(2020, 5, 27)
  ytchid = 'ubrunojonssen'
  nname = 'Bruno Jonssen'
  ytvideohtmlpage = YtVideosPage(ytchid, nname, refdate)
  print ('ytvideohtmlpage', ytvideohtmlpage)
  pass

def process():
  adhoc_test()

if __name__ == '__main__':
  process()