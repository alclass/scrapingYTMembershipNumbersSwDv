#!/usr/bin/env python3
"""
  docstring
"""
# import datetime
# import os
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Boolean, Integer, String, Date, DateTime, Time, TIMESTAMP, \
#   ForeignKey, Text, UniqueConstraint
# from sqlalchemy.types import BINARY
# from sqlalchemy.orm import relationship, backref
# from sqlalchemy.sql import text  # func
# import fs.datefunctions.datefs as dtfs
# from sqlalchemy.sql.expression import asc, desc
# import config
import fs.db.sqlalchdb.sqlalchemy_conn as saconn
import models.sa_models.ytchannelsubscribers_samodels as sam


def fetch_all_active_ytchannels_in_db(p_session=None):
  if p_session is None:
    session = saconn.Session()
  else:
    session = p_session
  ytchannels = session.query(sam.YTChannelSA).\
    filter(sam.YTChannelSA.active == 1).\
    order_by(sam.YTChannelSA.nname).\
    all()
  if p_session is None:
    session.close()
  return ytchannels


def fetch_all_channels_from_db(p_session):
  if p_session is None:
    session = saconn.Session()
  else:
    session = p_session
  dbytchannels = session.query(sam.YTChannelSA). \
      order_by(sam.YTChannelSA.nname). \
      all()
  if p_session is None:
    session.close()
  return dbytchannels


def fetch_sname_with_ytchannelid(ytchannelid):
  session = saconn.Session()
  ytchannel = session.query(sam.YTChannelSA.nname). \
      filter(sam.YTChannelSA.ytchannelid == ytchannelid). \
      first()
  if ytchannel is not None:
    sname = ytchannel.sname
    return sname
  session.close()
  return None


def fetch_ytchannel_with_likenname(likenname, p_session=None):
  if p_session is None:
    session = saconn.Session()
  else:
    session = p_session
  ytchannel = session.query(sam.YTChannelSA). \
      filter(sam.YTChannelSA.nname.like(likenname)). \
      first()
  if p_session is None:
    session.close()
  return ytchannel


def fetch_ytchannel_with_ytchannelid(ytchannelid, p_session=None):
  if p_session is None:
    session = saconn.Session()
  else:
    session = p_session
  ytchannel = session.query(sam.YTChannelSA). \
      filter(sam.YTChannelSA.ytchannelid == ytchannelid). \
      first()
  if p_session is None:
    session.close()
  return ytchannel


def adhoc_test():
  pass


def process():
  adhoc_test()


if __name__ == '__main__':
  process()
