#!/usr/bin/env python3
"""
1  dateini = '2020-07-05' ; datefim = '2020-07-07'
  daterange = make_daterange_with_dateini_n_datefim(dateini, datefim)
  print ('dateini', dateini, 'datefim', datefim)
  print ('daterange', daterange)
2  dateini = '2021-07-05' ; datefim = '2020-07-11' # both above today when it's 2020-07-08
  daterange = make_daterange_with_dateini_n_datefim(dateini, datefim)
  print ('daterange', daterange)
3  dateini = '2020-07-11' ; datefim = '2020-07-06'
  daterange = make_daterange_with_dateini_n_datefim(dateini, datefim)
  print ('dateini', dateini, 'datefim', datefim)
  print ('daterange', daterange)
4  dateini = '2020-07-03' ; datefim = '2020-06-30'
  daterange = make_daterange_with_dateini_n_datefim(dateini, datefim)
  print ('dateini', dateini, 'datefim', datefim)
  print ('daterange', daterange)
"""
import datetime
import unittest
import fs.datefunctions.datefs as dtfs


class EmptyMock:
  pass


class TestCaseDates(unittest.TestCase):

  def test_convert_datetime_to_date(self):
    today = datetime.date.today()
    input_datetime = datetime.datetime(year=today.year, month=today.month, day=today.day)
    expected_date = today
    returned_date = dtfs.convert_datetime_to_date(input_datetime)
    self.assertEqual(expected_date, returned_date)
    input_datetime = datetime.datetime.now()
    # expected_date = today
    returned_date = dtfs.convert_datetime_to_date(input_datetime)
    self.assertEqual(expected_date, returned_date)
    date_mock_obj = EmptyMock()
    date_mock_obj.year = today.year
    date_mock_obj.month = today.month
    date_mock_obj.day = today.day
    returned_date = dtfs.convert_datetime_to_date(date_mock_obj)
    self.assertEqual(today, returned_date)

  def test_monthdelta(self):
    deltamonth = 3
    pdate = datetime.date(2020, 7, 8)
    expected_date = datetime.date(2020, 7+3, 8)
    returned_date = dtfs.add_or_subtract_to_month(pdate, deltamonth)
    self.assertEqual(expected_date, returned_date)
    deltamonth = 7
    pdate = datetime.date(2020, 7, 8)
    expected_date = datetime.date(2021, 2, 8)
    returned_date = dtfs.add_or_subtract_to_month(pdate, deltamonth)
    self.assertEqual(expected_date, returned_date)
    deltamonth = -3
    pdate = datetime.date(2020, 7, 8)
    expected_date = datetime.date(2020, 7-3, 8)
    returned_date = dtfs.add_or_subtract_to_month(pdate, deltamonth)
    self.assertEqual(expected_date, returned_date)
    deltamonth = -7
    pdate = datetime.date(2020, 7, 8)
    expected_date = datetime.date(2019, 12, 8)
    returned_date = dtfs.add_or_subtract_to_month(pdate, deltamonth)
    self.assertEqual(expected_date, returned_date)

  def test_make_daterange_with_dateini_n_datefim(self):

    dateini = '2020-07-05'
    datefim = '2020-07-07'
    expected_strdaterange = ['2020-07-05', '2020-07-06', '2020-07-07']
    expected_daterange = list(map(lambda strdate: dtfs.get_refdate_from_strdate(strdate), expected_strdaterange))
    returned_daterange = dtfs.make_daterange_with_dateini_n_datefim(dateini, datefim)
    self.assertEqual(expected_daterange, returned_daterange)

    dateini = '2220-07-05'
    datefim = '2220-07-07'
    expected_daterange = []
    returned_daterange = dtfs.make_daterange_with_dateini_n_datefim(dateini, datefim)
    self.assertEqual(expected_daterange, returned_daterange)

    dateini = '2020-07-03'
    datefim = '2020-06-29'
    expected_strdaterange = ['2020-07-03', '2020-07-02', '2020-07-01', '2020-06-30', '2020-06-29']
    expected_daterange = list(map(lambda strdate: dtfs.get_refdate_from_strdate(strdate), expected_strdaterange))
    returned_daterange = dtfs.make_daterange_with_dateini_n_datefim(dateini, datefim)
    self.assertEqual(expected_daterange, returned_daterange)

    dateini = None
    datefim = None
    today = datetime.date.today()
    expected_daterange = [today]
    returned_daterange = dtfs.make_daterange_with_dateini_n_datefim(dateini, datefim)
    self.assertEqual(expected_daterange, returned_daterange)

  def test_transform_duration_in_sec_into_hms(self):
    """
        the returned value will have a left-zero in the string, though as input (see below) the zero is not necessary
    :return:
    """
    duration_in_sec = 61
    expected_hms = '01:01'
    returned_hms = dtfs.transform_duration_in_sec_into_hms(duration_in_sec)
    self.assertEqual(expected_hms, returned_hms)

  def test_transform_hms_into_duration_in_sec(self):
    hms = '1:01'
    expected_duration_in_sec = 61
    returned_duration_in_sec = dtfs.transform_hms_into_duration_in_sec(hms)
    self.assertEqual(expected_duration_in_sec, returned_duration_in_sec)

  def test_ajust_calendardatestr_to_start_with_a_number(self):
    input_str = 'há 2 dias atrás'
    expected_output_str = '2 dias atrás'
    returned_output_str = dtfs.ajust_calendardatestr_to_start_with_a_number(input_str)
    self.assertEqual(expected_output_str, returned_output_str)
    input_str = '3 days ago'
    expected_output_str = '3 days ago'
    returned_output_str = dtfs.ajust_calendardatestr_to_start_with_a_number(input_str)
    self.assertEqual(expected_output_str, returned_output_str)
    input_str = 'blah bla 10 hours ahead'
    expected_output_str = '10 hours ahead'
    returned_output_str = dtfs.ajust_calendardatestr_to_start_with_a_number(input_str)
    self.assertEqual(expected_output_str, returned_output_str)
    input_str = 'blah bla 10'
    expected_output_str = '10'
    returned_output_str = dtfs.ajust_calendardatestr_to_start_with_a_number(input_str)
    self.assertEqual(expected_output_str, returned_output_str)
    input_str = 'blah bla no numbers here'
    expected_output_str = '1 hora'  # this is the default, try to move it to config.py
    returned_output_str = dtfs.ajust_calendardatestr_to_start_with_a_number(input_str)
    self.assertEqual(expected_output_str, returned_output_str)

  def test_DateAdderSubtractor(self):
    quant = 3
    unit = dtfs.DateAdderSubtractor.DA
    adder = dtfs.DateAdderSubtractor(unit, quant)
    input_date = datetime.date(2020, 7, 11)
    expected_date = datetime.date(2020, 7, 11-quant)
    returned_date = adder.add_from_datetime(input_date)
    self.assertEqual(expected_date, returned_date)
    quant = 3
    unit = dtfs.DateAdderSubtractor.DA
    adder = dtfs.DateAdderSubtractor(unit, quant, topast=False)
    input_date = datetime.date(2020, 7, 11)
    expected_date = datetime.date(2020, 7, 11+quant)
    returned_date = adder.add_from_datetime(input_date)
    self.assertEqual(expected_date, returned_date)
    quant = 8
    unit = dtfs.DateAdderSubtractor.MO
    adder = dtfs.DateAdderSubtractor(unit, quant)
    input_date = datetime.date(2020, 7, 11)
    expected_date = datetime.date(2019, 11, 11)
    returned_date = adder.add_from_datetime(input_date)
    self.assertEqual(expected_date, returned_date)
    quant = 2
    unit = dtfs.DateAdderSubtractor.WE
    adder = dtfs.DateAdderSubtractor(unit, quant)
    input_date = datetime.date(2020, 7, 11)
    expected_date = datetime.date(2020, 6, 27)
    returned_date = adder.add_from_datetime(input_date)
    self.assertEqual(expected_date, returned_date)
    quant = 3
    unit = dtfs.DateAdderSubtractor.WE
    adder = dtfs.DateAdderSubtractor(unit, quant, topast=False)
    input_date = datetime.date(2020, 7, 11)
    expected_date = datetime.date(2020, 8, 1)
    returned_date = adder.add_from_datetime(input_date)
    self.assertEqual(expected_date, returned_date)
    quant = 3
    unit = dtfs.DateAdderSubtractor.HO
    adder = dtfs.DateAdderSubtractor(unit, quant)
    input_datetime = datetime.datetime(2020, 7, 11, 4, 0, 0)
    expected_datetime = datetime.datetime(2020, 7, 11, 1, 0, 0)
    returned_datetime = adder.add_from_datetime(input_datetime)
    self.assertEqual(expected_datetime, returned_datetime)
    quant = 5
    unit = dtfs.DateAdderSubtractor.HO
    adder = dtfs.DateAdderSubtractor(unit, quant)
    input_datetime = datetime.datetime(2020, 7, 11, 4, 0, 0)
    expected_datetime = datetime.datetime(2020, 7, 10, 23, 0, 0)
    returned_datetime = adder.add_from_datetime(input_datetime)
    self.assertEqual(expected_datetime, returned_datetime)

  def test_transform_calendarstr_to_dateadder(self):
    calendar_date_str = '3 dias atrás'
    dtadder = dtfs.transform_calendarstr_to_dateadder(calendar_date_str)
    today = datetime.date.today()
    threedays = datetime.timedelta(days=3)
    expected_date = today - threedays
    returned_date = dtadder.add_from_datetime(today)
    self.assertEqual(expected_date, returned_date)

  def test_transform_date_to_datetime(self):
    """
For unit test:
  - for input None expected output is None
  - for input obj(2020, 07, 11) expected output is datetime(2020, 07, 11, 0, 0, 0)
  - for input obj(2020, 07) expected output is None
  - for input obj(2020, 07, 11, 11, 11, 11) expected output is the same as input typed-datetime
  - for input obj(2020, 07, 11, 11) expected output is datetime(2020, 07, 11, 11, 0, 0)
    """

    expected_datetime = None
    returned_datetime = dtfs.transform_datelike_to_datetime(None)
    self.assertEqual(expected_datetime, returned_datetime)
    input_pdt = datetime.date(2020, 7, 11)
    expected_datetime = datetime.datetime(2020, 7, 11, 0, 0, 0)
    returned_datetime = dtfs.transform_datelike_to_datetime(input_pdt)
    self.assertEqual(expected_datetime, returned_datetime)
    input_pdt = None
    expected_datetime = None
    returned_datetime = dtfs.transform_datelike_to_datetime(input_pdt)
    self.assertEqual(expected_datetime, returned_datetime)
