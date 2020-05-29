#!/usr/bin/python3
import datetime, os
import datefunctions.datefs as dtfs
import filefunctions.pathfunctions as pathfs

class YtVideosPage:

  def __init__(self, ytchid, nname=None, refdate=None):
    self.ytchid  = ytchid
    self.nname   = nname
    self._nOfSubscribers = None
    self.refdate = dtfs.get_refdate(refdate)

  @property
  def nOfSubscribers(self):
    return self._nOfSubscribers

  @nOfSubscribers.setter
  def nOfSubscribers(self, n):
    if n is None:
      return
    self._nOfSubscribers = n

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
      return filename
    return pathfs.datedpage_filename(self.strdate, self.nname, self.ytchid)

  def get_statistic_fig_imgsrc_uptodate(self, ext='png'):
    htmlfilename = self.ytvideospagefilename
    name, _ = os.path.splitext(htmlfilename)
    imagefilename = name + '.' + ext
    return imagefilename

  @property
  def statimgfn(self):
    return self.get_statistic_fig_imgsrc_uptodate()

  @property
  def ytvideospagefile_abspath(self):
    abspath = pathfs.get_datebased_ythtmlfiles_folderabspath(self.refdate)
    filename = self.ytvideospagefilename
    return os.path.join(abspath, filename)

  def get_html_text(self):
    try:
      fp = open(self.ytvideospagefile_abspath, 'r', encoding='utf8')
      return fp.read()
    except OSError:
      pass
    return None

  def get_htmltext_truncated(self, uptochar=50):
    htmltrun = self.get_html_text()
    if htmltrun is not None:
      if len(htmltrun) > uptochar:
        htmltrun = htmltrun[:uptochar]
    else:
      htmltrun = '[htmltext not found]'
    return htmltrun

  def __str__(self):
    htmltrun = self.get_htmltext_truncated(100)
    outdict = {
      'ytchid'  :self.ytchid,'nname':self.nname,'sname':self.sname,
      'filename':self.ytvideospagefilename,
      'ytvideospagefile_abspath':self.ytvideospagefile_abspath,
      'statimgfn': self.statimgfn,
      'htmltrun': htmltrun,
      'strdate' : self.strdate
    }
    outstr = '''YtVideosPage:
  ytchid   = %(ytchid)s
  nname    = %(nname)s
  sname    = %(sname)s
  filename = %(filename)s
  abspath  = %(ytvideospagefile_abspath)s
  statimgfn= %(statimgfn)s 
  htmltrun = %(htmltrun)s
  refdate = %(strdate)s
    ''' %outdict
    return outstr

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