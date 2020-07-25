#!/usr/bin/env python3
import datetime, os # for adhoc test
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Boolean, Integer, String, Date, DateTime, TIMESTAMP, ForeignKey, Text, UniqueConstraint # DateTime,
from sqlalchemy.types import BINARY
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
import fs.datefunctions.datefs as dtfs
from sqlalchemy.sql.expression import asc, desc
import config
import fs.db.sqlalchdb.sqlalchemy_conn as saconn


def get_all_ytchannelids():
  session = saconn.Session()
  ytchannels = session.query(YTChannelSA).order_by(YTChannelSA.nname).all()
  ytchannelids = list(map(lambda o : o.ytchannelid, ytchannels))
  session.close()
  return ytchannelids

class YTChannelSA(Base):

  __tablename__ = 'channels'

  id = Column(Integer, primary_key=True)
  ytchannelid = Column(String, unique=True)
  nname = Column(String)
  category_id = Column(Integer, ForeignKey('nw_categories.id'), nullable=True)
  each_n_days_for_dld = Column(Integer, default=1)
  # scrapedate = Column(Date, nullable=True) # now it's a property below
  obs = Column(Text, nullable=True)

  daily_subscribers = relationship('YTDailySubscribersSA', backref='ytchannel', lazy='dynamic', order_by=(desc('infodate')))
  vinfolist = relationship('YTVideoItemInfoSA', backref='ytchannel', lazy='dynamic', order_by=(desc('publishdatetime')))

  created_at = Column(TIMESTAMP, server_default=func.now()) #, nullable=False, server_default=text('0'))
  updated_at = Column(TIMESTAMP, nullable=True)

  @property
  def scrapedate(self):
    '''
    This attribute returns, if there is, most recent scrapedate in db for a ytchannel.
    The most recent scrapedate is taken from the daily_subscribers object list.
    Due to the desc() ordering function (see above in the fields declaration),
      its first element (index 0) is the most recent.
    The infodate attribute in this object is the sought-for most recent scrapedate.
    '''
    try:
      subs = self.daily_subscribers[0] # due to the desc() ordering function
      most_recent_scrapedate = subs.infodate
      return most_recent_scrapedate
    except IndexError:
      pass
    return None

  @property
  def most_recent_video(self):
    if self.vinfolist.count() > 0:
      return self.vinfolist[0]
    return None

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

  def find_next_download_date(self):
    today = datetime.date.today()
    if self.scrapedate is None:
      return today
    return self.scrapedate + datetime.timedelta(days=self.each_n_days_for_dld)

  def __repr__(self):
    return '<Channel(ytchannelid="%s", nname="%s")>' %(self.ytchannelid, self.nname)

class YTDailySubscribersSA(Base): # YTDailySubscribersSA <= DailySubscribers
  '''
  ALTER TABLE `dailychannelsubscribernumbers` ADD UNIQUE `infodate_n_subscribers_ytchannelid_uniq`(`subscribers`,`infodate`, `ytchannelid`);
  '''
  __tablename__ = 'dailychannelsubscribernumbers'

  id = Column(Integer, primary_key=True)
  subscribers = Column(Integer)
  infodate = Column(Date)

  ytchannelid = Column(String, ForeignKey('channels.ytchannelid'))
  #ytchannel = relationship(YTChannelSA)

  created_at = Column(TIMESTAMP, server_default=func.now()) #, nullable=False, server_default=text('0'))
  # created_at = Column(TIMESTAMP, default=datetime.utcnow) #, nullable=False, server_default=text('0'))
  updated_at = Column(TIMESTAMP, nullable=True)

  __table_args__ = (UniqueConstraint('infodate', 'subscribers', 'ytchannelid', name='infodate_n_subscribers_ytchannelid_uniq'),)

  def __repr__(self):
    return '<DailySubscribers(ytchannelid="%s", infdt="%s". subs=%d)>' % (self.ytchannelid, str(self.infodate), self.subscribers)

YT_VIDEO_URL_BASE_TO_INTERPOLATE = 'https://www.youtube.com/watch?v=%s'
class YTVideoItemInfoSA(Base):

  __tablename__ = 'individualvideostats'

  id = Column(Integer, primary_key=True)
  ytvideoid = Column(String(11), unique=True)
  title = Column(String)
  duration_in_sec = Column(Integer, nullable=True)
  publishdatetime = Column(DateTime, nullable=True)
  published_time_ago = Column(String(30))
  infodatetime = Column(DateTime, nullable=True)
  changelog = Column(Text, nullable=True)

  vviewlist = relationship('YTVideoViewsSA', backref='vinfo', lazy='dynamic', order_by=desc('infodate'))
  ytchannelid = Column(String, ForeignKey('channels.ytchannelid'))

  created_at = Column(TIMESTAMP, server_default=func.now()) #, nullable=False, server_default=text('0'))
  # created_at = Column(TIMESTAMP, default=datetime.utcnow) #, nullable=False, server_default=text('0'))
  updated_at = Column(TIMESTAMP, nullable=True)

  def recalc_n_return_publishdtime_from_infodtime_n_calendarstr(self):
    return dtfs.calculate_origdtime_from_targetdtime_n_calendarstr(self.infodatetime, self.published_time_ago)

  @property
  def duration_in_hms(self):
    return dtfs.transform_duration_in_sec_into_hms(self.duration_in_sec)

  @property
  def infodate(self):
    return dtfs.convert_datetime_to_date(self.infodatetime)

  @property
  def publishdate(self):
    return dtfs.convert_datetime_to_date(self.publishdatetime)

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
    return '<YTVideoItemInfoSA(ytvideoid="%s", title="%s", infdt="%s")>' %(self.ytvideoid, self.title, self.infodate)

class YTVideoViewsSA(Base):
  '''
  video views taken from a videospage per date
  ALTER TABLE `videosviews` ADD UNIQUE `infodate_n_ytvideoid_uniq`(`infodate`, `ytvideoid`);
  '''

  __tablename__ = 'videosviews'

  id = Column(Integer, primary_key=True)
  views = Column(Integer, nullable=True)
  infodate = Column(DateTime, nullable=True)

  ytvideoid = Column(String(11), ForeignKey('individualvideostats.ytvideoid'))
  # videoinfolist = relationship(YTVideoItemInfoSA)

  created_at = Column(TIMESTAMP, server_default=func.now()) #, nullable=False, server_default=text('0'))
  # created_at = Column(TIMESTAMP, default=datetime.utcnow) #, nullable=False, server_default=text('0'))
  updated_at = Column(TIMESTAMP, nullable=True)

  # ALTER TABLE `videosviews` ADD UNIQUE `infodate_n_ytvideoid_uniq`(`infodate`, `ytvideoid`);
  __table_args__ = (UniqueConstraint('infodate', 'ytvideoid', name='infodate_n_ytvideoid_uniq'),)

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
  sha1 = Column(BINARY)
  sizeinbytes = Column(Integer, nullable=True)
  publisher_id = Column(Integer, ForeignKey('nw_publishers.id'), nullable=True)
  publishdate = Column(Date, nullable=True)
  url = Column(String, nullable=True)
  url_main_img = Column(String, nullable=True)
  cat_id = Column(Integer, ForeignKey('nw_categories.id'), nullable=True)
  is_read = Column(Boolean, ForeignKey('nw_categories.id'), default=False)
  personal_rank = Column(Integer, default=0)
  summary = Column(Text, nullable=True)
  comment = Column(Text, nullable=True)
  created_at = Column(TIMESTAMP, server_default=func.now()) #, nullable=False, server_default=text('0'))
  updated_at = Column(TIMESTAMP, nullable=True)

  @property
  def sha1hex(self):
    '''
      Explanation:
        1) self.sha1 is a BINARY field in DB and a bytes class-attribute in-here;
        2) for visualization, this bytes/BINARY attribute/field is best seen when converted to a hexadecimal representation;
        3) the bytes-type has a .hex() method that does this conversion;
        4) so, it suffices to issue .hex() on the bytes attribute returning its hexadecimal representation.

      Notice
        1) that a sha1 hash is a 20-byte binary field and a 40-byte hexadecimal field (consider 8-bit bytes);
        2) because of that size issue, a binary field for sha1's is more memory-economic (twice as much) than its string/char counterpart.
    '''
    return self.sha1.hex()

  def __repr__(self):
    title = self.title
    if len(title) > 50:
      title = self.title[:50] + '...'
    return '<NewsArticlesSA(id=%s, date=%s, title="%s")>' %(str(self.id), self.publishdate, title)

class NewsPublishersSA(Base):
  '''
  video views taken from a videospage per date
  '''

  __tablename__ = 'nw_publishers'

  id = Column(Integer, primary_key=True)
  name = Column(String(40))
  created_at = Column(TIMESTAMP, server_default=func.now()) #, nullable=False, server_default=text('0'))
  updated_at = Column(TIMESTAMP, nullable=True)

  articles = relationship('NewsArticlesSA', backref='publisher', lazy='dynamic', order_by=(desc('publishdate')))

class RelativeFolderSA(Base):
  '''
  '''

  __tablename__ = 'nw_relativefolders'

  id = Column(Integer, primary_key=True)
  parent_id = Column(Integer, ForeignKey('nw_relativefolders.id'))
  tree_id = Column(Integer, ForeignKey('nw_treebaseabspaths.id'))
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

class TreeBaseAbsPath(Base):
  '''
  '''

  __tablename__ = 'nw_treebaseabspaths'

  id = Column(Integer, primary_key=True)
  app_tree_strkey = Column(String(30))
  abspath = Column(String, unique=True)
  medianame = Column(String(30), nullable=True)
  lookup_order = Column(Integer, default=1)
  created_at = Column(TIMESTAMP, server_default=func.now()) #, nullable=False, server_default=text('0'))
  updated_at = Column(TIMESTAMP, nullable=True)

  def __repr__(self):
    return '<TreeBaseAbsPath(id=%d, tree_key="%s", abspath="%s")>' %(self.id, self.app_tree_strkey, self.abspath)


class CategorySA(Base):
  '''
  '''

  __tablename__ = 'nw_categories'

  id = Column(Integer, primary_key=True)
  category_id = Column(Integer, ForeignKey('nw_categories.id'))
  name = Column(String)

  subcategories = relationship('CategorySA', backref=backref('category', remote_side=[id]))

  created_at = Column(TIMESTAMP, server_default=func.now()) #, nullable=False, server_default=text('0'))
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
