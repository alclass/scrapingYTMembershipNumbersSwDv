#!/usr/bin/python3
import bs4
import datetime
import os
import fs.textfunctions.regexp_helpers as regexp
from models.gen_models.YtVideosPageMod import YtVideosPage
import fs.numberfunctions.numbermod as nmod

SUBSCRIBERS_NUMBER_HTMLCLASSNAME = 'yt-subscription-button-subscriber-count-branded-horizontal'
'''
  <span class="yt-subscription-button-subscriber-count-branded-horizontal subscribed yt-uix-tooltip" 
    title="433 mil" tabindex="0" aria-label="433 mil inscritos">433 mil</span>
Alternatively:  
  <yt-formatted-string id="subscriber-count" 
  class="style-scope ytd-c4-tabbed-header-renderer">365&nbsp;mil inscritos</yt-formatted-string>  
'''
# SubscribersStatNT = collections.namedtuple('SubscribersStatNT', ['n_subscribers', 'strline'])


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
    number = nmod.consume_left_side_float_number(firstword)
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


class SubscriberScraper:

  def __init__(self, content):
    self.parse_has_run = False
    self.content = content
    self._subscribersnumber = None
    self.goparse()
    self.parse_has_run = True

  @property
  def subscribersnumber(self):
    if self.parse_has_run:
      return self._subscribersnumber
    if self.content is None:
      return -1
    if self._subscribersnumber is None:
      self.goparse()
    return self._subscribersnumber

  def goparse(self):
    """

    :return:
    """
    self.try_approch_1_span_n_class()
    if self._subscribersnumber is None:
      self.try_approch_2_id_subscriber_count()

  def try_approch_1_span_n_class(self):
    """

    :return:
    """
    bsoup = bs4.BeautifulSoup(self.content, 'html.parser')
    result = bsoup.find('span', attrs={'class': SUBSCRIBERS_NUMBER_HTMLCLASSNAME})
    if result is None:
      self._subscribersnumber = None
      return
    # print ('=> RESULT', result.text)
    phrase = result.text
    number = regexp.find_nsubscribers_via_two_words(phrase)  # eg x mil
    # number = extract_number_from_known_pieces(phrase)
    if number is None or number == -1:
      self._subscribersnumber = None
      return
    self._subscribersnumber = number

  def try_approch_2_id_subscriber_count(self):
    """

    :return:
    """
    number = regexp.find_nsubscribers_via_either_re_or_find(self.content)
    if number is None:
      self._subscribersnumber = -1
      return
    # it can be -1 from here (which means number was not found)
    self._subscribersnumber = number


class HTMLScraper:

  def __init__(self, ytvideopageobj):

    self.ytvideopageobj = ytvideopageobj
    self.scrape_subscribers_number()

  def scrape_subscribers_number(self):
    htmlfilename = self.ytvideopageobj.filename
    # sname = self.ytvideopageobj.sname
    try:
      content = self.ytvideopageobj.get_html_text()
    except OSError:
      return None
    extlessname = os.path.splitext(htmlfilename)[0]
    subs_scraper = SubscriberScraper(content)
    if subs_scraper.subscribersnumber is None:
      print('Subscribers number not found for', extlessname)
      return
    self.ytvideopageobj.n_subscribers = subs_scraper.subscribersnumber

  @staticmethod
  def scrape_individual_video_views(htmlfilename, content):
    """
    Not used by now
    ===============
    :param htmlfilename:
    :param content:
    :return:
    """
    extlessname = os.path.splitext(htmlfilename)[0]
    bsoup = bs4.BeautifulSoup(content, 'html.parser')
    result = bsoup.find('span', attrs={'class': SUBSCRIBERS_NUMBER_HTMLCLASSNAME})
    if result is None:
      print('Subscribers number not found for', extlessname)
      return

  def __str__(self):
    n_of_subscribers = self.ytvideopageobj.n_subscribers
    outstr = '''
    ytvideopageobj = %(ytvideopageobj)s
    n_subscribers = %(nOfSubscribers)d 
    ''' % {'ytvideopageobj': self.ytvideopageobj, 'nOfSubscribers': n_of_subscribers}
    return outstr


def adhoc_test():
  # 1
  seq = 1
  print('Test', seq)
  print('-'*50)
  ytchid = 'ubrunojonssen'
  nname = 'Bruno Jonssen'
  refdate = datetime.date(2020, 5, 27)
  ytvideopagesobj = YtVideosPage(ytchid, nname, refdate)
  htmlscraper = HTMLScraper(ytvideopagesobj)
  print(htmlscraper)
# 2
  seq += 1
  print('Test', seq)
  print('-' * 50)
  ytchid = 'ubrunojonssen'
  nname = 'Bruno Jonssen'
  refdate = datetime.date(2020, 5, 28)
  ytvideopagesobj = YtVideosPage(ytchid, nname, refdate)
  htmlscraper = HTMLScraper(ytvideopagesobj)
  print(htmlscraper)
# 3
  seq += 1
  print('Test', seq)
  print('-' * 50)
  ytchid = 'upgjr23'
  nname = 'Paulo Ghiraldelli'
  refdate = datetime.date(2020, 5, 28)
  ytvideopagesobj = YtVideosPage(ytchid, nname, refdate)
  htmlscraper = HTMLScraper(ytvideopagesobj)
  print(htmlscraper)


def process():
  adhoc_test()


if __name__ == '__main__':
  process()
