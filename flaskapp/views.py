from flask import render_template
from sqlalchemy.orm import sessionmaker
import models.sa_models.ytchannelsubscribers_samodels as samodels
from fs.db.sqlalchdb.sqlalchemy_conn import sqlalchemy_engine

Session = sessionmaker(bind=sqlalchemy_engine)

def output_ytchannel_lister():
  session = Session()
  ytchannels = session.query(samodels.YTChannelSA). \
    order_by(samodels.YTChannelSA.nname). \
    all()
  return render_template('ytchannel_lister_tmpl.html', title='ytchannels list', ytchannels=ytchannels)

def fetch_ytchannels_videos(ytchannelid):

  session = Session()
  ytchannel = session.query(samodels.YTChannelSA, samodels.YTVideoItemInfoSA). \
    filter(samodels.YTChannelSA.ytchannelid == samodels.YTVideoItemInfoSA.ytchannelid). \
    first()
  print(ytchannel)

  videoviewsobj = session.query(samodels.YTVideoItemInfoSA, samodels.YTVideoViewsSA). \
    filter(samodels.YTVideoItemInfoSA.ytchannelid == ytchannelid). \
    filter(samodels.YTVideoViewsSA.ytvideoid == samodels.YTVideoItemInfoSA.ytvideoid). \
    order_by(samodels.YTVideoViewsSA.infodate). \
    all()
  session.close()
  return videoviewsobj

def output_ytchannel_videos(ytchannelid):
  videoviewsobjs = fetch_ytchannels_videos(ytchannelid)
  return render_template('ytvideo_views_tmpl.html', title='video views statistics', videoviewsobjs=videoviewsobjs)
