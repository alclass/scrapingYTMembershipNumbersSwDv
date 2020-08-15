#!/usr/bin/env python3
"""
  docstring
"""
from models.procdb.SubscriberInsertorMod import Session
import models.sa_models.ytchannelsubscribers_samodels as samodels


def get_channels_from_db(session):
  dbytchannels = session.query(samodels.YTChannelSA). \
    order_by(samodels.YTChannelSA.nname). \
    all()
  return dbytchannels


def list_todays_downloadables():
  """
    Deactivated
  :return:
  """
  session = Session()
  not_dld_counter = 0
  dld_counter = 0
  for ytchannel in get_channels_from_db(session):
    if not ytchannel.is_downloadable_on_date():
      not_dld_counter += 1
      print(not_dld_counter, ytchannel.scrapedate, 'Not downloadable', ytchannel.nname)
      continue
    dld_counter += 1
    print(dld_counter, ytchannel.scrapedate, 'Downloadable', ytchannel.nname)
  session.close()
  print('dld_counter =', dld_counter, '| not_dld_counter = ', not_dld_counter)


def process():
  list_todays_downloadables()


if __name__ == '__main__':
  process()
