#!/usr/bin/python3
import datetime, json, calendar
from models.gen_models.YtVideosPageMod import YtVideosPage
import fs.textfunctions.scraper_helpers as scraphlp

def drill_down_dict(pdict, tablevel=0):
  if tablevel == 0:
    strtabs = ''
  else:
    strtabs = '\t' * tablevel
  for level_a in pdict:
    if type(level_a) == dict:
      return drill_down_dict(level_a, tablevel+1)
    else:
      print (strtabs, level_a)

subscriberBegStr = '"subscriberCountText":{"runs":[{"text":"'
subscriberPrefixBegStr = '"subscriberCountText":'
subscriberEndStr = '"}]},'
# "subscriberCountText":{"runs":[{"text":"69,2 mil inscritos"}]}
def extract_subscriber_number(text, ytvideopage):
  begpos = text.find(subscriberBegStr)
  if begpos > -1:
    trunk = text[begpos + len(subscriberPrefixBegStr): ]
    endpos = trunk.find(subscriberEndStr)
    if endpos > -1:
      trunk = trunk[ : endpos + len(subscriberEndStr) -1 ]
      pdict = json.loads(trunk)
      print (pdict)
      subscriberText = pdict['runs'][0]['text']
      subscriber_number = scraphlp.extract_number_from_phrase_unit_mil_k_mi(subscriberText)
      print (subscriber_number, ytvideopage.sname)

def process_via_file(ytchannelid, refdate=None):
  ytvideopage = YtVideosPage(ytchannelid, None, refdate)
  if ytvideopage.datedpage_filepath is None:
    print ('Filepath is None for', ytchannelid, ':: returning...' )
    return
  timestamp = ytvideopage.filesdatetime.st_atime
  print (ytvideopage.filesdatetime.st_atime)
  videopagefilesdatetime = datetime.datetime.fromtimestamp(timestamp)
  print (videopagefilesdatetime)

  text = ytvideopage.get_html_text()
  extract_subscriber_number(text, ytvideopage)

from models.sa_models.ytchannelsubscribers_samodels import get_all_ytchannelids
def run_thru_channels():
  today = datetime.date.today()
  ini_fim_daterange = [today]
  for ytchannelid in get_all_ytchannelids(): # ytchannelids = finder.get_ytchannelids_on_datefolder(today)
    for refdate in ini_fim_daterange:  # dtfs.get_range_date(yesterday, today):
      print ('Rolling', ytchannelid, 'for date', refdate )
      print ('-'*50)
      process_via_file(ytchannelid, refdate)

def process():
  run_thru_channels()

if __name__ == '__main__':
  process()