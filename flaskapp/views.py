from flask import render_template
from sqlalchemy.orm import sessionmaker
import models.sa_models.ytchannelsubscribers_samodels as samodels
from fs.db.sqlalchdb.sqlalchemy_conn import sqlalchemy_engine

Session = sessionmaker(bind=sqlalchemy_engine)

def output_ytchannel_lister():
  samodels.YTChannelSA()
  session = Session()
  ytchannels = session.query(samodels.YTChannelSA). \
    order_by(samodels.YTChannelSA.nname). \
    all()
  return render_template('ytchannel_lister_tmpl.html', title='ytchannels list', ytchannels=ytchannels)
