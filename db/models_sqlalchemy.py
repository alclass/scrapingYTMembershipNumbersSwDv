#!/usr/bin/python3

# from db.sqlalchemy_conn import sqlalchemy_engine
# print(sqlalchemy_engine)

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

class Channel(Base):

  __tablename__ = 'channels'
  id = Column(Integer, primary_key=True)
  ytchannelid = Column(String, unique=True)
  nname = Column(String)
  obs = Column(String)

  def __repr__(self):
    return '<Channel(nname="%s", ytchid="%s")>' %(self.nname, self.ytchannelid)

#channel_ghira = Channel(ytchannelid='upgjr23', nname="Paulo Ghiraldelli")
#print (channel_ghira)

class DailySubscribers(Base):

  __tablename__ = 'dailychannelsubscribernumbers'
  id = Column(Integer, primary_key=True)
  subscribers = Column(Integer)
  date = Column(Date)

  ytchannelid = Column(String, ForeignKey('channels.ytchannelid'))
  ytchannel = relationship('Channel')

  def __repr__(self):
    return '<DailySubscribers(ytchid="%s", subscribers=%d, date="%s")>' % (self.ytchannelid, self.subscribers, str(self.date))

#daily19 = DailySubscribers(ytchannel=channel_ghira, subscribers=40, date='2020-05-19')
#daily20 = DailySubscribers(ytchannel=channel_ghira, subscribers=40, date='2020-05-20')
#print ('daily19', daily19)
#print ('daily19.ytchannel', daily19.ytchannel)
#print ('daily20', daily20)
#print ('daily20.ytchannel', daily20.ytchannel)

def process():
  pass

if __name__ == '__main__':
  process()
