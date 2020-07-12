#!/usr/bin/python3
'''
This script is just for a one (or at least few) use(s).

This script intends to correct db-column publishdatetime
  based on infodatetime and calendarstr (published_time_ago).

Due to a moment where the scraping of calendarstr (published_time_ago) was buggy,
  some publishdate data was recorded wrongly, some even in the future, ie, a video that exists was
  published in the future, that is obviously wrong (this script has already correct this problem).

Because of an upgrade expanding infodate (Date-typed) to infodatetime (DateTime-type),
  refactored together with this script,
  the old datum was left as day-midnight, ie, <date 00:00:00.0000>.

So, many videos were updated to sometime on the previous day to their actual date.
  That's easy to see, if calendarstr was "3 horas atrás", the date-midnight in infodatetime
  left the publishdatetime as previous-date-9-pm.  But most htmls were downloaded by midday and,
  for most of these cases, publishdatetime will be a bit out of the most corrected time.

An additional effort might correct the above stated problem,
  reading from the html file's timestamp. At any rate, this is not considered a critical aspect in-here,
  for times are already approximated in the youtube platform
  (a derivation from a calendarstr with a file's timestamp).

Moreover, newer downloads will have the file's timestamp attributed to infodatetime,
  so a date-midnight will only happen in case an html is downloaded by that time.

Also, the html files will be deleted somewhen in the future, so the exact daytime will be lost,
  but, as stated above, times are already a bit approximated, so it's okay for this app, for now.
'''
from models.sa_models.ytchannelsubscribers_samodels import YTVideoItemInfoSA
from fs.db.sqlalchdb.sqlalchemy_conn import Session
import fs.datefunctions.datefs as dtfs

def loop_vitems_to_correct_publishdatetime():
  filename = 'z_pubdate_analysis.log'
  fp = open(filename, 'w', encoding='utf8')
  session = Session()
  vitems = session.query(YTVideoItemInfoSA).all()
  n_need_change = 0
  for i, vi in enumerate(vitems):
    recalc_publishdtime = vi.recalc_n_return_publishdtime_from_infodtime_n_calendarstr()
    recalc_publishdt = dtfs.convert_datetime_to_date(recalc_publishdtime)
    if recalc_publishdt != vi.publishdate:
      n_need_change += 1
      line = str(n_need_change) + '/' + str(i+1) + ' infdt ' + str(vi.infodate)  + ' pubdt ' + str(vi.publishdate) + ' calend ' +  str(vi.published_time_ago)+ '\n'
      line += ' recalc ' + str(recalc_publishdt) +  ' [ needs updating ]' + '\n'
      fp.write(line)
      print(line)
      vi.publishdatetime = recalc_publishdtime
      session.commit()
  line = 'Number of corrected records = ' + str(n_need_change) + ' // Total video items records = ' + str(len(vitems)) + '\n'
  fp.write(line)
  print(line)
  fp.close()
  session.close()
  print ('Written', filename)

def process():
  loop_vitems_to_correct_publishdatetime()

if __name__ == '__main__':
  process()