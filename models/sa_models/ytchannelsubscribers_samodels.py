#!/usr/bin/python3
import datetime, os # for adhoc test
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Boolean, Integer, String, Date, TIMESTAMP, ForeignKey, Text # DateTime,
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
import fs.datefunctions.datefs as dtfs
from sqlalchemy.sql.expression import asc, desc
import config

class YTChannelSA(Base):

  __tablename__ = 'channels'

  id = Column(Integer, primary_key=True)
  ytchannelid = Column(String, unique=True)
  nname = Column(String)
  category_id = Column(Integer, ForeignKey('nw_categories.id'), nullable=True)
  each_n_days_for_dld = Column(Integer, default=1)
  scrapedate = Column(Date, nullable=True)
  obs = Column(Text, nullable=True)

  daily_subscribers = relationship('YTDailySubscribersSA', backref='ytchannel', lazy='dynamic', order_by=(desc('infodate')))
  vinfolist = relationship('YTVideoItemInfoSA', backref='ytchannel', lazy='dynamic', order_by=(desc('publishdate')))

  created_at = Column(TIMESTAMP, server_default=func.now()) #, nullable=False, server_default=text('0'))
  updated_at = Column(TIMESTAMP, nullable=True)

  @property
  def first_subscribers(self):
    '''
      first_subscribers_n is the oldest subscribers number in database.
    :return:
    '''
    return self.daily_subscribers.order_by(None).order_by(asc('infodate')).first()

  @property
  def first_subscribers_n(self):
    subs = self.first_subscribers
    if subs:
      return subs.subscribers
    return 0

  @property
  def current_subscribers(self):
    '''
      first_subscribers_n is the oldest subscribers number in database.
    :return:
    '''
    return self.daily_subscribers.first() # notice it's default as a descending order_by above

  @property
  def current_subscribers_n(self):
    '''
      current_subscribers_n is the same as last_subscribers_n,
      ie, it's the most recent in date; eg if system is daily run,
      that may be today or yestearday depending on hour
    :return:
    '''
    curr_subs = self.current_subscribers
    if curr_subs:
      return curr_subs.subscribers
    return 0

  @property
  def videos_per_day(self):
    '''

    return 'hi'

    :return:
    '''
    return self.get_videos_per_day()

  def get_videos_per_day(self):
    total_videos = self.vinfolist.count()
    ndays = self.get_ndays_between_first_n_current()
    if ndays == 0:
      return 0.0
    return total_videos / ndays

  @property
  def ndays_first_current(self):
    return self.get_ndays_between_first_n_current()

  def get_ndays_between_first_n_current(self):
    dtini = None; dtfim = None
    if self.first_subscribers:
      dtini = self.first_subscribers.infodate
    else:
      return 0
    if self.current_subscribers:
      dtfim = self.current_subscribers.infodate
    else:
      return 0
    if dtini is None or dtfim is None:
      return 0
    timedelta = dtfim - dtini
    ndays = timedelta.days
    return ndays

  def is_downloadable_on_date(self):
    if self.scrapedate is None:
      return True
    today = datetime.date.today()
    timedelta = today - self.scrapedate
    if timedelta.days >= self.each_n_days_for_dld:
      return True
    return False

  def __repr__(self):
    return '<Channel(ytchannelid="%s", nname="%s")>' %(self.ytchannelid, self.nname)

class YTDailySubscribersSA(Base): # YTDailySubscribersSA <= DailySubscribers

  __tablename__ = 'dailychannelsubscribernumbers'

  id = Column(Integer, primary_key=True)
  subscribers = Column(Integer)
  infodate = Column(Date)

  ytchannelid = Column(String, ForeignKey('channels.ytchannelid'))
  #ytchannel = relationship(YTChannelSA)

  created_at = Column(TIMESTAMP, server_default=func.now()) #, nullable=False, server_default=text('0'))
  # created_at = Column(TIMESTAMP, default=datetime.utcnow) #, nullable=False, server_default=text('0'))
  updated_at = Column(TIMESTAMP, nullable=True)

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

  vviewlist = relationship('YTVideoViewsSA', backref='vinfo', lazy='dynamic', order_by=desc('infodate'))
  ytchannelid = Column(String, ForeignKey('channels.ytchannelid'))

  created_at = Column(TIMESTAMP, server_default=func.now()) #, nullable=False, server_default=text('0'))
  # created_at = Column(TIMESTAMP, default=datetime.utcnow) #, nullable=False, server_default=text('0'))
  updated_at = Column(TIMESTAMP, nullable=True)

  @property
  def duration_in_hms(self):
    return dtfs.transform_duration_in_sec_into_hms(self.duration_in_sec)

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

  created_at = Column(TIMESTAMP, server_default=func.now()) #, nullable=False, server_default=text('0'))
  # created_at = Column(TIMESTAMP, default=datetime.utcnow) #, nullable=False, server_default=text('0'))
  updated_at = Column(TIMESTAMP, nullable=True)

  def __repr__(self):
    return '<YTVideoViewsSA(ytvideoid="%s", views="%s", infdt="%s")>' %(self.ytvideoid, self.views, self.infodate)

class NewsArticlesSA(Base):
  '''
  video views taken from a videospage per date
  '''

  __tablename__ = 'newsarticles'

  id = Column(Integer, primary_key=True)
  title = Column(String)
  filename = Column(String)
  publisher_id = Column(Integer, ForeignKey('newspublishers.id'), nullable=True)
  publishdate = Column(Date, nullable=True)
  cat_id = Column(Integer, ForeignKey('newscategories.id'), nullable=True)
  reldir_id = Column(Integer, ForeignKey('relativefolders.id'), nullable=True)
  is_read = Column(Boolean, ForeignKey('newscategories.id'), nullable=True)
  personal_rank = Column(Integer, default=0)
  comment = Column(Text, nullable=True)
  created_at = Column(TIMESTAMP, server_default=func.now()) #, nullable=False, server_default=text('0'))
  updated_at = Column(TIMESTAMP, nullable=True)

  def __repr__(self):
    title = self.title
    if len(title) > 50:
      title = self.title[:50] + '...'
    return '<NewsArticlesSA(id=%d, date=%s, title="%s")>' %(self.id, self.publishdate, title)

class RelativeFolderSA(Base):
  '''
  '''

  __tablename__ = 'nw_relativefolders'

  id = Column(Integer, primary_key=True)
  parent_id = Column(Integer, ForeignKey('nw_relativefolders.id'))
  foldername = Column(String)

  entries = relationship('RelativeFolderSA', backref=backref('parent', remote_side=[id]))

  created_at = Column(TIMESTAMP, server_default=func.now()) #, nullable=False, server_default=text('0'))
  # created_at = Column(TIMESTAMP, default=datetime.utcnow) #, nullable=False, server_default=text('0'))
  updated_at = Column(TIMESTAMP, nullable=True)

  @property
  def parent_folder(self):
    return self.entries.filter('parent_id'==self.parent_id).first()

  @property
  def parent_foldername(self):
    '''
    '''
    parent_folder = self.parent_folder()
    if parent_folder:
      return parent_folder.foldername
    return 'w/inf'

  def __repr__(self):
    return '<NewsArticlesSA(id=%d, p_id=%d, folder="%s")>' %(self.id, self.p_id, self.foldername)

class CategorySA(Base):
  '''
  '''

  __tablename__ = 'nw_categories'

  id = Column(Integer, primary_key=True)
  category_id = Column(Integer, ForeignKey('nw_categories.id'))
  name = Column(String)
  created_at = Column(TIMESTAMP) #, default=datetime.utcnow, nullable=False, server_default=text('0'))
  updated_at = Column(TIMESTAMP)

  subcategories = relationship('CategorySA', backref=backref('category', remote_side=[id]))

  created_at = Column(TIMESTAMP, server_default=func.now()) #, nullable=False, server_default=text('0'))
  # created_at = Column(TIMESTAMP, default=datetime.utcnow) #, nullable=False, server_default=text('0'))
  updated_at = Column(TIMESTAMP, nullable=True)

  @property
  def parent_category(self):
    return self.entries.filter('category_id'==self.parent_id).first()

  @property
  def parent_name(self):
    '''
    '''
    if self.parent_category:
      return self.parent_category.name
    return 'w/inf'

  def __repr__(self):
    return '<NewsArticlesSA(id=%d, p_id=%d, folder="%s")>' %(self.id, self.p_id, self.foldername)

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
