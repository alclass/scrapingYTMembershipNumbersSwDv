#!/usr/bin/python3
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
# from matplotlib.ticker import MaxNLocator

from models.gen_models.YtVideosPageMod import YtVideosPage
import models.procdb.SubscriberDaysMod as subsmod
import fs.numberfunctions.statisticsMod as statmod
from models.sa_models.ytchannelsubscribers_samodels import YTChannelSA
from fs.db.sqlalchdb.sqlalchemy_conn import sqlalchemy_engine
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
  days = list(map(lambda x : x.split('-')[-1], days))
  n_subscribers = list(map(lambda x : x[1], ytvideospage.days_n_subscribers))
  # n_subscribers_norm, basemin = normalize(n_subscribers)
  y_pos = np.arange(len(days))

  plt.clf()
  plt.bar(y_pos, n_subscribers, align='center', alpha=0.5)
  # fig, _ = plt.subplots()
  plt.xticks(y_pos, days)
  plt.ylabel('N de Inscritos')
  plt.title('Inscritos Dia a Dia')
  pngfile_abspath = ytvideospage.barchartpngfile_abspath
  print ('pngfile_abspath', pngfile_abspath)
  plt.savefig(pngfile_abspath)
  # plt.show()

def generate_figure():
  session = Session()
  channels = session.query(YTChannelSA).order_by(YTChannelSA.nname).all()
  for i, channel in enumerate(channels):
    ytvideospage = YtVideosPage(channel.ytchannelid, channel.nname)
    subsmod.SubscriberDayForChannel(ytvideospage)
    seq = i + 1
    print (seq, 'Saving png for', channel.nname)
    save_graphic_to_folder(ytvideospage)
  session.close()

def process():
  generate_figure()

if __name__ == '__main__':
  process()