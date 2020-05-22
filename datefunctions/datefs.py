#!/usr/bin/python3
import datetime

class UtilDater:

  @classmethod
  def get_refdate_inverted_fields_str(cls, p_refdate=None):
    refdate = p_refdate
    if refdate is None or type(refdate) != datetime.date:
      refdate = datetime.date.today()
    refdate_str = '%d-%s-%s' % (refdate.year, str(refdate.month).zfill(2), str(refdate.day).zfill(2))
    return refdate_str

def test():
  date_str = UtilDater.get_refdate_inverted_fields_str()
  print(date_str)
  d = datetime.date(2020, 5, 19)
  date_str = UtilDater.get_refdate_inverted_fields_str(d)
  print(date_str)

def process():
  test()

if __name__ == '__main__':
  process()
