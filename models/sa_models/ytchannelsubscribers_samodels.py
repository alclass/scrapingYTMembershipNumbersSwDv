#!/usr/bin/python3
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship

class YTChannelSA(Base):
  '''
  Channel class to channels sql-table
  '''
  __tablename__ = 'channels'
  id = Column(Integer, primary_key=True)
  ytchannelid = Column(String, unique=True)
  nname = Column(String)
  obs = Column(Text, nullable=True)

  def __repr__(self):
    return '<Channel(ytchannelid="%s", nname="%s")>' %(self.ytchannelid, self.nname)

class YTDailySubscribersSA(Base): # YTDailySubscribersSA <= DailySubscribers
  '''
  DailySubscribers class to dailychannelsubscribernumbers sql-table
  '''
  __tablename__ = 'dailychannelsubscribernumbers'
  id = Column(Integer, primary_key=True)
  subscribers = Column(Integer)
  date = Column(Date)

  ytchannelid = Column(String, ForeignKey('channels.ytchannelid'))
  ytchannel = relationship(YTChannelSA)

  def __repr__(self):
    return '<DailySubscribers(ytchannelid="%s", date="%s". subscribers=%d)>' % (self.ytchannelid, str(self.date), self.subscribers)

class YTVideoItemInfoSA(Base):
  '''
  Channel class to channels sql-table
  '''
  __tablename__ = 'individualvideostats'
  id = Column(Integer, primary_key=True)
  ytvideoid = Column(String(11), unique=True)
  title = Column(String)
  duration_in_sec = Column(Integer, nullable=True)
  views = Column(Integer, nullable=True)
  publishdate = Column(Date, nullable=True)
  published_time_ago = Column(String(30), unique=True)
  info_refdate = Column(Date, nullable=True)
  changelog = Column(Text, nullable=True)

  ytchannelid = Column(String, ForeignKey('channels.ytchannelid'))
  ytchannel = relationship(YTChannelSA)

  def __repr__(self):
    return '<YTVideoItemInfoSA(ytvideoid="%s", title="%s", views="%s")>' %(self.ytvideoid, self.title, self.views)

def test():
  pass

def process():
  test()

if __name__ == '__main__':
  process()
