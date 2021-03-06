#!/usr/bin/env python3
import os
import fs.datefunctions.datefs as dtfs
import fs.filefunctions.autofinders as autof
import fs.filefunctions.pathfunctions as pathfs
import fs.textfunctions.regexp_helpers as regexp


def does_filename_ext_belong_to_ht_htm_html_shtml(word):
  """
    lambdaentryhashtmlext  = lambda word : pathfs.does_filename_have_ext_from_extlist(word, [<list>])
  :param word:
  :return:
  """
  htmls_extlist = ['ht', 'htm', 'html', 'shtml']
  return pathfs.does_filename_have_ext_from_extlist(word, htmls_extlist)


class InvalidNamedHtmlOnFolder(ValueError):
  """
  A helper exception-class that is used from some points below
  """
  pass


class HtmlInDateFolder:
  """

  """

  def __init__(self, filename):
    self.filename = filename
    self.verify_filename()
    # properties derivable from filename and instanced, ie, built once:
    self._refdate = None
    self._sname = None
    self._ytchannelid = None
    self.filename_is_out_of_convention = False
    self.instanciate_derivable()

  def verify_filename(self):
    if self.filename is None:
      error_msg = 'Error: HtmlInDateFolder received parameter filename as None'
      raise ValueError(error_msg)
    if os.sep in self.filename:  # filename can not have os.sep in it
      _, self.filename = os.path.split(self.filename)

  def instanciate_derivable(self):
    """

    # properties derivable from filename and not-instanced, ie, built once are:
      refdate, sname and ytchannelid
    Obs: it suffices to issue one of them that the others are instanced too

    # properties derivable from filename and not-instanced, ie, built per request:
    # => file_abspath
    # => foldername
    # => folder_abspath
    :return:
    """

    _ = self._ytchannelid

  def set_date_sname_n_ytchannelid(self):
    name_without_ext, _ = os.path.splitext(self.filename)
    strdate = name_without_ext[:10]
    self._refdate = dtfs.get_refdate_from_strdate(strdate)
    ytchannelid = regexp.find_ytchannelid_within_brackets_in_filename(name_without_ext)
    if ytchannelid is None:
      self.filename_is_out_of_convention = True
      return
    ytchannelid = ytchannelid.lstrip('[').rstrip(']')
    self._ytchannelid = ytchannelid
    sname = name_without_ext[11: -(len(ytchannelid)+2)]  # plus 2 is for [] (brackets)
    _sname = sname.strip(' ')
    if len(_sname) > 10:
      error_msg = 'Error: when trying to extract sname (%s) from filename (%s) it came out bigger than 10 characters.' \
                  % (sname, self.filename)
      raise ValueError(error_msg)
    self._sname = sname

  @property
  def sname(self):
    if self._sname is None:
      self.set_date_sname_n_ytchannelid()
    return self._sname

  @property
  def ytchannelid(self):
    if self._ytchannelid is None:
      self.set_date_sname_n_ytchannelid()
    return self._ytchannelid

  @property
  def refdate(self):
    if self._refdate is None:
      self.set_date_sname_n_ytchannelid()
    return self._refdate

  @property
  def infodate(self):
    return self.refdate

  # derivable : foldername
  @property
  def foldername(self):
    """
    This is 2nd level (and last) foldername
    :return:
    """

    if self.refdate is None:
      error_msg = 'Error: HtmlInDateFolder has refdate as None; refdate is fundamental' \
                  ' for knowing foldername nad folderpath.'
      raise InvalidNamedHtmlOnFolder(error_msg)
      # return None
    try:
      yyyymmdd = str(self.refdate)
      return yyyymmdd
    except IndexError:
      pass
    return None

  @property
  def foldername_level1(self):
    """
    This is 2nd level (and last) foldername
    :return:
    """

    if self.refdate is None:
      error_msg = 'Error: HtmlInDateFolder has refdate as None; refdate is fundamental' \
                  ' for knowing foldername nad folderpath.'
      raise InvalidNamedHtmlOnFolder(error_msg)
      # return None
    try:
      yyyymm = str(self.refdate)[:7]
      return yyyymm
    except IndexError:
      pass
    return None

  # derivable : folder_abspath
  @property
  def folder_abspath(self):
    """
      folder_abspath is level2_abspath
    :return:
    """
    level3folderabspath = autof.mount_level3folderabspath_with_date(self.refdate)
    if level3folderabspath is None:
      return None
    return level3folderabspath

  # derivable : file_abspath
  @property
  def file_abspath(self):
    if self.folder_abspath is None:
      return None
    return os.path.join(self.folder_abspath, self.filename)

  def asdict(self):
    asdict = {
      'filename': self.filename,
      'refdate': self.refdate,
      'sname': self.sname,
      'ytchannelid': self.ytchannelid,
      'foldername': self.foldername,
      'folder_abspath': self.folder_abspath,
      'file_abspath': self.file_abspath,
    }
    return asdict

  def __str__(self):
    outstr = '''HtmlInDateFolder:
  filename = %(filename)s
  refdate  = %(refdate)s 
  sname    = %(sname)s 
  ytchannelid    = %(ytchannelid)s
  foldername     = %(foldername)s
  folder_abspath = %(folder_abspath)s
  file_abspath   = %(file_abspath)s 
''' % self.asdict()
    return outstr


def test1():
  """
  This docstring it to help develop unittests later on
  htmlfileobj HtmlInDateFolder:
    filename = 2020-06-14 Paulo Ghir [upgjr23].html
    refdate  = 2020-06-14
    sname    = Paulo Ghir
    ytchannelid    = upgjr23
    foldername     = 2020-06-14
    folder_abspath = /media/friend/SAMSUNG/Ytvideos BRA Politics/z Other ytchannels/000_scrape_ytdata/2020-06/2020-06-14
    file_abspath   = /media/friend/SAMSUNG/Ytvideos BRA Politics/z Other ytchannels/000_scrape_ytdata/2020-06/2020-06-14
    /2020-06-14 Paulo Ghir [upgjr23].html
  :return:
  """
  filename = '2020-06-14 Eduardo M [umoreira].html'
  htmlfileobj = HtmlInDateFolder(filename)
  print('htmlfileobj', htmlfileobj)


def process():
  test1()


if __name__ == '__main__':
  process()
