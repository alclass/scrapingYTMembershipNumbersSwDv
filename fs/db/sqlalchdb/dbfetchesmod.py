#!/usr/bin/env python3
"""
  docstring
"""
from models.procdb.SubscriberInsertorMod import Session
import models.sa_models.ytchannelsubscribers_samodels as samodels


def fetch_ytchannel_by_ytchannelid(ytchannelid, session):
  return session.query(samodels.YTChannelSA).filter(samodels.YTChannelSA.ytchannelid == ytchannelid).first()


def fetch_ytchannel_by_ytchannelid_n_transpose(ytchannelid, transposedobj):
  """
    The idea of transpose is to transfer the attributes from a SqlAlchemy object to a non-SqlAlchemy object
    It's done as a way to close the session inside function and have the object available with an open db-session
    (There may exist a better solution for this.)

    Notice:
      This function is a method in YtVideosPage in order to avoid importing to samodels
      To avoid direct-cross-importing (which results in crash/error) the adhoc test is in a different module.

  :param ytchannelid:
  :param transposedobj:
  :return:
  """
  transposed = False
  session = Session()
  ytchannel = session.query(samodels.YTChannelSA).filter(samodels.YTChannelSA.ytchannelid == ytchannelid).first()
  if ytchannel:
    transposedobj.transpose(ytchannel)
    transposed = True
  session.close()
  if transposed:
    return True
  return False


def show_downloadables():
  session = Session()
  ytchannels = session.query(samodels.YTChannelSA).order_by(samodels.YTChannelSA.nname).all()
  total = len(ytchannels)
  n_of_dld = 0
  for ytchannel in ytchannels:
    isdld = ytchannel.is_downloadable_on_date()
    if isdld:
      n_of_dld += 1
    print(isdld, ' <== downloadable', ytchannel.nname)
  print(' ==       n_of_dld =', n_of_dld, 'total', total)
  session.close()


def adhoc_test():
  show_downloadables()
  print('The transpose object adhoc test is performed in the dbfetchesmod_adhoctest script.')


def process():
  adhoc_test()


if __name__ == '__main__':
  process()
