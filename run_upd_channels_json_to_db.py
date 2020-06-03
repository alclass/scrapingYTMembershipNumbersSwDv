#!/usr/bin/python3
# from YtChannelMod import YtChannel
import readjson
from models.sqlalch_models.ytdailysubscribers_samodel import Channel

from fs.db.sqlalchemy_conn import sqlalchemy_engine
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=sqlalchemy_engine)

def process():
  insert_or_update_json_to_db()

def insert_or_update_json_to_db():
  reader = readjson.JsonYtChannel()
  n_added = 0
  session = Session()
  for i, channeldict in enumerate(reader.loopthru()):
    seq = i + 1
    nname = channeldict['nname']
    ytchid = channeldict['ytchannelid']
    channel_in_db = session.query(Channel).filter(Channel.ytchannelid==ytchid).first()
    if channel_in_db:
      if channel_in_db.nname != nname:
        oldname = channel_in_db.nname
        channel_in_db.nname = nname
        print (seq, 'Updating', oldname, 'to', nname)
        session.commit()
      else:
        print(seq, 'Channel ', nname, 'exists.')
      continue
    channel = Channel(ytchannelid=ytchid, nname=nname)
    print ('Adding', channel)
    session.add(channel)
    n_added += 1
  if n_added > 0:
    print('n_added =', n_added, '=> Committing...')
    session.commit()
  else:
    print('n_added =', n_added, '=> No commits.')
  session.close()


if __name__ == '__main__':
  process()
