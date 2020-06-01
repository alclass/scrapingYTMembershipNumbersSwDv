#!/usr/bin/python3
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
# from matplotlib.ticker import MaxNLocator

from models.YtVideosPageMod import YtVideosPage
import fs.db.SubscriberDaysMod as subsmod
import fs.statfunctions.statisticsMod as statmod
from fs.db.models_sqlalchemy import Channel
from fs.db.sqlalchemy_conn import sqlalchemy_engine
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=sqlalchemy_engine)

def normalize(n_subscribers):
  mini, maxi, diff, delt = statmod.calc_min_max_dif_del(n_subscribers)
  basemin  = mini - diff
  # basemax  = maxi + diff
  norm_list = list(map(lambda x: x - basemin, n_subscribers))
  return norm_list, basemin

def save_graphic_to_folder(ytvideospage):
  days = list(map(lambda x : x[0], ytvideospage.days_n_subscribers))
  n_subscribers = list(map(lambda x : x[1], ytvideospage.days_n_subscribers))
  n_subscribers_norm, basemin = normalize(n_subscribers)
  y_pos = np.arange(len(days))

  plt.bar(y_pos, n_subscribers_norm, align='center', alpha=0.5)
  fig, _ = plt.subplots()
  plt.xticks(y_pos, days)
  plt.ylabel('N de Inscritos')
  plt.title('Inscritos Dia a Dia')

  fig.savefig('henry.png')
  plt.show()

def generate_figure():
  session = Session()
  channel = session.query(Channel).filter(Channel.nname.contains('Henry')).first()
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