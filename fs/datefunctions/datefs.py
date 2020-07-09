#!/usr/bin/python3
import calendar, datetime
import config
import random
import fs.textfunctions.scraper_helpers as scraphlp

def convert_datetime_to_date(pdatetime):
  if type(pdatetime) == datetime.date:
    return pdatetime
  try: # supposed datetime.datetime type:
    pdate = datetime.date(year=pdatetime.year, month=pdatetime.month, day=pdatetime.day)
    return pdate
  except AttributeError:
    pass
  return None

def add_or_subtract_to_month(pdate, delta):
  '''
  Ref https://stackoverflow.com/questions/3424899/whats-the-simplest-way-to-subtract-a-month-from-a-date-in-python

  d = min(date.day, calendar.monthrange(y, m)[1])
      or
  d = min(date.day, [31,
                     29 if y % 4 == 0 and not y % 400 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1])

  :param date:
  :param delta:
  :return:
  '''
  m, y = (pdate.month + delta) % 12, pdate.year + ((pdate.month) + delta - 1) // 12
  if not m: m = 12
  d = min(pdate.day, calendar.monthrange(y, m)[1])
  return pdate.replace(day=d, month=m, year=y)

def get_refdate(p_refdate=None):
  if p_refdate is None or type(p_refdate) != datetime.date:
    refdate = datetime.date.today()
    return refdate
  return p_refdate

def get_strdate(p_refdate=None):
  refdate = get_refdate(p_refdate)
  strdate = '%d-%s-%s' %(refdate.year, str(refdate.month).zfill(2), str(refdate.day).zfill(2))
  return strdate

def get_refdate_from_strdate_or_None(strdate):
  if strdate is None:
    return None
  strdate = str(strdate)
  try:
    pp = strdate.split('-')
    year  = int(pp[0])
    month = int(pp[1])
    day   = int(pp[2])
    rdate = datetime.date(year, month, day)
    return rdate
  except IndexError:
    pass
  except ValueError:
    pass
  return None

def get_refdate_from_strdate(strdate=None):
  if strdate is None:
    return get_refdate()
  if type(strdate) in [datetime.date, datetime.datetime]:
    return strdate
  strdate = str(strdate)
  if len(strdate) != 10:
    return get_refdate()
  try:
    pp = strdate.split('-')
    year = int(pp[0])
    month = int(pp[1])
    day = scraphlp.consume_left_side_int_number_w_optional_having_comma_or_point(pp[2])
    return datetime.date(year, month, day)
  except IndexError:
    pass
  except ValueError:
    pass
  return get_refdate()

def is_stryyyydashmm_good(yyyymm7char):
  if yyyymm7char is None:
    return False
  try:
    pp = yyyymm7char.split('-')
    year = int(pp[0])
    month = int(pp[1])
    day = 1
    _ = datetime.date(year, month, day)
    return True
  except IndexError:
    pass
  except ValueError: # but for int() and for datetime.infodate()
    pass
  return False

def return_refdate_as_datetimedate_or_today(refdate=None):
  if refdate is None:
    return datetime.date.today()
  if type(refdate) == datetime.date:
    return refdate
  elif type(refdate) == datetime.datetime:
    return datetime.date(refdate.year, refdate.month, refdate.day)
  if type(refdate) != str:
    refdate = str(refdate)
  try:
    pp = refdate.split('-')
    year = int(pp[0])
    month = int(pp[1])
    day = int(pp[2])
    return datetime.date(year, month, day)
  except IndexError:
    pass
  except ValueError:
    pass
  return get_refdate()

def is_year_month_day_good(year, month, day=1):
  try:
    _ = datetime.date(year, month, day)  # if this op is complete, year_month is good
    return True
  except ValueError:
    pass
  return False

def str_is_inversed_year_month(str_year_month):
  if str_year_month is None:
    return False
  try:
    pp = str_year_month.split('-')
    year = int(pp[0]); month = int(pp[1]); day = 1
    _ = datetime.date(year, month, day) # if this op is complete, year_month is good
    return True
  except IndexError:
    pass
  except ValueError:
      pass
  return False

def str_is_inversed_date(strdate):
  if strdate is None:
    return False
  try:
    pp = strdate.split('-')
    year = int(pp[0]); month = int(pp[1]); day = int(pp[1])
    _ = datetime.date(year, month, day) # if this op is complete, infodate is good
    return True
  except IndexError:
    pass
  except ValueError:
      pass
  return False

def calc_past_date_from_refdate_back_n_days(p_refdate, p_backdays=None):
  refdate = return_refdate_as_datetimedate_or_today(p_refdate)
  backdays = 1
  if p_backdays is not None:
    backdays = p_backdays
  return refdate - datetime.timedelta(days=backdays)

def transform_hms_into_duration_in_sec(duration_hms):
  if duration_hms is None:
    return None
  if type(duration_hms) != str:
    error_msg = 'Error: in set_duration_in_sec() => duration_in_sec =' + str(duration_hms)
    raise ValueError(error_msg)
  pp = duration_hms.split(':')
  if len(pp) == 2:
    try:
      minutes = int(pp[0])
      seconds = int(pp[1])
      duration_in_sec = minutes * 60 + seconds
      return duration_in_sec
    except ValueError:
      pass
  elif len(pp) == 3:
    try:
      hours = int(pp[0])
      minutes = int(pp[1])
      seconds = int(pp[2])
      duration_in_sec = hours * 60 * 60 + minutes * 60 + seconds
      return duration_in_sec
    except ValueError:
      pass
  error_msg = 'Error: in set_duration_in_sec() => duration_in_sec =' + str(duration_hms)
  raise ValueError(error_msg)

def does_it_startswith_a_number(word):
  try:
    _ = int(word.split(' ')[0])
    return True
  except ValueError:
    pass
  return False

def ajust_calendardatestr_to_start_with_a_number(calendardatestr):
  '''
    This function strips non-numbers out of the beginning of the string after a space-split,
      ie, the result must start with a number if there is a number inside the string, if not,
      the default will be returned.

    E.g.
      1) input_str = 'há 2 dias atrás' :: output_str will be '2 dias atrás'
      2) input_str = '3 days ago' :: output_str will be the same as input_str, ie '3 days ago'
      3) input_str = 'blah bla 10 hours ahead' :: output_str will be '10 hours ahead'

    Take a look at the corresponding unit test module for more examples.

  :param calendardatestr:
  :return:
  '''
  default_calendardatestr = '1 hora'

  current_split_list = calendardatestr.split(' ')
  while len(current_split_list) > 0:
    try:
      _ = int(current_split_list[0])
      break
    except ValueError:
      del current_split_list[0]
  recomposed_calendarstr = ' '.join(current_split_list)
  if recomposed_calendarstr == '': # if current_split_list is empty, the join str will be empty if with a space ' ' calling join
    recomposed_calendarstr = default_calendardatestr
  return recomposed_calendarstr

def make_daterange_with_dateini_n_datefim(dateini=None, datefim=None):
  today = datetime.date.today()
  if dateini is None:
    dateini = today
  if datefim is None:
    datefim = today
  dateini = return_refdate_as_datetimedate_or_today(dateini)
  datefim = return_refdate_as_datetimedate_or_today(datefim)
  if dateini > today and datefim > today:
    return []
  if dateini > today:
    dateini = today
  if datefim > today:
    datefim = today
  delta = datefim - dateini
  absdeltadays = abs(delta.days)
  if absdeltadays == 0:
    daterange = [datefim] # dateini here is equal to datefim
    return daterange
  daterange = [dateini]
  previous_date = dateini
  if dateini < datefim:
    for d in range(absdeltadays):
      previous_date = previous_date + datetime.timedelta(days=1)
      daterange.append(previous_date)
    return daterange
  if datefim < dateini:
    for d in range(absdeltadays):
      previous_date = previous_date - datetime.timedelta(days=1)
      daterange.append(previous_date)
    return daterange
  error_msg = 'Algorithm Error: flow control got to end of function when it should not [dtfs.form_daterange_with_dateini_n_datefim(dateini=%s, datefim=%s)]' %(str(dateini, str(datefim)))
  raise ValueError(error_msg)

def transform_duration_in_sec_into_hms(duration_in_sec):
  if duration_in_sec is None:
    return 'w/inf'
  if duration_in_sec < 60:
    return '0:%s' %str(duration_in_sec).zfill(2)
  elif duration_in_sec < 60 * 60:
    minutes = duration_in_sec // 60
    seconds = duration_in_sec % 60
    return '%s:%s' %(str(minutes).zfill(2), str(seconds).zfill(2))
  else:
    hours = duration_in_sec // (60 * 60)
    remaining = duration_in_sec - hours * (60 * 60)
    minutes = remaining // 60
    seconds = remaining % 60
    return '%s:%s:%s' % (str(hours).zfill(2), str(minutes).zfill(2), str(seconds).zfill(2))
  # return 'w/inf' the if-elif-else above make this point unreachable (the IDE confims)

def get_random_n_within_interval(n_min, n_max_plus_1):
  return random.randrange(n_min, n_max_plus_1)

def get_random_config_download_wait_nsecs():
  n_min = config.DOWNLOAD_WAIT_SECONDS_MIN
  n_max = config.DOWNLOAD_WAIT_SECONDS_MAX
  return get_random_n_within_interval(n_min, n_max+1)

def test():
  date_str = get_strdate()
  print('default date_str', date_str)
  d = datetime.date(2020, 5, 19)
  date_str = get_strdate(d)
  print('given datetime.infodate to date_str', date_str, 'type', type(date_str))
  recup_date = get_refdate_from_strdate(date_str)
  print('recup_date', recup_date, 'type', type(recup_date))

def process():
  test()
  n_wait = get_random_config_download_wait_nsecs()
  print('n_wait',n_wait)
  n_wait = get_random_config_download_wait_nsecs()
  print('n_wait',n_wait)

if __name__ == '__main__':
  process()
