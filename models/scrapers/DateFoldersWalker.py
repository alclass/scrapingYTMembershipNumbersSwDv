#!/usr/bin/python3
'''
  This script scrapes video items through out the html video page
  Without parameter, it scrapes today's folder.
  An optional parameter --daysbefore=<n> scrapes n days before, if related folder exists.
'''
import os
import fs.filefunctions.autofinders as autofind
import fs.textfunctions.regexp_helpers as regexp
from adhoctasks.obsolete.YTVideoItemScraperMod import YTVideoItemScraper

def scrape_htmls_in_datenamed_folder(datefolder_abspath, strdate, seq_date):
  '''
  This routine processes all html video-items files in a datenamed folder.

  :param datefolder_abspath:
  :param strdate:
  :param seq_date:
  :return:
  '''
  print ('-'*50)
  print(strdate, datefolder_abspath)
  print ('-'*50)
  entries = os.listdir(datefolder_abspath)
  entries = sorted(entries)
  for i, htmlfilename in enumerate(entries):
    _, ext = os.path.splitext(htmlfilename)
    if ext != '.html':
      continue
    html_counter = i + 1
    print (seq_date, html_counter, htmlfilename)
    name_without_ext, _ = os.path.splitext(htmlfilename)
    refdate, sname, ytchannelid = regexp.find_triple_date_sname_n_ytchid_in_filename(name_without_ext)
    scraper = YTVideoItemScraper(ytchannelid, refdate, sname)
    print(scraper)
    scraper.scrape_html_on_folder()
    scraper.save_to_db()
  #if seq_dates > 1:
  print (seq_date, 'st/nd/rd/th infodate: on:', strdate)
  # return

def walk_thru_all_datenamed_folders():
  dates_n_abspaths_od = autofind.get_ordered_dict_with_dates_n_abspaths()
  for i, strdate in enumerate(dates_n_abspaths_od):
    seq_date = i + 1
    datefolder_abspath = dates_n_abspaths_od[strdate]
    scrape_htmls_in_datenamed_folder(datefolder_abspath, strdate, seq_date)
