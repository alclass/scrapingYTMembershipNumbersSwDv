#!/usr/bin/python3
import datetime, os
import fs.datefunctions.datefs as dtfs
import fs.filefunctions.pathfunctions as pathfs
import fs.db.sqlalchdb.dbfetchesmod as dbfetch
from fs.db.sqlalchdb.sqlalchemy_conn import Session
from models.sa_models.ytchannelsubscribers_samodels import YTDailySubscribersSA

class YtVideosPage:

  def __init__(self, ytchannelid, nname=None, refdate=None):
    self.ytchannelid     = ytchannelid
    self.nname           = nname
    self._sname           = None
    self.refdate = dtfs.get_refdate(refdate)
    self._nOfSubscribers = None
    self._days_n_subscribers = []
    self._downloadable_on_date = None # to set 'lazily' as boolean

  @property
  def nOfSubscribers(self):
    return self._nOfSubscribers

  @nOfSubscribers.setter
  def nOfSubscribers(self, n):
    if n is None:
      return
    self._nOfSubscribers = n

  def dbsave_subscribers_number(self, subscribers_number):
    session = Session()
    subs = session.query(YTDailySubscribersSA).\
      filter(YTDailySubscribersSA.infodate==self.refdate). \
      filter(YTDailySubscribersSA.ytchannelid == self.ytchannelid). \
      first()
    changed = False
    if subs:
      if subs.subscribers != subscribers_number:
        subs.subscribers = subscribers_number
        changed = True
    else:
      subs = YTDailySubscribersSA()
      subs.ytchannelid = self.ytchannelid
      subs.subscribers = subscribers_number
      subs.infodate = self.refdate
      session.add(subs)
      changed = True
    if changed:
      session.commit()
      self.nOfSubscribers = subscribers_number
      print(' * Subscribers DB-written *')
    else:
      print(' *** Subscribers NOT DB-written ***')
    session.close()
    return changed

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
      if len(self._sname) > 10:
        self._sname = self._sname[:10]
      if self._sname.endswith(' '):
        self._sname = self._sname.strip(' ')
      return self._sname
    wname = self.nname
    if wname is not None:
      if len(wname) > 10:
        wname = wname[:10]
      wname = wname.strip(' ')
      self._sname = wname
      return self._sname
    # try to find it in folders (this case will only happen if for instances there is a corresponding file on folder which may, in some cases, be empty.)
    sname = pathfs.get_sname_from_filename(self.filename)
    return sname

  @sname.setter
  def sname(self, shortname):
    if shortname is None:
      return
    self._sname = shortname
    if len(shortname) > 10:
      self._sname = shortname[:10]
    if self._sname.endswith(' '):
      self._sname = self._sname.strip(' ')

  @property
  def downloadable_on_date(self):
    if self._downloadable_on_date is not None:
      return self._downloadable_on_date

  @downloadable_on_date.setter
  def downloadable_on_date(self, boolvalue):
    self._downloadable_on_date = boolvalue

  @property
  def strdate(self):
    return dtfs.get_strdate(self.refdate)

  @property
  def filesdatetime(self):
    tupl = os.stat(self.datedpage_filepath)
    return tupl

  @property
  def filename(self):
    '''
  Notice an import difference here:
    1) if nname is None, filename should exist on folder and should be retrieve by dir lookup
    2) if nname is given, filename is returned even if it does not exist, for it is about to be created

      filename = pathfs.find_datedpage_filename_on_folder(self.ytchannelid, self.refdate)
      if filename is None:
        error_msg = 'Could not establish filename for ' + str(self)
        raise OSError(error_msg)
      return filename

  :return:
    '''
    if self._sname is None:
      self.find_set_n_get_sname_by_folder_or_None()
      if self._sname is None:
        # this will happen when a ytchannel from db is trying to find a corresponding youtube videos page on a certain date and that does not exist
        self._sname = 'in-wait'
        #error_msg = 'Error: sname could not be established in @property filename [class YtVideosPage]'
        #raise ValueError(error_msg)
    return pathfs.datedpage_filename(self.strdate, self._sname, self.ytchannelid)

  def set_sname_by_nname(self):
    if self.nname is None:
      return
    self._sname = self.nname if len(self.nname) < 11 else self.nname[:10]

  @property
  def ytvideospagefile_abspath(self):
    abspath = pathfs.get_datebased_ythtmlfiles_folderabspath(self.refdate)
    filename = self.filename
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
    if len(sought_entry) == 1:
      filename = sought_entry[0]
      if len(filename) < 11 + 2 + len(ending):
        return None
      sname = filename[11 : - len(ending)]
      if len(sname) > 10: sname = sname[:10]
      if sname.endswith(' '): sname = sname.strip(' ')
      self._sname = sname
      return sname
    if self.nname is None:
      return None
    return self.nname if len(self.nname) < 11 else self.nname[:10]

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
    sname = self.sname
    if sname is None:
      error_msg = '@property datedpage has sname as None (strdate=%s, sname=%s, ytchannelid=%s)' %(self.strdate, self.sname, self.ytchannelid)
      raise ValueError(error_msg)
    return pathfs.datedpage_filename(self.strdate, self.sname, self.ytchannelid)

  @property
  def datedpage_filepath(self):
    datedagefn = self.datedpage_filename
    if datedagefn is None:
      error_msg = '@property datedpage_filepath returned None'
      raise ValueError(error_msg)
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
    htmlfilename = self.filename
    name, _ = os.path.splitext(htmlfilename)
    imagefilename = name + '.' + ext
    return imagefilename

  @property
  def png_filename(self):
    return '%s.png' %self.ytchannelid

  @property
  def barchartpngfile_abspath(self):
    statichtml_folderabspath = pathfs.get_statichtml_folderabspath()
    pngfolder_abspath = os.path.join(statichtml_folderabspath, 'img')
    if not os.path.isdir(pngfolder_abspath):
      os.makedirs(pngfolder_abspath)
    pngfile_abspath = os.path.join(pngfolder_abspath, self.png_filename)
    return pngfile_abspath

  @property
  def statimgfn(self):
    return self.get_dated_stat_fig_imgsrc_uptodate()

  def fetch_dbytchannel_n_transpose(self):
    return dbfetch.fetch_ytchannel_by_ytchannelid_n_transpose(self.ytchannelid, self)

  def transpose(self, ytchannelsa):
    # transposed = copy.copy(self)  # this is an immutable manner to transpose to a copy, not the current on-place mutable object
    self._downloadable_on_date = ytchannelsa.is_downloadable_on_date()
    # for the time being, change will mutate on-place:
    # return transposed

  def __str__(self):
    htmltrun = '[File missing or does not exist yet.]'
    try:
      htmltrun = self.get_htmltext_truncated(100)
    except OSError:
      pass
    outdict = {
      'ytchannelid'  :self.ytchannelid, 'nname':self.nname, 'sname':self.sname,
      'filename':self.filename,
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