from flask import render_template
from sqlalchemy.orm import sessionmaker
import models.sa_models.ytchannelsubscribers_samodels as samodels
import models.procdb.sqlalch_fetches as fetch
from fs.db.sqlalchdb.sqlalchemy_conn import sqlalchemy_engine
from models.sa_models.ytchannelsubscribers_samodels import YTChannelSA
from models.sa_models.ytchannelsubscribers_samodels import YTVideoItemInfoSA
from models.sa_models.ytchannelsubscribers_samodels import YTVideoViewsSA

Session = sessionmaker(bind=sqlalchemy_engine)

def list_ytchannels_view():
  session = Session()
  ytchannels = session.query(samodels.YTChannelSA). \
    order_by(samodels.YTChannelSA.nname). \
    all()
  return render_template('ytchannel_lister_tmpl.html', title='ytchannels list', ytchannels=ytchannels)

def ytchannel_summary(ytchannelid): # former output_ytchannel_videos
  session = Session()
  ytchannel = session.query(samodels.YTChannelSA). \
    filter(YTChannelSA.ytchannelid == ytchannelid). \
    first()
  return render_template('ytchannel_summary_tmpl.html', title='ytchannel summary', ytchannel=ytchannel)

def videos_per_channel(ytchannelid):
  session = Session()
  ytchannel = session.query(YTChannelSA).filter(YTChannelSA.ytchannelid == ytchannelid).first()
  # session.close()
  return render_template('videos_per_channel_tmpl.html', title='videos_per_channel', ytchannel=ytchannel)

def views_per_video(ytvideoid):
  session = Session()
  vviews = session.query(YTVideoViewsSA).filter(YTVideoViewsSA.ytvideoid == ytvideoid).all()
  return render_template('views_per_video_tmpl.html', title='views_per_video', vviews=vviews)

def process():
  pass


if __name__ == '__main__':
  process()