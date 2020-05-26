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
  obs = Column(String, nullable=True)

  def __repr__(self):
    return '<Channel(ytchannelid="%s", nname="%s")>' %(self.ytchannelid, self.nname)

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
    return '<DailySubscribers(ytchannelid="%s", date="%s". subscribers=%d)>' % (self.ytchannelid, str(self.date), self.subscribers)

def test():
  test_channel = Channel(ytchannelid='upgjr23', nname="Ghiraldelli Louco")
  print('test_channel', test_channel)
  daily19 = DailySubscribers(subscribers=40, date='2020-05-19', ytchannel=test_channel)
  daily20 = DailySubscribers(subscribers=37, date='2020-05-20', ytchannelid='upgjr23')
  print ('daily19', daily19)
  print ('daily19.ytchannel', daily19.ytchannel)
  print('daily19.ytchannelid', daily19.ytchannelid)
  print ('daily20', daily20)
  print ('daily20.ytchannel', daily20.ytchannel)

def process():
  test()

if __name__ == '__main__':
  process()
