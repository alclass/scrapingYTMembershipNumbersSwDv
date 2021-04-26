#!/usr/bin/env python3
"""
  ...
  https://api.adviceslip.com/advice/24
"""
# from prettytable import PrettyTable
import datetime
import json
import random
import requests


BASE_URL = 'https://api.adviceslip.com/advice'
LAST_ADVICE_NUMBER = 217  # On April 25, 2021: 217 advices were observed


def try_balance_brackets(s):
  """
  For the time being, it just supposes the last '}' is missing.
  (which is known beforehand as a "little bug" in the API response)

  :param s:
  :return:
  """
  s = s + '}'
  pdict = json.loads(s)
  return pdict


def convert_json_to_dict(s):
  '''

  Obs: this function has the purpose of correct a missing '}' in the API payload.

  The problem is the following:
  > bytes to str [{"slip": { "id": 217, "advice": "Identify sources of happiness."}]
  > Caught  Expecting ',' delimiter: line 1 column 66 (char 65)
  > pdict {'slip': {'id': 217, 'advice': 'Identify sources of happiness.'}}
  --------------------------------------------------------
  Notice above the last '}' (the closing angle bracket) is missing
  --------------------------------------------------------

  ie, there is a missing '}' in the json payload returned by the API server at
    => https://api.adviceslip.com/advice/24

  The other url, the one for a random advice, brings the final '}' correctly.
    => https://api.adviceslip.com/advice

  :param s:
  :return:
  '''
  try:
    pdict = json.loads(s)
    return pdict
  except json.decoder.JSONDecodeError as e:
    # print('Caught json.decoder.JSONDecodeError =>', e)
    return try_balance_brackets(s)


def get_advice_url(advice_random_n=None):
  """
  The API for slip advices is used in two ways:
    => a random advice with its BASE URL (see constant above)
    => a specified advice with a URL having an id
  :return:
  """
  # print('Fetching advice number', advice_random_n)
  url = BASE_URL
  if advice_random_n is not None:
    url = BASE_URL + '/' + str(advice_random_n)
  # print(url)
  return url


class SlipAdvice:

  def __init__(self):
    self.advice_text = None
    self.advice_id = None
    self.advice_random_n = random.randint(1, LAST_ADVICE_NUMBER)
    self.process()

  def process(self):
    if self.fetch():
      slip_to_print = self.gen_outstr()
      print(slip_to_print)

  def fetch(self):
    url = get_advice_url(self.advice_random_n)
    req = requests.get(url)
    if req.status_code == 200:
      bytes = req.content
      s = bytes.decode('utf8')
      # print('bytes to str [' + s + ']')
      pdict = convert_json_to_dict(s)
      # print('pdict', pdict)
      self.advice_text = pdict['slip']['advice']
      self.advice_id = pdict['slip']['id']
      if self.advice_id != self.advice_random_n:
        print('self.advice_id,  self.advice_random_n', self.advice_id, self.advice_random_n)
      return True
    else:
      print('Failing to get advice number', self.advice_random_n)
      print(req.content)  # there should be a message (error) object (with type & text)
    return False

  def gen_outstr(self):
    datetime_str = datetime.datetime.now()
    outstr = '''
           ADVICESLIP.COM
      =========================
  
      {advice_text}
  
      =========================
  
       on {datetime_str}  id={advice_id}
    '''.format(advice_text=self.advice_text, datetime_str=datetime_str, advice_id=self.advice_id)
    return outstr


def process():
  SlipAdvice()


if __name__ == '__main__':
  process()
