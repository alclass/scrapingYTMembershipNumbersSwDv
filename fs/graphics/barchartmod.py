#!/usr/bin/python3
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
# from matplotlib.ticker import MaxNLocator

from models.YtVideosPageMod import YtVideosPage
import fs.db.SubscriberDaysMod as subsmod
from fs.db.models_sqlalchemy import Channel
from fs.db.sqlalchemy_conn import sqlalchemy_engine
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=sqlalchemy_engine)

def save_graphic_to_folder(ytvideospage):
  days = list(map(lambda x : x[0], ytvideospage.days_n_subscribers))
  n_subscribers = list(map(lambda x : x[1], ytvideospage.days_n_subscribers))
  y_pos = np.arange(len(days))

  plt.bar(y_pos, n_subscribers, align='center', alpha=0.5)
  plt.xticks(y_pos, days)
  plt.ylabel('N de Inscritos')
  plt.title('Inscritos Dia a Dia')

  plt.show()

def generate_figure():
  session = Session()
  channel = session.query(Channel).filter(Channel.nname.contains('Clayson')).first()
  if channel is None:
    return
  ytvideospage = YtVideosPage(channel.ytchannelid, channel.nname)
  subsmod.SubscriberDayForChannel(ytvideospage)
  save_graphic_to_folder(ytvideospage)
  session.close()

def process():
  generate_figure()

if __name__ == '__main__':
  process()