from flask import render_template, g
import models.sa_models.ytchannelsubscribers_samodels as samodels
from models.sa_models.ytchannelsubscribers_samodels import YTChannelSA
from models.sa_models.ytchannelsubscribers_samodels import YTVideoViewsSA

def list_ytchannels_view():
  # session = Session()
  ytchannels = g.sa_ext_session.query(samodels.YTChannelSA). \
    order_by(samodels.YTChannelSA.nname). \
    all()
  return render_template('ytchannel_lister_tmpl.html', title='YouTube Channels Observed', ytchannels=ytchannels)

def ytchannel_summary(ytchannelid): # former output_ytchannel_videos
  ytchannel = g.sa_ext_session.query(samodels.YTChannelSA). \
    filter(YTChannelSA.ytchannelid == ytchannelid). \
    first()
  title_sent = ytchannel.nname + ' Summary'
  return render_template('ytchannel_summary_tmpl.html', title=title_sent, ytchannel=ytchannel)

def videos_per_channel(ytchannelid):
  ytchannel = g.sa_ext_session.query(YTChannelSA).filter(YTChannelSA.ytchannelid == ytchannelid).first()
  title_sent = ytchannel.nname + ' Video Listing and Statistics'
  return render_template('videos_per_channel_tmpl.html', title=title_sent, ytchannel=ytchannel)

def views_per_video(ytvideoid):
  vviews = g.sa_ext_session.query(YTVideoViewsSA).filter(YTVideoViewsSA.ytvideoid == ytvideoid).all()
  return render_template('views_per_video_tmpl.html', title='Views per Video', vviews=vviews)

def process():
  pass

if __name__ == '__main__':
  process()
