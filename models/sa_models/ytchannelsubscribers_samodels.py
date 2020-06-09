#!/usr/bin/python3
import datetime # for adhoc test
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship

class YTChannelSA(Base):

  __tablename__ = 'channels'

  id = Column(Integer, primary_key=True)
  ytchannelid = Column(String, unique=True)
  nname = Column(String)
  obs = Column(Text, nullable=True)

  def __repr__(self):
    return '<Channel(ytchannelid="%s", nname="%s")>' %(self.ytchannelid, self.nname)

class YTDailySubscribersSA(Base): # YTDailySubscribersSA <= DailySubscribers

  __tablename__ = 'dailychannelsubscribernumbers'

  id = Column(Integer, primary_key=True)
  subscribers = Column(Integer)
  infodate = Column(Date)

  ytchannelid = Column(String, ForeignKey('channels.ytchannelid'))
  ytchannel = relationship(YTChannelSA)

  def __repr__(self):
    return '<DailySubscribers(ytchannelid="%s", infodate="%s". subscribers=%d)>' % (self.ytchannelid, str(self.infodate), self.subscribers)

class YTVideoItemInfoSA(Base):

  __tablename__ = 'individualvideostats'

  id = Column(Integer, primary_key=True)
  ytvideoid = Column(String(11), unique=True)
  title = Column(String)
  duration_in_sec = Column(Integer, nullable=True)
  publishdate = Column(Date, nullable=True)
  published_time_ago = Column(String(30))
  infodate = Column(Date, nullable=True)
  changelog = Column(Text, nullable=True)

  ytchannelid = Column(String, ForeignKey('channels.ytchannelid'))
  ytchannel = relationship(YTChannelSA)

  def __repr__(self):
    return '<YTVideoItemInfoSA(ytvideoid="%s", title="%s")>' %(self.ytvideoid, self.title)

class YTVideoViewsSA(Base):
  '''
  video views taken from a videospage per date
  '''

  __tablename__ = 'videosviews'

  id = Column(Integer, primary_key=True)
  views = Column(Integer, nullable=True)
  infodate = Column(Date, nullable=True)

  ytvideoid = Column(String(11), ForeignKey('individualvideostats.ytvideoid'))
  ytvideo = relationship(YTVideoItemInfoSA)

  @property
  def ytchannel(self):
    if self.ytvideo:
      if self.ytvideo.ytchannel:
        return self.ytvideo.ytchannel
    return 'w/o inf'

  def __repr__(self):
    return '<YTVideoViewsSA(ytvideoid="%s", views="%s")>' %(self.ytvideoid, self.views)

def adhoc_test():
  ytchannel_sa = YTChannelSA()
  ytchannel_sa.ytchannelid = 'ueduardoamoreira'
  ytchannel_sa.nname = 'Eduardo Moreira'
  print ('ytchannel_sa', ytchannel_sa)
  subscriber_sa = YTDailySubscribersSA()
  subscriber_sa.infodate = datetime.date(2020, 5, 30)
  subscriber_sa.subscribers = 1234
  subscriber_sa.ytchannelid = ytchannel_sa.ytchannelid
  print ('subscriber_sa', subscriber_sa)
  videoiteminfo_sa = YTVideoItemInfoSA()
  videoiteminfo_sa.ytvideoid = '1234-678_ab'
  videoiteminfo_sa.title = 'Title 1234-678_ab'
  videoiteminfo_sa.infodate = datetime.date(2020, 5, 30)
  # videoiteminfo_sa.ytchannel = ytchannel_sa
  print ('videoiteminfo_sa', videoiteminfo_sa)
  videoviews_sa = YTVideoViewsSA()
  videoviews_sa.ytvideoid = 'vid12345678'
  videoviews_sa.views = 12345
  videoviews_sa.infodate = datetime.date(2020, 5, 30)
  videoviews_sa.ytvideo = videoiteminfo_sa
  print ('videoviews_sa', videoviews_sa)
  print ('videoviews_sa.ytvideo', videoviews_sa.ytvideo)
  print ('videoviews_sa.ytchannel', videoviews_sa.ytchannel)

def process():
  adhoc_test()

if __name__ == '__main__':
  process()
