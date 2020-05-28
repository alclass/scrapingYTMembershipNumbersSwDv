#!/usr/bin/python3
import bs4, os
import textfunctions.regexp_helpers as regexp
from YtVideosPageMod import YtVideosPage

SUBSCRIBERS_NUMBER_HTMLCLASSNAME = 'yt-subscription-button-subscriber-count-branded-horizontal'
'''
  <span class="yt-subscription-button-subscriber-count-branded-horizontal subscribed yt-uix-tooltip" 
    title="433 mil" tabindex="0" aria-label="433 mil inscritos">433 mil</span>
Alternatively:  
  <yt-formatted-string id="subscriber-count" class="style-scope ytd-c4-tabbed-header-renderer">365&nbsp;mil inscritos</yt-formatted-string>  
'''
# SubscribersStatNT = collections.namedtuple('SubscribersStatNT', ['nOfSubscribers', 'strline'])

def extract_number_from_known_pieces(phrase):
  if phrase is None or type(phrase) != str:
    return None
  phrase = phrase.strip()
  if len(phrase) == 0:
    return None
  pp = phrase.split(' ')
  firstword = pp[0]
  if firstword.find(',') > -1:
    firstword = firstword.replace(',', '.')
  try:
    number = float(firstword)
  except ValueError:
    number = regexp.consume_left_side_float_number(firstword)
    if number is None:
      return None
  # subscribersnumber_found = True
  if len(pp) > 1:
    if phrase.find('mil'):
      return int(number) * 1000
    elif phrase.find('k'):
      return int(number) * 1000
    elif phrase.find('mi'):
      return int(number) * 1000 * 1000
  return int(number)

class GoParser:

  def __init__(self, bsoup):
    self.bsoup = bsoup  # bsoup is a Beautiful Soup object with the whole html in it
    self.subscribersnumber = None
    self.goparse()

  def goparse(self):
    '''

    :return:
    '''
    self.try_approch_1_span_n_class()
    if self.subscribersnumber is None:
      self.try_approch_2_id_subscriber_count()

  def try_approch_1_span_n_class(self):
    '''

    :return:
    '''
    result = self.bsoup.find('span', attrs={'class': SUBSCRIBERS_NUMBER_HTMLCLASSNAME})
    if result is None:
      return
    phrase = result.text
    number = extract_number_from_known_pieces(phrase)
    if number is None:
      return
    self.subscribersnumber = number

  def try_approch_2_id_subscriber_count(self):
    '''

    :return:
    '''
    result = self.bsoup.find('yt-formatted-string', attrs={'id': 'subscriber-count'})
    if result is None:
      return
    phrase = result.text
    number = extract_number_from_known_pieces(phrase)
    if number is None:
      return
    self.subscribersnumber = number

class HTMLScraper:

  def __init__(self, ytvideopageobj):

    self.ytvideopageobj = ytvideopageobj
    self.scrape_subscribers_number()

  def scrape_subscribers_number(self):
    htmlfilename = self.ytvideopageobj.ytvideospagefilename
    # print('Parsing =>', htmlfilename)
    sname   = self.ytvideopageobj.sname
    content = self.ytvideopageobj.get_html_text()
    extlessname = os.path.splitext(htmlfilename)[0]
    bsoup = bs4.BeautifulSoup(content, 'html.parser')
    goparser = GoParser(bsoup)
    if goparser.subscribersnumber is None:
      print('Subscribers number not found for', extlessname)
      #self.ids_with_subsnumber_not_found.append(sname)
      return
    self.ytvideopageobj.nOfSubscribers = goparser.subscribersnumber
    id_n_qty_tuple = (self.ytvideopageobj.ytchid, self.ytvideopageobj.nOfSubscribers)
    self.ytvideopageobj.id_n_qty_tuplelist.append(id_n_qty_tuple)


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

def adhoc_test():
  # refdate = datetime.date(2020,5,26)
  # scraper = HTMLScraper(refdate)

  ytchid = 'ubrunojonssen'
  nname = 'Bruno Jonssen'
  ytvideopagesobj = YtVideosPage(ytchid, nname) # refdate

  scraper = HTMLScraper(ytvideopagesobj)
  print(scraper)

def process():
  adhoc_test()

if __name__ == '__main__':
  process()
