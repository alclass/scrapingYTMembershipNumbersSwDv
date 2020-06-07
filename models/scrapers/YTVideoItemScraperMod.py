#!/usr/bin/python3
'''
  This script scrapes video items through out the html video page
  Without parameter, it scrapes today's folder.
  An optional parameter --daysbefore=<n> scrapes n days before, if related folder exists.
'''
import bs4, os
import fs.textfunctions.scraper_helpers as scraphlp
import fs.textfunctions.regexp_helpers as regexp
from models.gen_models.YtVideosPageMod import YtVideosPage
from models.gen_models.YtVideoItemInfoMod import YtVideoItemInfo
from models.procdb.VideoItemInsertorMod import VideoItemInsertor

'''
<h3 class="yt-lockup-title ">
  <a class="yt-uix-sessionlink yt-uix-tile-link
    spf-link  yt-ui-ellipsis yt-ui-ellipsis-2" dir="ltr"
    title="Uma história bonita (#Pirula 333)"
    aria-describedby="description-id-908445"
    data-sessionlink="ei=UnjWXqGdIoTKxgTiupyYDg&amp;feature=c4-videos-u"
    href="/watch?v=eQ4mv7srfpY"
    rel="nofollow">
    Uma história bonita (#Pirula 333)
  </a>
  <span class="accessible-description" id="description-id-908445"> - Duração: 17 minutos.
  </span>
</h3>
'''

total_videoinfos = 0 # global here: TO-DO: improve this later on (ie, see if it's possible to avoid global)

class YTVideoItemScraper:

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

    self.resultlist = []
    self.htmlvideospagemetainfo = htmlvideospagemetainfo

  def get_html_text(self):
    file_abspath = self.htmlvideospagemetainfo.file_abspath
    if not os.path.isfile(file_abspath):
      error_msg = 'Error: in YTVideoItemScraper.get_html_text(): file [%s] does not exist and then can not be open/read' %file_abspath
      raise ValueError(error_msg)
    return open(file_abspath, 'r', encoding='utf8').read()

  def scrape_html_on_folder(self):
    self.htmlcontent = self.get_html_text()
    print('htmlcontent size', len(self.htmlcontent))
    bsoup = bs4.BeautifulSoup(self.htmlcontent, 'html.parser')
    for i, item in enumerate(bsoup.find_all('h3', attrs={'class' : 'yt-lockup-title'})):
      child = item.find('a') # , attrs=['title']
      if child is None:
        return
      ytvideoid = str(child['href'])
      pos = ytvideoid.find('=')
      if pos > -1:
        ytvideoid = ytvideoid[pos+1:] # it has prefix '/ watch?v='
      title = str(child['title'])
      if len(title) > 200: # in db it allows up to 255 chars: TO-DO: revise later on
        title = title[:200]
      print('-'*50)
      print (i, 'ytvideoid', ytvideoid)
      print('title', title)
      child = item.find('span', attrs={'class' : 'accessible-description'})
      try:
        print ('accessible-description', str(child.text))
      except AttributeError as e:
        pass
      videoinfo = YtVideoItemInfo(ytvideoid, title, self.htmlvideospagemetainfo.ytchannelid, self.htmlvideospagemetainfo.refdate)
      print(i, videoinfo)
      self.resultlist.append(videoinfo)

    for i, item in enumerate(bsoup.find_all('span', attrs={'class' : 'video-time'})):
      videoinfo = self.resultlist[i]
      duration_hms = item.text
      videoinfo.set_duration_in_sec_as_hms(duration_hms)

    for i, item in enumerate(bsoup.find_all('ul', attrs={'class' : 'yt-lockup-meta-info'})):
      lis = item.find_all('li')
      views = 0; published_time_ago = 'w/inf'
      for j, li in enumerate(lis):
        if j == 0:
          views = scraphlp.consume_left_side_int_number_w_optional_having_comma_or_point(li.text)
        else:
          published_time_ago = li.text
      videoinfo = self.resultlist[i]
      print ('views', views)
      videoinfo.views = views
      videoinfo.published_time_ago = published_time_ago

    for i, videoinfo in enumerate(self.resultlist):
      seq = i + 1
      print(seq, videoinfo)

  def save_to_db(self):
    global total_videoinfos
    total_videoinfos += 1
    for i, videoinfo in enumerate(self.resultlist):
      seq = i + 1
      vis = VideoItemInsertor(videoinfo)
      was_db_modified = vis.insert()
      print(total_videoinfos, seq, 'Saving', videoinfo.ytvideoid, videoinfo.title, 'MODIFIED', was_db_modified)

  def __str__(self):
    outstr = 'Scraper(ytchannelid=%s, refdate=%s)' %(self.htmlvideospagemetainfo.ytchannelid, self.htmlvideospagemetainfo.refdate)
    return outstr

def test1():
  pass

def process():
  '''
    adhoc_test's are found in adhoctasks.fs.autofind_adhoctests.py

  :return:
  '''
  pass

if __name__ == '__main__':
  process()