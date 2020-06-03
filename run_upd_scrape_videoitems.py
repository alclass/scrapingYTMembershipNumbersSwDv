#!/usr/bin/python3
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
import bs4
import fs.datefunctions.datefs as dtfs
import fs.textfunctions.scraper_helpers as scraphlp
from models.gen_models.YtVideosPageMod import YtVideosPage
from models.gen_models.YtVideoItemInfoMod import YtVideoItemInfo

resultlist = []
def parse_videopage_for_videoitems(htmlcontent):
  print('htmlcontent size', len(htmlcontent))
  bsoup = bs4.BeautifulSoup(htmlcontent, 'html.parser')
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
    videoinfo = YtVideoItemInfo(ytvideoid, title)
    resultlist.append(videoinfo)

  for i, item in enumerate(bsoup.find_all('span', attrs={'class' : 'video-time'})):
    videoinfo = resultlist[i]
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

    videoinfo = resultlist[i]
    print ('views', views)
    videoinfo.views = views
    videoinfo.published_time_ago = published_time_ago

  for videoinfo in resultlist:
    print(videoinfo)

def scrape_html_on_folder(ytchannelid):
  refdate = dtfs.get_refdate()
  ytchannelvideospage = YtVideosPage(ytchannelid, None, refdate)
  sname = ytchannelvideospage.find_set_n_get_sname_by_folder_or_None()
  if sname is None:
    print(ytchannelid, 'file does exist on data folder.')
    return
  print ('['+sname+']')
  htmlcontent = ytchannelvideospage.get_html_text()
  # print (htmlcontent)
  parse_videopage_for_videoitems(htmlcontent)

def test1():
  o = YtVideoItemInfo('ytid', 'title bla')
  o.views = '123,123'
  print (o)

def process():
  # ytchannelid = 'upgjr23'
  ytchannelid = 'ueduardoamoreira'
  scrape_html_on_folder(ytchannelid)
  # test1()

if __name__ == '__main__':
  process()
