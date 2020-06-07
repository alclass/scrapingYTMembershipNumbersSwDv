#!/usr/bin/python3
from models.procdb.SubscriberInsertorMod import Session
from models.sa_models.ytchannelsubscribers_samodels import YTChannelSA
from models.sa_models.ytchannelsubscribers_samodels import YTDailySubscribersSA
from models.gen_models.YtVideosPageMod import transpose_sqlalchs_to_ytvideopages
import fs.statfunctions.statisticsMod as statmod

class SubscriberDayForChannel:

  def __init__(self, channel):
    self.channel = channel
    self.find_daily_subscribers()

  def find_daily_subscribers(self):
    session = Session()
    dailysubs = session.query(YTDailySubscribersSA). \
      filter(YTDailySubscribersSA.ytchannelid == self.channel.ytchannelid). \
      order_by(YTDailySubscribersSA.infodate).all()
    # print('Channel', channel.nname, 'has', len(self.dailysubs), 'daily subscribers records.')
    if len(dailysubs) > 0:
      self.tabulate_subscribers_per_day(dailysubs)
    session.close()

  def tabulate_subscribers_per_day(self, dailysubs):
    days_n_subscribers = []
    for dailysub in dailysubs:
      strdate = str(dailysub.infodate)
      day_n_subscriber_tuple = (strdate, dailysub.subscribers)
      days_n_subscribers.append(day_n_subscriber_tuple)
    days_n_subscribers = sorted(days_n_subscribers, key=lambda x: x[0])
    self.channel.days_n_subscribers = days_n_subscribers

class SubscriberDays:

  def __init__(self):
    self.days_n_subscribers = []
    session = Session()
    channels = session.query(YTChannelSA).order_by(YTChannelSA.nname).all()
    self.channels = transpose_sqlalchs_to_ytvideopages(channels)
    session.close()
    self.loop_thru_channels()

  def loop_thru_channels(self):
    for channel in self.channels:
      SubscriberDayForChannel(channel)

  def print_days_n_subscribers_per_channel(self):
    print ('Fetched', len(self.channels), 'channels.')
    print('-'*50)
    for i, channel in enumerate(self.channels):
      if channel.days_n_subscribers is None:
        continue
      quantlist = list(map(lambda x: x[1], channel.days_n_subscribers))
      mini, maxi, diff, delt = statmod.calc_min_max_dif_del(quantlist)
      seq = i+1
      print(seq, channel.nname, len(channel.days_n_subscribers), channel.days_n_subscribers, mini, maxi, diff, delt)

def adhoc_test():
  pass

def process():
  adhoc_test()

if __name__ == '__main__':
  process()