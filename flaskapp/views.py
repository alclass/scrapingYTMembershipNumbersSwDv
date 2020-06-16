from flask import render_template, g
import models.sa_models.ytchannelsubscribers_samodels as samodels
from models.sa_models.ytchannelsubscribers_samodels import YTChannelSA
from models.sa_models.ytchannelsubscribers_samodels import YTVideoViewsSA
# from models.sa_models.ytchannelsubscribers_samodels import YTVideoItemInfoSA
# import models.procdb.sqlalch_fetches as fetch

def list_ytchannels_view():
  # session = Session()
  ytchannels = g.sa_ext_session.query(samodels.YTChannelSA). \
    order_by(samodels.YTChannelSA.nname). \
    all()
  return render_template('ytchannel_lister_tmpl.html', title='ytchannels list', ytchannels=ytchannels)

def ytchannel_summary(ytchannelid): # former output_ytchannel_videos
  ytchannel = g.sa_ext_session.query(samodels.YTChannelSA). \
    filter(YTChannelSA.ytchannelid == ytchannelid). \
    first()
  return render_template('ytchannel_summary_tmpl.html', title='ytchannel summary', ytchannel=ytchannel)

def videos_per_channel(ytchannelid):
  ytchannel = g.sa_ext_session.query(YTChannelSA).filter(YTChannelSA.ytchannelid == ytchannelid).first()
  return render_template('videos_per_channel_tmpl.html', title='videos_per_channel', ytchannel=ytchannel)

def views_per_video(ytvideoid):
  vviews = g.sa_ext_session.query(YTVideoViewsSA).filter(YTVideoViewsSA.ytvideoid == ytvideoid).all()
  return render_template('views_per_video_tmpl.html', title='views_per_video', vviews=vviews)

def process():
  pass

if __name__ == '__main__':
  process()
