#!/usr/bin/python3
'''
  This script scrapes video items through out the html video page
  Without parameter, it scrapes today's folder.
  An optional parameter --daysbefore=<n> scrapes n days before, if related folder exists.
'''
import bs4, os, sys
import fs.datefunctions.datefs as dtfs
import fs.filefunctions.autofinders as autofind
import fs.textfunctions.scraper_helpers as scraphlp
import fs.textfunctions.regexp_helpers as regexp

from models.gen_models.YtVideosPageMod import YtVideosPage
from models.gen_models.YtVideoItemInfoMod import YtVideoItemInfo
# from models.sa_models.ytchannelsubscribers_samodels import YTVideoItemInfoSA
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

  def __init__(self, ytchannelid, refdate=None, sname=None):
    self.resultlist = []
    self.ytchannelid = ytchannelid
    self.refdate = dtfs.return_refdate_as_datetimedate_or_today(refdate)
    if sname is None:
      sname = self.ytchannelvideospage.find_set_n_get_sname_by_folder_or_None()
      print(self.ytchannelid, 'file does exist on data folder.')
      # TO-DO: log info in a logfile
      return
    self.sname = sname
    self.ytchannelvideospage = YtVideosPage(self.ytchannelid, None, self.refdate)
    self.ytchannelvideospage.sname = self.sname
    print ('['+self.sname+']', self.ytchannelid, self.refdate)

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
      videoinfo = YtVideoItemInfo(ytvideoid, title, self.ytchannelid, self.refdate)
      print(i, videoinfo)
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

  def save_to_db(self):
    global total_videoinfos
    total_videoinfos += 1
    for i, videoinfo in enumerate(self.resultlist):
      seq = i + 1
      vis = VideoItemInsertor(videoinfo)
      vis.insert()
      print(total_videoinfos, seq, 'Saving', videoinfo.ytvideoid, videoinfo.title)

  def __str__(self):
    outstr = 'Scraper(ytchannelid=%s, refdate=%s)' %(self.ytchannelid, self.refdate)
    return outstr

def test1():
  pass

def walk_thru_dates():
  level2_foldernames = autofind.find_yyyymmdd_level2_foldernames()
  for i, level2_foldername in enumerate(level2_foldernames):
    seq = i+1
    print (seq, level2_foldername)

def walk_thru_date_folders():
  dates_n_abspaths_od = autofind.get_ordered_dict_with_dates_n_abspaths()
  # print (dates_n_abspaths_od)
  html_counter = 0
  for i, strdate in enumerate(dates_n_abspaths_od):
    seq_dates = i + 1
    datefolder_abspath = dates_n_abspaths_od[strdate]
    print ('-'*50)
    print(strdate, datefolder_abspath)
    print ('-'*50)
    entries = os.listdir(datefolder_abspath)
    entries = sorted(entries)
    for htmlfilename in entries:
      _, ext = os.path.splitext(htmlfilename)
      if ext != '.html':
        continue
      html_counter += 1
      print (html_counter, htmlfilename)
      name_without_ext, _ = os.path.splitext(htmlfilename)
      # ytchannelid = regexphlp.find_ytchannelid_within_brackets_in_filename(name_without_ext)
      refdate, sname, ytchannelid = regexp.find_triple_date_sname_n_ytchid_in_filename(name_without_ext)
      # YtVideoItemInfo(ytvideoid, title, ytchannelid, info_refdate)
      # YTVideoItemScraper(ytchannelid, refdate = None, sname = None)
      scraper = YTVideoItemScraper(ytchannelid, refdate, sname)
      print(scraper)
      scraper.scrape_html_on_folder()
      scraper.save_to_db()
    #if seq_dates > 1:
    print (seq_dates, 'st/nd/rd/th date: on:', strdate)
    # return

def test1():
  # ytchannelid = 'upgjr23'
  ytchannelid = 'ueduardoamoreira'
  refdate = get_refdate_from_param_n_days_before_or_today()
  videoitemscraper = YTVideoItemScraper(ytchannelid, refdate)
  videoitemscraper.scrape_html_on_folder()

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
  print ('param refdate', refdate)
  return refdate

def process():
  refdate = get_refdate_from_param_n_days_before_or_today()
  # test1()
  walk_thru_date_folders()
  # walk_thru_dates()

if __name__ == '__main__':
  process()
