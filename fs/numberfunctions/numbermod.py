#!/usr/bin/env python3
"""
  docstring
"""
import string


def consume_left_side_float_number(word):
  """

  :param word:
  :return:
  """
  if word is None:
    return None
  if type(word) == int or type(word) == float:
    return float(word)
  numberstr = ''
  for c in word:
    if c in string.digits:
      numberstr += c
    elif c in [',', '.']:
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
  if type(word) == int:
    return word
  numberstr = ''
  for c in word:
    if c in string.digits:
      numberstr += c
    elif c in [',', '.']:
      continue
    else:
      break
  if numberstr == '':
    return None
  intnumber = int(numberstr)
  return intnumber


def adhoc_test():
  word = '45234,67 fsfgsdf'
  consume_left_side_float_number(word)
  print('word', word)
  word = consume_left_side_int_number_w_optional_having_comma_or_point(word)
  consume_left_side_int_number_w_optional_having_comma_or_point(word)
  print('word', word)


def process():
  adhoc_test()


if __name__ == '__main__':
  process()
