#!/usr/bin/env python3
"""
  docstring
"""
import os
import re
import fs.textfunctions.scraper_helpers as scraphlp


regexp_str = r'(\d+[\,|\.]*[\d+]*.\S*)\"\}'  # inscritos
re_compiled = re.compile(regexp_str)


def try_find_nsubscribers_via_regexp(content):
  """
  Expected:
    if content has 'blah {"text": "437.6 k subscribers"} blah':
      result = 437.6 k subscribers
    elif content has 'blah {"text": "437,6 mil inscritos"} blah':
      result = 437,6 mil inscritos
  For the time being, the second case above will be treated.

  Notice also that most of pages will not call this function,
    they will find the searched info via the aria-label tag.
  Consider this helper function as a "fallback function"
    when the aria-label tag is somehow missing in the page.

  :param content:
  :return:
  """
  match = re_compiled.search(content)
  if match is None:
    return -1
  result = str(match.group(1))  # + ' ' + str(match.group(2))
  try:
    pp = result.split(' ')
    # number
    '''
    lastword = pp[-1]
    if lastword not in ['inscritos', 'subscribers', 'suscriptores', 'abonnés']:
      return -1
    '''
    number = pp[0]
    if number.find(',') > -1:
      number = number.replace(',', '.')
    number = float(number)
    if len(pp) > 2:
      if pp[1] == 'mi':
        return int(number*1000*1000)
      elif pp[1] in ['mil', 'k']:
        return int(number * 1000)
      return int(number)
  except ValueError:
    pass
  except IndexError:
    pass
    # if content had the data, it should have already returned by here
  return -1

# class="style-scope ytd-c4-tabbed-header-renderer">365&nbsp;mil inscritos
# <yt-formatted-string id="subscriber-count" class="style-scope ytd-c4-tabbed-header-renderer">
# 365&nbsp;mil inscritos</yt-formatted-string>


def find_nsubscribers_via_either_re_or_find(content):
  result = try_find_nsubscribers_via_regexp(content)
  if result == -1:
    return scraphlp.find_subscriber_count_text_in_js(content)
  return result


def find_nsubscribers_via_two_words(phrase):
  """
  YouTube does not send a character space in the phrase, example:
     "111 mil"
  It sends, instead of a space, a non-breakable space, seen as '\xa0'
  Trying to decode it to string, it does not work, because bsoup
    put it in a string as \xa0.
    (byt = b'\xa0'; sep = byt.decode(); # did not work.)
  The workaround was to use method string's replace() like the following
    phrase = phrase.replace('\xa0', ' ')
  That worked and this scraper also uses a second try method, fallingback,
    which scrapes from a Javascript chunk and there char-space is char-space
  :param phrase:
  :return:
  """
  if phrase is None:
    return None
  phrase = phrase.replace('\xa0', ' ')
  phrase = phrase.replace(',', '.')
  pp = phrase.split(' ')
  try:
    n_of_subscribers = float(pp[0])
  except ValueError as e:
    print('phrase', phrase)
    raise ValueError(e)
  if len(pp) == 1:
    return n_of_subscribers
  sufix = pp[1]
  if sufix in ['k', 'mil']:
    return int(n_of_subscribers * 1000)
  elif sufix in ['mi']:
    return int(n_of_subscribers * 1000 * 1000)
  return int(n_of_subscribers)


regexp_ytchid_str = r'.+(\[[a-zA-Z0-9_\-]+\])$'
re_ytchid_compiled = re.compile(regexp_ytchid_str)


def find_ytchannelid_within_brackets_in_filename(name_without_ext):
  match = re_ytchid_compiled.search(name_without_ext)
  if match is None:
    return None
  result = str(match.group(1))
  result = result.lstrip('[').rstrip(']')
  return result


def find_triple_date_sname_n_ytchid_in_filename(name_without_ext):
  """
    name_without_ext should be mounted as:
     "yyyy-mm-dd <sname (up to 10 chars)> [channelphrase]"
  :param name_without_ext:
  :return:
  """
  if name_without_ext is None:
    return None, None, None
  if name_without_ext.find('.') > -1:
    name_without_ext, _ = os.path.splitext(name_without_ext)
  try:
    strdate = name_without_ext[:10]
    ytchid = find_ytchannelid_within_brackets_in_filename(name_without_ext)
    sname = name_without_ext[11: -(len(ytchid)+2+1)]
    if len(sname) > 10:
      sname = sname[:10]
    if sname.endswith(' '):
      sname = sname.strip(' ')
    return strdate, sname, ytchid
  except IndexError:
    pass
  return None, None, None


def adhoc_test():
  t = 'blah {"text": "437.6 k subscribers"} blah'
  print('Sending =>', t)
  result = find_nsubscribers_via_either_re_or_find(t)
  print('result', result)
  print('-'*40)
  t = 'blah {"text": "437,6 mi inscritos"}'
  print('Sending =>', t)
  result = find_nsubscribers_via_either_re_or_find(t)
  print('result', result)
  t = 'bla [-cUlddjf_aj-dlf-_]'
  print('Sending =>', t)
  result = find_ytchannelid_within_brackets_in_filename(t)
  print('result', result)


def process():
  adhoc_test()


if __name__ == '__main__':
  process()
