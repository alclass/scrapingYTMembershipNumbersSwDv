#!/usr/bin/python3
import bs4, collections, json, os, string
import datefunctions.datefs as dtfs
import readHtmlsOnFolder as readmod

SUBSCRIBERS_NUMBER_HTMLCLASSNAME = 'yt-subscription-button-subscriber-count-branded-horizontal'
'''
<span class="yt-subscription-button-subscriber-count-branded-horizontal subscribed yt-uix-tooltip" 
  title="433 mil" tabindex="0" aria-label="433 mil inscritos">433 mil</span> 
'''
SubscribersStatNT = collections.namedtuple('SubscribersStatNT', ['nOfSubscribers', 'strline'])

def extract_number_from_arialabel(arialabel):
  numberstr = ''
  for c in arialabel:
    if c in string.digits:
      numberstr += c
    elif c in [',','.']:
      numberstr += '.'
    else:
      break
  if numberstr == '':
    return -1
  number = float(numberstr)
  if arialabel.find('mil') > -1:
    number = number * 1000
  elif arialabel.find('mi') > -1:
    number = number * 1000 * 1000
  return int(number) # number of subscribers is an int

class HTMLScraper:

  def __init__(self, refdate=None):
    self.refdate = dtfs.get_refdate(refdate)
    # self.strdate is @property
    self.reader = readmod.YtVideoPagesTraversal(refdate)
    self.counter = 0
    # self.scrapingResuls = []
    print ('Please, wait a moment; there are', self.reader.n_of_pages, 'pages to be processed.')
    self.scrape_to_inner_vars()

  @property
  def strdate(self):
    return dtfs.get_strdate(self.refdate)

  def scrape_to_inner_vars(self):
    for ytvideopagesobj in self.reader.ytvideopageobj_list:
      self.counter += 1
      self.scrape_subscribers_number(ytvideopagesobj)
      # self.scrape_individual_video_views(htmlfilename, content)

  def scrape_subscribers_number(self, ytvideopageobj):
    htmlfilename = ytvideopageobj.ytvideospagefilename
    # print('Parsing =>', htmlfilename)
    sname   = ytvideopageobj.sname
    content = ytvideopageobj.get_html_text()
    extlessname = os.path.splitext(htmlfilename)[0]
    bsoup = bs4.BeautifulSoup(content, 'html.parser')
    # result, if found, is a bs4.element.Tag object
    result = bsoup.find('span', attrs={'class':SUBSCRIBERS_NUMBER_HTMLCLASSNAME})
    if result is None:
      print('Subscribers number not found for', extlessname)
      return
    statdate = extlessname[:10]
    strline  = '[not found]'
    try:
      arialabel = str(result['aria-label'])
      strline = arialabel
      strline = strline.replace('\\xa0', '')
      number = extract_number_from_arialabel(arialabel)
      nOfSubscribers = number # even if it's -1 (case it's not found)
    except IndexError:
      nOfSubscribers = -1
    # subsrecord = SubscribersStatNT(nOfSubscribers=nOfSubscribers, strline=strline)
    # ytvideopageobj.scrapedrecord = subsrecord
    # self.scrapingResuls.append(subsrecord)
    ytvideopageobj.nOfSubscribers = nOfSubscribers
    ytvideopageobj.nOfSubscribers_strline = strline

  def print_scraping_results(self):
    # for i, subsrecord in enumerate(self.scrapingResuls):
    for i, ytvideopageobj in enumerate(self.reader.ytvideopageobj_list):
      # subsrecord = ytvideopageobj.scrapedrecord
      print(i+1, ytvideopageobj.refdate, ytvideopageobj.sname, 'has', ytvideopageobj.nOfSubscribers, ytvideopageobj.nOfSubscribers_strline)

  def saveJson(self):
    outlist = []
    for i, ytvideopageobj in enumerate(self.reader.ytvideopageobj_list):
      dictrecord = ytvideopageobj.as_dict_for_json()
      outlist.append(dictrecord)
    outfilename = self.strdate + ' test.json'
    outfile = open(outfilename, 'w', encoding='utf8')
    outtext = json.dumps(str(outlist))
    outfile.write(outtext)
    outfile.close()

  def scrape_individual_video_views(self, htmlfilename, content):
    '''
    Not used by now
    ===============
    :param htmlfilename:
    :param content:
    :return:
    '''
    extlessname = os.path.splitext(htmlfilename)[0]
    bsoup = bs4.BeautifulSoup(content, 'html.parser')
    result = bsoup.find('span', attrs={'class':SUBSCRIBERS_NUMBER_HTMLCLASSNAME})
    if result is None:
      print('Subscribers number not found for', extlessname)
      return

def process():
  scraper = HTMLScraper()
  scraper.print_scraping_results()
  print ('len =', len(scraper.reader.ytvideopageobj_list))

if __name__ == '__main__':
  process()
