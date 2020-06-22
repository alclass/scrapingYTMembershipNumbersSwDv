from flask import render_template, g
import models.sa_models.ytchannelsubscribers_samodels as samodels

def list_ytchannels_view():
  # session = Session()
  ytchannels = g.sa_ext_session.query(samodels.YTChannelSA). \
    order_by(samodels.YTChannelSA.nname). \
    all()
  return render_template('ytchannel_lister_tmpl.html', title='YouTube Channels Observed', ytchannels=ytchannels)

def ytchannel_summary(ytchannelid): # former output_ytchannel_videos
  ytchannel = g.sa_ext_session.query(samodels.YTChannelSA). \
    filter(samodels.YTChannelSA.ytchannelid == ytchannelid). \
    first()
  vinfolist = ytchannel.vinfolist
  if vinfolist.count() > 20:
    vinfolist = ytchannel.vinfolist[ : 20] # .query.paginate(1, 20).items
  title_sent = ytchannel.nname + ' Summary'
  return render_template('ytchannel_summary_tmpl.html', title=title_sent, ytchannel=ytchannel, vinfolist=vinfolist)

def videos_per_channel(ytchannelid):
  ytchannel = g.sa_ext_session.query(samodels.YTChannelSA).filter(samodels.YTChannelSA.ytchannelid == ytchannelid).first()
  title_sent = ytchannel.nname + ' Video Listing and Statistics'
  return render_template('videos_per_channel_tmpl.html', title=title_sent, ytchannel=ytchannel)

def views_per_video(ytvideoid):
  ini = 1; fim = 20
  vviews = g.sa_ext_session.query(samodels.YTVideoViewsSA).filter(samodels.YTVideoViewsSA.ytvideoid == ytvideoid).paginate(ini, fim,False).items
  return render_template('views_per_video_tmpl.html', title='Views per Video', vviews=vviews)

def newsarticles():
  articles = g.sa_ext_session.query(samodels.NewsArticlesSA).all()
  return render_template('newsarticles_tmpl.html', title='News Articles', articles=articles)

def process():
  pass

if __name__ == '__main__':
  process()
