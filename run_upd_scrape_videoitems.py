#!/usr/bin/python3
'''
  This script scrapes video items through out the html video page
  Without parameter, it scrapes today's folder.
  An optional parameter --daysbefore=<n> scrapes n days before, if related folder exists.
'''

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
import bs4, sys
import fs.datefunctions.datefs as dtfs
import fs.textfunctions.scraper_helpers as scraphlp
from models.gen_models.YtVideosPageMod import YtVideosPage
from models.gen_models.YtVideoItemInfoMod import YtVideoItemInfo


class YTVideoItemScraper:

  def __init__(self, ytchannelid, refdate=None):
    self.resultlist = []
    self.ytchannelid = ytchannelid
    self.refdate = dtfs.return_refdate_as_datetimedate_or_today(refdate)
    self.ytchannelvideospage = YtVideosPage(self.ytchannelid, None, self.refdate)
    sname = self.ytchannelvideospage.find_set_n_get_sname_by_folder_or_None()
    if sname is None:
      print(self.ytchannelid, 'file does exist on data folder.')
      return
    print ('['+sname+']')

  def scrape_html_on_folder(self):
    self.htmlcontent = self.ytchannelvideospage.get_html_text()
    self.parse_videopage_for_videoitems()

  def parse_videopage_for_videoitems(self):
    print('htmlcontent size', len(self.htmlcontent))
    bsoup = bs4.BeautifulSoup(self.htmlcontent, 'html.parser')
    for i, item in enumerate(bsoup.find_all('h3', attrs={'class' : 'yt-lockup-title'})):
      child = item.find('a') # , attrs=['title']
      if child is None:
        return
      href_ytvideoid = str(child['href'])
      ytvideoid = href_ytvideoid[len('/ watch?v=') : ]
      title = str(child['title'])
      print('-'*50)
      print (i, 'ytvideoid', ytvideoid)
      print('title', title)
      child = item.find('span', attrs={'class' : 'accessible-description'})
      print ('accessible-description', str(child.text))
      videoinfo = YtVideoItemInfo(ytvideoid, title, self.refdate, self.ytchannelid)
      self.resultlist.append(videoinfo)

    for i, item in enumerate(bsoup.find_all('span', attrs={'class' : 'video-time'})):
      videoinfo = self.resultlist[i]
      duration_hms = item.text
      # print (i, duration_m_s)
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

def test1():
  o = YtVideoItemInfo('ytid', 'title bla')
  o.views = '123,123'
  print (o)

def show_help_n_exit():
  print (__doc__)
  sys.exit()

def get_args():
  for arg in sys.argv:
    if arg.startswith('-h'):
      show_help_n_exit()
    elif arg.startswith('--daysbefore='):
      try:
        pos = len('--daysbefore=')
        rightside = arg[pos:]
        n_days_before = int(rightside)
      except ValueError:
        print ('Error: parameter --daysbefore=<n> expects an integer as input (entered %s).' %rightside)
        sys.exit()
      return n_days_before
  return None

def get_refdate_from_param_n_days_before_or_today():
  n_days_before = get_args()
  refdate = dtfs.return_refdate_as_datetimedate_or_today()
  if n_days_before is not None:
    refdate = dtfs.calc_past_date_from_refdate_back_n_days(refdate, n_days_before)
  print ('refdate', refdate)
  return refdate

def process():
  # test1()   # ytchannelid = 'upgjr23'
  ytchannelid = 'ueduardoamoreira'
  refdate = get_refdate_from_param_n_days_before_or_today()
  videoitemscraper = YTVideoItemScraper(ytchannelid, refdate)
  videoitemscraper.scrape_html_on_folder()

if __name__ == '__main__':
  process()
