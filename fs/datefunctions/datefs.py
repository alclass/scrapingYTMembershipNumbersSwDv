#!/usr/bin/python3
import datetime
import config
import random
import fs.textfunctions.scraper_helpers as scraphlp

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
