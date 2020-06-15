#!/usr/bin/python3
'''
  This script scrapes video items through out the html video page
  Without parameter, it scrapes today's folder.
  An optional parameter --daysbefore=<n> scrapes n days before, if related folder exists.
'''
import bs4, json, os
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
    # print('htmlcontent size', len(self.htmlcontent))
    bsoup = bs4.BeautifulSoup(self.htmlcontent, 'html.parser')
    entered_loop = False
    for i, item in enumerate(bsoup.find_all('h3', attrs={'class': 'yt-lockup-title'})):
      entered_loop = True
    if not entered_loop:
      self.bsoup_does_not_have_info = True
      print ('bsoup find all is empty for ', self.htmlvideospagemetainfo.filename)

  def __str__(self):
    outstr = 'Scraper(ytchannelid=%s, refdate=%s)' %(self.htmlvideospagemetainfo.ytchannelid, self.htmlvideospagemetainfo.refdate)
    return outstr

def run_thu_the_htmls_on_folder():
  '''
    ytchannelid = 'upgjr23'

  :return:
  '''
  n_of_empties = 0
  empty_ones = []
  filepaths = autofind.get_htmlfilepaths_from_date()
  for filepath in filepaths:
    htmlvideospagemetainfo = HtmlInDateFolder(filepath)
    htmlfileobj = YTVideoItemBsoupEmpty(htmlvideospagemetainfo)
    htmlfileobj.scrape_html_on_folder()
    if htmlfileobj.bsoup_does_not_have_info:
      n_of_empties += 1
      empty_ones.append(filepath)
  print('-' * 50)
  print('n_of_empties =', n_of_empties)

def test1():
  for i in [1]:
    print('for with loops')
  else:
    print ('else')

def process():
  '''
    adhoc_test's are found in adhoctasks.fs.autofind_adhoctests.py

  :return:
  '''
  run_thu_the_htmls_on_folder()
  # test1()


if __name__ == '__main__':
  process()
