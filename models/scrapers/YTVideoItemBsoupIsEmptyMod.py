#!/usr/bin/python3
'''
  This script was copied and simplified from that one that scrapes video items
    in the DOM inside the html video page,  It works only from today's directory.

  Its objective is to find out html files that are unscrapeable by the DOM,
    upon finding such a file, the strategy is to delete the file and redownload it,
    checking it again later on in a new try.

  The system will try a redownload up to 3 times, the end result is a message informing
    how many files are still unscrapeable.
    (Hopefully, 3 times are enough to have all files scrapeable.)
'''
import bs4, os, sys, time
from models.gen_models.HtmlInDateFolderMod import HtmlInDateFolder
import fs.filefunctions.autofinders as autofind

class YTVideoItemBsoupEmpty:

  def __init__(self, htmlvideospagemetainfo): # filename = None
    '''
    Example of HtmlInDateFolder:
      filename = 2020-06-07 Vozes da D [uhumbertocostapt].html
      refdate  = 2020-06-07
      sname    = Vozes da D
      ytchannelid    = uhumbertocostapt
      foldername     = 2020-06
      folder_abspath = /media/friend/SAMSUNG/Ytvideos BRA Politics/z Other ytchannels/000_scrape_ytdata/2020-06/2020-06-07
      file_abspath   = /media/friend/SAMSUNG/Ytvideos BRA Politics/z Other ytchannels/000_scrape_ytdata/2020-06/2020-06-07/2020-06-07 Vozes da D [uhumbertocostapt].html

    :param htmlvideospagemetainfo:
    '''

    self.bsoup_does_not_have_info = False
    self.htmlvideospagemetainfo = htmlvideospagemetainfo

  def get_html_text(self):
    file_abspath = self.htmlvideospagemetainfo.file_abspath
    if not os.path.isfile(file_abspath):
      error_msg = 'Error: in YTVideoItemScraper.get_html_text(): file [%s] does not exist and then can not be open/read' %file_abspath
      raise ValueError(error_msg)
    return open(file_abspath, 'r', encoding='utf8').read()

  def scrape_html_on_folder(self):
    self.htmlcontent = self.get_html_text()
    bsoup = bs4.BeautifulSoup(self.htmlcontent, 'html.parser')
    entered_loop = False
    for i, item in enumerate(bsoup.find_all('h3', attrs={'class': 'yt-lockup-title'})):
      entered_loop = True
    if not entered_loop:
      self.bsoup_does_not_have_info = True

  def __str__(self):
    outstr = 'Empty Finder for %s %s' %(self.htmlvideospagemetainfo.ytchannelid, self.htmlvideospagemetainfo.refdate)
    return outstr

class RunEmtpyFinderThuFolder:

  def __init__(self): # filename = None
    self.n_of_empties = 0
    self.empty_ones = []

  def run_thu_folder_htmls(self, do_delete=True):
    '''
      ytchannelid = 'upgjr23'
    :return:
    '''
    self.n_of_empties = 0
    self.empty_ones = []
    filepaths = autofind.get_htmlfilepaths_from_date()
    for i, filepath in enumerate(filepaths):
      htmlvideospagemetainfo = HtmlInDateFolder(filepath)
      htmlfileobj = YTVideoItemBsoupEmpty(htmlvideospagemetainfo)
      printline = ' :: Scraping [' + str(i+1) + ']' + htmlfileobj.htmlvideospagemetainfo.filename
      htmlfileobj.scrape_html_on_folder()
      if htmlfileobj.bsoup_does_not_have_info:
        printline = ' DOM-EMPTY ' + printline
        self.n_of_empties += 1
        self.empty_ones.append(filepath)
        if do_delete:
          print(self.n_of_empties, 'Deleting', filepath)
          os.remove(filepath)
      else:
        printline = ' NOT DOM-EMPTY ' + printline
      print(printline)

  def report(self):
    print('-' * 50)
    print('n_of_empties =', self.n_of_empties)

def test1():
  for i in [1]:
    print('for with loops')
  else:
    print ('else')

def get_delete_arg():
  for arg in sys.argv:
    if arg.startswith('--dodel'):
      return True
  return False

def process():
  '''
  :return:
  '''
  pass

if __name__ == '__main__':
  process()
