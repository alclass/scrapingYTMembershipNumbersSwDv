#!/usr/bin/python3
import datetime, os # for adhoc test
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
import config

class YTChannelSA(Base):

  __tablename__ = 'channels'

  id = Column(Integer, primary_key=True)
  ytchannelid = Column(String, unique=True)
  nname = Column(String)
  obs = Column(Text, nullable=True)

  daily_subscribers = relationship('YTDailySubscribersSA', backref='ytchannel', lazy='dynamic')
  vinfolist = relationship('YTVideoItemInfoSA', backref='ytchannel', lazy='dynamic')

  def __repr__(self):
    return '<Channel(ytchannelid="%s", nname="%s")>' %(self.ytchannelid, self.nname)

class YTDailySubscribersSA(Base): # YTDailySubscribersSA <= DailySubscribers

  __tablename__ = 'dailychannelsubscribernumbers'

  id = Column(Integer, primary_key=True)
  subscribers = Column(Integer)
  infodate = Column(Date)

  ytchannelid = Column(String, ForeignKey('channels.ytchannelid'))
  #ytchannel = relationship(YTChannelSA)

  def __repr__(self):
    return '<DailySubscribers(ytchid="%s", infdt="%s". subs=%d)>' % (self.ytchannelid, str(self.infodate), self.subscribers)

YT_VIDEO_URL_BASE_TO_INTERPOLATE = 'https://www.youtube.com/watch?v=%s'
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

  vviewlist = relationship('YTVideoViewsSA', backref='vinfo', lazy='dynamic')
  ytchannelid = Column(String, ForeignKey('channels.ytchannelid'))
  #ytchannel = relationship(YTChannelSA)

  @property
  def ytvideo_url(self):
    return self.get_ytvideo_url()

  def get_ytvideo_url(self):
    try:
      yturlbasetointerpolate = config.YTVIDEO_URL_BASE_TO_INTERPOLATE
    except AttributeError:
      yturlbasetointerpolate = 'https://www.youtube.com/watch?v=%s' # fallback_yturlbasetointerpolate
    return yturlbasetointerpolate %self.ytvideoid

  @property
  def local_matplot_png(self):
    return self.get_local_matplot_png()

  @property
  def matplot_image_filename(self):
    return '%s.png' %self.ytvideoid

  @property
  def matplot_image_abspath(self):
    flaskapp_abspath = config.get_flaskapp_abspath()
    imagefolder_abspath = os.path.join(flaskapp_abspath, 'img')
    image_abspath = os.path.join(imagefolder_abspath, self.matplot_image_filename)
    return image_abspath

  def get_local_matplot_png(self):
    url = 'http://127.0.0.1:5000/img/%s' %self.matplot_image_filename
    url = 'http://127.0.0.1:5000/img/test.png'
    return url

  def __repr__(self):
    return '<YTVideoItemInfoSA(ytvid="%s", title="%s", infdt="%s")>' %(self.ytvideoid, self.title, self.infodate)

class YTVideoViewsSA(Base):
  '''
  video views taken from a videospage per date
  '''

  __tablename__ = 'videosviews'

  id = Column(Integer, primary_key=True)
  views = Column(Integer, nullable=True)
  infodate = Column(Date, nullable=True)

  ytvideoid = Column(String(11), ForeignKey('individualvideostats.ytvideoid'))
  # videoinfolist = relationship(YTVideoItemInfoSA)

  def __repr__(self):
    return '<YTVideoViewsSA(ytvideoid="%s", views="%s", infdt="%s")>' %(self.ytvideoid, self.views, self.infodate)

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
