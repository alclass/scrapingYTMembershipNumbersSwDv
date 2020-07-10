#!/usr/bin/python3
import string

def consume_left_side_float_number(word):
  '''

  :param word:
  :return:
  '''
  if word is None:
    return None
  if type(word) == int or type(word) == float:
    return float(word)
  numberstr = ''
  for c in word:
    if c in string.digits:
      numberstr += c
    elif c in [',','.']:
      numberstr += '.'
    else:
      break
  if numberstr == '':
    return None
  floatnumber = float(numberstr)
  return floatnumber

def consume_left_side_int_number_w_optional_having_comma_or_point(word):
  if word is None:
    return None
  if type(word) == int: # or type(word) == float:
    return word
  numberstr = ''
  for c in word:
    if c in string.digits:
      numberstr += c
    elif c in [',','.']:
      continue
    else:
      break
  if numberstr == '':
    return None
  intnumber = int(numberstr)
  return intnumber

def extract_number_from_phrase_unit_mil_k_mi(arialabel):
  '''
  This function:
    1) calls consume_left_side_float_number(t) above
      to firstly get a floatnumber (or None if none is there);
    2) verifies a multiplier sufix (mil (or k), mi)
      obs: in the future, language issues, such as k, mil etc, should be taken
    3) returns the whole (integer) number
      or -1 if none was found
  :param arialabel:
  :return:
  '''
  floatnumber = consume_left_side_float_number(arialabel)
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
  return int(floatnumber) # number of subscribers is an int

def extract_phrase_from__subscriberCountText_in_js(content):
  '''
  In Javascript, not in DOM:
    "subscriberCountText":{"runs":[{"text":"365 mil inscritos"}]},
  :param content:
  :return:
  '''
  subscriberCountText = '"subscriberCountText"'
  pos = content.find(subscriberCountText)
  if pos < 0:
    return -1
  # content as parameter is not changed, though strings do not suffer side-effect
  trunk = content[pos : ]
  curly_bracket_text = '{"text":'
  pos = trunk.find(curly_bracket_text)
  if pos < 0:
    return -1
  trunk = trunk[pos : ]
  quote_closing_curly_bracket = '"}'
  pos = trunk.find(quote_closing_curly_bracket)
  if pos < 0:
    return -1
  trunk = trunk[ : pos+2]
  result = trunk
  try:
    pdict = eval(trunk)
    result = pdict['text']
  except ValueError:
    pass
  return result

def find_subscriberCountText_in_js(content):
  phrase = extract_phrase_from__subscriberCountText_in_js(content)
  return extract_number_from_phrase_unit_mil_k_mi(phrase)

def adhoc_test():
  t = '"subscriberCountText": {"runs": [{"text": "365 mil inscritos"}]},'
  result = find_subscriberCountText_in_js(t)
  print (result)

def process():
  adhoc_test()

if __name__ == '__main__':
  process()
