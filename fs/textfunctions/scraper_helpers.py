#!/usr/bin/env python3
"""
  docstring
"""
import datetime
import json
import logging
import os
import string
import config
import fs.numberfunctions.numbermod as nmod

_, logfilename = os.path.split(__file__)
logfilename = str(datetime.date.today()) + '_' + logfilename[:-3] + '.log'
logfilepath = os.path.join(config.get_logfolder_abspath(), logfilename)
logging.basicConfig(filename=logfilepath, filemode='w', format='%(name)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)



def extract_number_from_phrase_unit_mil_k_mi(arialabel):
  """
  This function:
    1) calls consume_left_side_float_number(t) above
      to firstly get a floatnumber (or None if none is there);
    2) verifies a multiplier sufix (mil (or k), mi)
      obs: in the future, language issues, such as k, mil etc, should be taken
    3) returns the whole (integer) number
      or -1 if none was found
  :param arialabel:
  :return:
  """
  floatnumber = nmod.consume_left_side_float_number(arialabel)
  if floatnumber is None:
    return -1
  if type(arialabel) != str:
    return arialabel
  if arialabel.find('mil ') > -1:
    floatnumber = floatnumber * 1000
  elif arialabel.find('k ') > -1:
    floatnumber = floatnumber * 1000
  elif arialabel.find('mi ') > -1:
    floatnumber = floatnumber * 1000 * 1000
  return int(floatnumber)  # number of subscribers is an int


def extract_phrase_from_subscriber_count_text_in_js(content):
  """
  In Javascript, not in DOM:
    "subscriberCountText":{"runs":[{"text":"365 mil inscritos"}]},
  :param content:
  :return:
  """
  subscriber_count_text = '"subscriberCountText"'
  pos = content.find(subscriber_count_text)
  if pos < 0:
    return -1
  # content as parameter is not changed, though strings do not suffer side-effect
  trunk = content[pos:]
  curly_bracket_text = '{"text":'
  pos = trunk.find(curly_bracket_text)
  if pos < 0:
    return -1
  trunk = trunk[pos:]
  quote_closing_curly_bracket = '"}'
  pos = trunk.find(quote_closing_curly_bracket)
  if pos < 0:
    return -1
  trunk = trunk[: pos+2]
  result = trunk
  try:
    pdict = eval(trunk)
    result = pdict['text']
  except ValueError:
    pass
  return result


subscriberBegStr = '"subscriberCountText":{"runs":[{"text":"'
subscriberPrefixBegStr = '"subscriberCountText":'
subscriberEndStr = '"}]},'
# "subscriberCountText":{"runs":[{"text":"69,2 mil inscritos"}]}


def extract_subscriber_2nd_try(text):
  """
  "subscriberCountText":{"simpleText":"556 mil inscritos"},
  :param text:
  :return:
  """
  begpos = text.find('"subscriberCountText":{"simpleText":"')
  if begpos > -1:
    chunk = text[begpos+len('"subscriberCountText":'): ]
    endpos = chunk.find('"}')
    if endpos > -1:
      chunk = chunk[ : endpos+2]
      print(chunk)
      pdict = json.loads(chunk)
      value = pdict['simpleText']
      n_of_subscribers = extract_number_from_phrase_unit_mil_k_mi(value)
      return n_of_subscribers
  return None


def extract_subscriber_number(text):
  """
  :param text:
  :return:
  """
  subscriber_number = None
  begpos = text.find(subscriberBegStr)
  if begpos > -1:
    trunk = text[begpos + len(subscriberPrefixBegStr):]
    endpos = trunk.find(subscriberEndStr)
    if endpos > -1:
      trunk = trunk[: endpos + len(subscriberEndStr) - 1]
      try:
        pdict = json.loads(trunk)
        print(pdict)
        subscriber_text = pdict['runs'][0]['text']
        subscriber_number = extract_number_from_phrase_unit_mil_k_mi(subscriber_text)
      except json.decoder.JSONDecodeError:
        pass
  if subscriber_number is None:
    # 2nd try
    subscriber_number = extract_subscriber_2nd_try(text)
  return subscriber_number


def videoitems_drill_down(json_as_dict):
  ytvideoid = json_as_dict['gridVideoRenderer']['videoId']
  title = None
  try:
    title = json_as_dict['gridVideoRenderer']['title']['runs'][0]['text']
  except KeyError:
    pass
  if title is None:
    try:
      title = json_as_dict['gridVideoRenderer']['title']['simpleText']
    except KeyError:
      title = 'No Title'
  try:
    calendar_date_str = json_as_dict['gridVideoRenderer']['publishedTimeText']['simpleText']
  except KeyError:
    calendar_date_str = '1 minut'
  try:
    n_views = json_as_dict['gridVideoRenderer']['viewCountText']['simpleText']
  except KeyError:
    n_views = '0 v'
  try:
    innerdict = json_as_dict['gridVideoRenderer']['thumbnailOverlays'][0]
    duration_str = innerdict['thumbnailOverlayTimeStatusRenderer']['text']['simpleText']
  except KeyError:
    duration_str = '0:0'
  log_msg = 'Scraped from json: <ytvideoid=%s t=[%s] cal=%s v=%s ds=%s>' \
            % (ytvideoid, title, calendar_date_str, n_views, duration_str)
  print(log_msg)
  logger.info(log_msg)

  return ytvideoid, title, calendar_date_str, n_views, duration_str


def find_subscriber_count_text_in_js(content):
  phrase = extract_phrase_from_subscriber_count_text_in_js(content)
  return extract_number_from_phrase_unit_mil_k_mi(phrase)


def adhoc_test1():
  t = '"subscriberCountText": {"runs": [{"text": "365 mil inscritos"}]},'
  result = find_subscriber_count_text_in_js(t)
  print(result)


def process():
  adhoc_test1()


if __name__ == '__main__':
  process()
