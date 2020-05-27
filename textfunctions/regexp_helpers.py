#!/usr/bin/python3
import re

# regexp_str = r'\{.+(\d+)[\s](\S+)[\s]inscritos\"\}'
regexp_str = r'\{\"text\"\:\s\"(\d+[\,|\.]*[\d+]*.\S+\s+\w+)\"\}' # inscritos
re_compiled = re.compile(regexp_str)
def find_nsubscribers_via_regexp(context):
  '''
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

  :param context:
  :return:
  '''
  match = re_compiled.search(context)
  if match is None:
    return -1
  result = str(match.group(1)) # + ' ' + str(match.group(2))
  try:
    pp = result.split(' ')
    # number
    lastword = pp[-1]
    if lastword not in ['inscritos', 'subscribers', 'suscriptores', 'abonnés']:
      return -1
    number = pp[0]
    if number.find(',') > -1:
      number = number.replace(',', '.')
    number = float(number)
    multiplier = pp[0]
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

def adhoc_test():
  t = 'blah {"text": "437.6 k subscribers"} blah'
  result = find_nsubscribers_via_regexp(t)
  print('result', result)
  t = 'blah {"text": "437,6 mi inscritos"}'
  result = find_nsubscribers_via_regexp(t)
  print ('result', result)

def process():
  adhoc_test()

if __name__ == '__main__':
  process()