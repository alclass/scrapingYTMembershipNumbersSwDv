#!/usr/bin/python3
import json, os
import config
import filefunctions.pathfunctions as pathfs
# from YtChannelMod import YtChannel
import readjson
from db.models_sqlalchemy import Channel

from db.sqlalchemy_conn import sqlalchemy_engine
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=sqlalchemy_engine)
session = Session()

def insert():
  reader = readjson.JsonYtChannel()
  for channeldict in reader.loopthru():
    nname = channeldict['nname']
    ytchid = channeldict['ytchid']
    channel = Channel(ytchannelid=ytchid, nname=nname)
    print (channel)
    session.add(channel)
  print('Committing...')
  session.commit()

def process():
  insert()

if __name__ == '__main__':
  process()
