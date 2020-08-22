#!/usr/bin/python3
import calendar
import datetime
import config
import random
import fs.textfunctions.scraper_helpers as scraphlp


def convert_datetime_to_date(pdatetime):
  """
    supposed datetime.datetime type:
  :param pdatetime:
  :return:
  """
  if type(pdatetime) == datetime.date:
    return pdatetime
  try:
    pdate = datetime.date(year=pdatetime.year, month=pdatetime.month, day=pdatetime.day)
    return pdate
  except AttributeError:
    pass
  return None


def extract_time_from_datetime(pdatetime):
  if pdatetime is None:
    return None
  try:
    ptime = datetime.time(pdatetime.hour, pdatetime.minute, pdatetime.second, pdatetime.microsecond)
  except AttributeError:
    return None
  return ptime


def get_roundint_hour_from_time(ptime, default_hour=12):
  """
    Notice: this function doesn't round hour 23 for the time being for it should "carry one"
      which it does do at this moment

  :param ptime:
  :param default_hour:
  :return:
  """
  if ptime is None:
    return default_hour
  try:
    hour = ptime.hour
    if hour > 22:
      return hour
    if hour % 2 == 0:
      if ptime.minute < 31:
        return hour
      else:
        return hour + 1
    if ptime.minute < 30:
      return hour
    else:
      return hour + 1
  except AttributeError:
    pass
  return default_hour


def zero_microsec_in_datetime(pdatetime):
  pdt = pdatetime
  if pdt is None:
    return None
  return datetime.datetime(pdt.year, pdt.month, pdt.day, pdt.hour, pdt.minute, pdt.second)


def split_date_n_time_from_datetime(pdatetime):
  pdate = convert_datetime_to_date(pdatetime)
  if pdate is None:
    return None, None
  ptime = extract_time_from_datetime(pdatetime)
  if ptime is None:
    return pdate, None
  return pdate, ptime


def add_or_subtract_to_month(pdate, delta):
  """
  Ref https://stackoverflow.com/questions/3424899/whats-the-simplest-way-to-subtract-a-month-from-a-date-in-python

  d = min(date.day, calendar.monthrange(y, m)[1])
      or
  d = min(date.day, [31,
                     29 if y % 4 == 0 and not y % 400 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1])

  :param pdate:
  :param delta:
  :return:
  """
  m, y = (pdate.month + delta) % 12, pdate.year + (pdate.month + delta - 1) // 12
  if not m:
    m = 12
  d = min(pdate.day, calendar.monthrange(y, m)[1])
  return pdate.replace(day=d, month=m, year=y)


def get_refdate_or_none(p_refdate=None):
  if p_refdate is None:
    return None
  if type(p_refdate) == datetime.date:
    return p_refdate
  if type(p_refdate) == datetime.datetime:
    return convert_datetime_to_date(p_refdate)
  return get_refdate_from_strdate_or_none(str(p_refdate))


def get_refdate_or_today(p_refdate=None):
  indate = get_refdate_or_none(p_refdate)
  if indate is None:
    return datetime.date.today()
  return indate


def get_strdate(p_refdate=None):
  refdate = get_refdate_or_today(p_refdate)
  strdate = '%d-%s-%s' % (refdate.year, str(refdate.month).zfill(2), str(refdate.day).zfill(2))
  return strdate


def get_refdate_from_strdate_or_today(pdate=None):
  indate = get_refdate_from_strdate_or_none(pdate)
  if indate is None:
    return datetime.date.today()
  return indate


def get_refdate_from_strdate_or_none(strdate):
  if strdate is None:
    return None
  strdate = str(strdate)
  try:
    pp = strdate.split('-')
    year = int(pp[0])
    month = int(pp[1])
    day = int(pp[2])
    rdate = datetime.date(year, month, day)
    return rdate
  except IndexError:
    pass
  except ValueError:
    pass
  return None


def get_refdate_from_strdate(strdate=None):
  if strdate is None:
    return get_refdate_or_today()
  if type(strdate) in [datetime.date, datetime.datetime]:
    return strdate
  strdate = str(strdate)
  if len(strdate) != 10:
    return get_refdate_or_today()
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
  return get_refdate_or_today()


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
  except IndexError:  # for non-existing indices
    pass
  except ValueError:  # for int() and for datetime.infodate()
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
  return get_refdate_or_today()


def is_year_month_day_good(year, month, day):
  """
    This function is also used by is_year_month_good(year, month)
  :param year:
  :param month:
  :param day:
  :return:
  """
  try:
    _ = datetime.date(int(year), int(month), int(day))
    return True
  except ValueError:
    pass
  return False


def is_year_month_good(year, month):
  return is_year_month_day_good(year, month, day=1)


def is_year_good(year):
  return is_year_month_day_good(year, month=1, day=1)


def is_stryyyy_good(stryyyy):
  try:
    year = int(stryyyy)
    return is_year_good(year)
  except ValueError:
    pass
  return False


def is_strdate_a_7char_yyyymm(str_year_month):
  """
    Valid one: 2020-01
    Invalid ones: 20201, 202001
  :param str_year_month:
  :return:
  """
  if str_year_month is None:
    return False
  if len(str_year_month) != 7:
    return False
  try:
    pp = str_year_month.split('-')
    year = int(pp[0])
    month = int(pp[1])
    day = 1
    _ = datetime.date(year, month, day)  # if this op is complete, year_month is good
    return True
  except IndexError:
    pass
  except ValueError:
      pass
  return False


def is_strdate_a_nondashed_8char_yyyymmdd(strdate):
  """
    Valid one: 20200101
    Invalid ones: 202011, 2020011, 2020101
  :param strdate:
  :return:
  """
  if strdate is None:
    return False
  if len(strdate) != 8:
    return False
  try:
    year = int(strdate[: 4])
    month = int(strdate[4: 6])
    day = int(strdate[6:])
    _ = datetime.date(year, month, day)  # if this op is complete, infodate is good
    return True
  except ValueError:
      pass
  return False


def is_strdate_a_10char_yyyymmdd(strdate):
  """
    Valid one: 2020-01-01
    Invalid ones: 2020-1-1, 2020-01-1, 2020-1-01,
  :param strdate:
  :return:
  """
  if strdate is None:
    return False
  if len(strdate) != 10:
    return False
  return is_strdate_a_dashed_8to10char_yyyymmdd(strdate)


def is_strdate_a_dashed_8to10char_yyyymmdd(strdate):
  """
    Valid ones: 2020-1-1, 2020-01-1, 2020-1-01, 2020-01-01
    Invalid ones: 202011, 202101, 2020101, 2020011
  :param strdate:
  :return:
  """
  if strdate is None:
    return False
  if len(strdate) < 8 or len(strdate) > 10:
    return False
  try:
    pp = strdate.split('-')
    year = int(pp[0])
    month = int(pp[1])
    day = int(pp[1])
    _ = datetime.date(year, month, day)  # if this op is complete, infodate is good
    return True
  except IndexError:
    pass
  except ValueError:
      pass
  return False


def does_str_form_yyyymm7chardate(word):
  if word is None:
    return False
  if len(word) != 7:
    return False
  strdate = word + '-1'
  if get_refdate_from_strdate_or_none(strdate):
    return True
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


def transform_datelike_to_datetime(pdatetime):
  """
  For unit test:
    - for input obj(2020, 07, 11) expected output is datetime(2020, 07, 11, 0, 0, 0)
    - for input obj(2020, 07) expected output is None
    - for input obj(2020, 07, 11, 11, 11, 11) expected output is the same as input typed-datetime
    - for input obj(2020, 07, 11, 11) expected output is datetime(2020, 07, 11, 11, 0, 0)
  :param pdatetime:
  :return:
  """
  if pdatetime is None:
    return None
  if type(pdatetime) == datetime.datetime:
    return pdatetime
  ho = 0
  mi = 0
  se = 0
  ms = 0
  odatetime = datetime.datetime.now()
  try:
    odatetime = odatetime.replace(year=pdatetime.year, month=pdatetime.month, day=pdatetime.day)
  except AttributeError:
    return None
  # in case, though it's not a datetime, known from above, it implements the attributes hour, minute & second
  try:
    ho = pdatetime.hour
    mi = pdatetime.minute
    se = pdatetime.second
    ms = pdatetime.microsecond
  except AttributeError:
    # if this is executed, some of them will be 0
    odatetime = odatetime.replace(hour=ho, minute=mi, second=se, microsecond=ms)
  return odatetime


class DateAdderSubtractor:
  MI = 'MI'
  HO = 'HO'
  DA = 'DA'
  WE = 'WE'
  MO = 'MO'
  YE = 'YE'
  ALL_UNITS = [MI, HO, DA, WE, MO, YE]

  def __init__(self, unit, quant, topast=True):
    self.unit = unit
    self.quant = quant
    self.topast = topast
    self.treat_unit_n_quant()

  def treat_unit_n_quant(self):
    if self.unit not in self.ALL_UNITS:
      error_msg = 'Error: given wrong time unit (%s) to DateAdderSubtractor: available units are %s' \
                  % (str(self.unit), self.ALL_UNITS)
      raise ValueError(error_msg)
    try:
      self.quant = int(self.quant)
      if self.topast and self.quant > 0:
        self.quant = -1 * self.quant
      elif not self.topast and self.quant < 0:
        self.quant = -1 * self.quant
    except ValueError:
      error_msg = 'Error: given calendar time quantity (%s) to DateAdderSubtractor' % (str(self.quant))
      raise ValueError(error_msg)

  def add_from_datetime(self, fdatetime):
    if type(fdatetime) not in [datetime.date, datetime.datetime]:
      fdatetime = transform_datelike_to_datetime(fdatetime)
      if fdatetime is None:
        return None
    if self.unit == self.MI:
      return fdatetime + datetime.timedelta(minutes=self.quant)
    elif self.unit == self.HO:
      return fdatetime + datetime.timedelta(hours=self.quant)
    elif self.unit == self.DA:
      return fdatetime + datetime.timedelta(days=self.quant)
    elif self.unit == self.WE:
      return fdatetime + datetime.timedelta(weeks=self.quant)
    elif self.unit == self.MO:
      return add_or_subtract_to_month(fdatetime, self.quant)
    elif self.unit == self.YE:
      n_months_for_quant_years = 12 * self.quant
      return add_or_subtract_to_month(fdatetime, n_months_for_quant_years)


def transform_calendarstr_to_dateadder(calendar_datestr):
  if calendar_datestr is None:
    return None
  # calendar_datestr = str(calendar_datestr)
  calendar_datestr = ajust_calendardatestr_to_start_with_a_number(calendar_datestr)
  if calendar_datestr.find('minut') > -1:
    quant = int(calendar_datestr.strip().split(' ')[0])
    unit = DateAdderSubtractor.MI
    return DateAdderSubtractor(unit, -quant)
  elif calendar_datestr.find('hora') > -1:
    quant = int(calendar_datestr.strip().split(' ')[0])
    unit = DateAdderSubtractor.HO
    return DateAdderSubtractor(unit, -quant)
  elif calendar_datestr.find('dia') > -1:
    quant = int(calendar_datestr.strip().split(' ')[0])
    unit = DateAdderSubtractor.DA
    return DateAdderSubtractor(unit, quant)
  elif calendar_datestr.find('semana') > -1:
    quant = int(calendar_datestr.strip().split(' ')[0])
    unit = DateAdderSubtractor.WE
    return DateAdderSubtractor(unit, quant)
  elif calendar_datestr.find('mês') > -1 or calendar_datestr.find('mes') > -1:  # mes for meses
    quant = int(calendar_datestr.strip().split(' ')[0])
    unit = DateAdderSubtractor.MO
    return DateAdderSubtractor(unit, quant)
  elif calendar_datestr.find('ano') > -1:
    quant = int(calendar_datestr.strip().split(' ')[0])
    unit = DateAdderSubtractor.WE
    return DateAdderSubtractor(unit, quant)


def calculate_origdtime_from_targetdtime_n_calendarstr(target_dtime, calendarstr):
  """

  if publishdata != date_result:
    line = 'publishdata (%s) != datetime_result (%s)' %(str(publishdata), str(datetime_result))
    print (line)

  :param target_dtime:
  :param calendarstr:
  :return:
  """
  dtadder = transform_calendarstr_to_dateadder(calendarstr)
  if dtadder is None:
    return None
  return dtadder.add_from_datetime(target_dtime)


def ajust_calendardatestr_to_start_with_a_number(calendardatestr):
  """
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
  """
  default_calendardatestr = '1 hora'
  if calendardatestr is None:
    calendardatestr = default_calendardatestr
  current_split_list = calendardatestr.split(' ')
  while len(current_split_list) > 0:
    try:
      _ = int(current_split_list[0])
      break
    except ValueError:
      del current_split_list[0]
  recomposed_calendarstr = ' '.join(current_split_list)
  # if current_split_list is empty, the join str will be empty if with a space ' ' calling join
  if recomposed_calendarstr == '':
    recomposed_calendarstr = default_calendardatestr
  return recomposed_calendarstr


def generate_daterange_with_dateini_n_datefin(dateini=None, datefin=None, allow_future=False):
  dateini = get_refdate_or_today(dateini)
  datefin = get_refdate_or_today(datefin)
  today = datetime.date.today()
  if not allow_future:
    if dateini > today and datefin > today:
      return None
    if dateini > today:
      dateini = today
    if datefin > today:
      datefin = today
  currdate = dateini
  if dateini == datefin:
    yield currdate
  elif dateini < datefin:
    while currdate <= datefin:
      yield currdate
      currdate = currdate + datetime.timedelta(days=1)
  else:
    while currdate >= datefin:
      yield currdate
      currdate = currdate - datetime.timedelta(days=1)
  return None


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
    daterange = [datefim]  # dateini here is equal to datefim
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
  error_msg = 'Algorithm Error: flow control got to end of function when it should not ' \
              '[dtfs.form_daterange_with_dateini_n_datefim(dateini=%s, datefim=%s)]' % (str(dateini), str(datefim))
  raise ValueError(error_msg)


def transform_duration_in_sec_into_hms(duration_in_sec):
  if duration_in_sec is None:
    return 'w/inf'
  if duration_in_sec < 60:
    return '0:%s' % str(duration_in_sec).zfill(2)
  elif duration_in_sec < 60 * 60:
    minutes = duration_in_sec // 60
    seconds = duration_in_sec % 60
    return '%s:%s' % (str(minutes).zfill(2), str(seconds).zfill(2))
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


def adhoc_test2():
  dtadder = DateAdderSubtractor(DateAdderSubtractor.DA, 2)
  today = datetime.date.today()
  dt_res = dtadder.add_from_datetime(today)
  print(dt_res)
  dtadder = DateAdderSubtractor(DateAdderSubtractor.DA, -3)
  today = datetime.date.today()
  dt_res = dtadder.add_from_datetime(today)
  print(dt_res)
  dtadder = DateAdderSubtractor(DateAdderSubtractor.MO, 2)
  today = datetime.date.today()
  dt_res = dtadder.add_from_datetime(today)
  print(dt_res)
  dtadder = DateAdderSubtractor(DateAdderSubtractor.YE, 2)
  today = datetime.date.today()
  dt_res = dtadder.add_from_datetime(today)
  print(dt_res)
  dtadder = DateAdderSubtractor(DateAdderSubtractor.YE, -3)
  today = datetime.date.today()
  dt_res = dtadder.add_from_datetime(today)
  print(dt_res)


def adhoc_test3():
  n_wait = get_random_config_download_wait_nsecs()
  print('n_wait', n_wait)
  n_wait = get_random_config_download_wait_nsecs()
  print('n_wait', n_wait)
  ptime = datetime.time(13, 29, 0)
  dayhour = get_roundint_hour_from_time(ptime)
  print(ptime, 'round hour to', dayhour)


def adhoc_test4():
  for pdate in generate_daterange_with_dateini_n_datefin():
    print(pdate)
  print('-'*30)
  inidate = '2020-8-6'
  findate = '2020-8-8'
  for pdate in generate_daterange_with_dateini_n_datefin(inidate, findate, allow_future=True):
    print(pdate)
  print('-'*30)
  inidate = '2020-8-15'
  findate = '2020-8-4'
  for pdate in generate_daterange_with_dateini_n_datefin(inidate, findate):
    print(pdate)


def process():
  adhoc_test4()

if __name__ == '__main__':
  process()
