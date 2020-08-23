#!/usr/bin/env python3
"""
  docstring
"""
import datetime
from models.procdb.SubscriberInsertorMod import Session
# import models.sa_models.ytchannelsubscribers_samodels as samodels
import fs.db.dbfetchers.centralfetchersmod as fetcher


def list_todays_downloadables():
  """
    Deactivated
  :return:
  """
  session = Session()
  not_dld_counter = 0
  dld_counter = 0
  today = datetime.date.today()
  ytchannels = fetcher.fetch_all_active_ytchannels_in_db(session)
  for ytchannel in ytchannels:
    if not ytchannel.is_downloadable_on_date():
      not_dld_counter += 1
      # print(not_dld_counter, ytchannel.scrapedate, 'Not downloadable', ytchannel.nname)
      continue
    dld_counter += 1
    deltatime = today - ytchannel.scrapedate
    ndaysago = deltatime.days
    print(dld_counter, 'last dld on', ndaysago, 'days ago | dld on each', ytchannel.each_n_days_for_dld, 'days | nname', ytchannel.nname)
  session.close()
  print('dld_counter =', dld_counter, '| not_dld_counter = ', not_dld_counter)


def process():
  list_todays_downloadables()


if __name__ == '__main__':
  process()
