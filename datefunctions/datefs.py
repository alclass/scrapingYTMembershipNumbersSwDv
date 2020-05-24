#!/usr/bin/python3
import datetime

def get_refdate(p_refdate=None):
  if p_refdate is None or type(p_refdate) != datetime.date:
    refdate = datetime.date.today()
    return refdate
  return p_refdate

def get_strdate(p_refdate=None):
  refdate = get_refdate(p_refdate)
  strdate = '%d-%s-%s' %(refdate.year, str(refdate.month).zfill(2), str(refdate.day).zfill(2))
  return strdate

def get_refdate_from_strdate(strdate=None):
  if strdate is None or len(strdate) != 10:
    return get_refdate()
  try:
    pp = strdate.split('-')
    year = int(pp[0])
    month = int(pp[1])
    day = int(pp[2])
    return datetime.date(year, month, day)
  except IndexError:
    pass
  except ValueError:
    pass
  return get_refdate()



def test():
  date_str = get_strdate()
  print('default date_str', date_str)
  d = datetime.date(2020, 5, 19)
  date_str = get_strdate(d)
  print('given datetime.date to date_str', date_str, 'type', type(date_str))
  recup_date = get_refdate_from_strdate(date_str)
  print('recup_date', recup_date, 'type', type(recup_date))

def process():
  test()

if __name__ == '__main__':
  process()
