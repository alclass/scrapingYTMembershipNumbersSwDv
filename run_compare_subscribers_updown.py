#!/usr/bin/python3
from fs.db.SubscriberInsertorMod import Session
from fs.db.models_sqlalchemy import Channel
from fs.db.models_sqlalchemy import DailySubscribers
from models.YtVideosPageMod import transpose_sqlalchs_to_ytvideopages

class SubscriberDays:

  def __init__(self):
    self.days_n_subscribers = []
    self.session = Session()
    channels = self.session.query(Channel).order_by(Channel.nname).all()
    self.channels = transpose_sqlalchs_to_ytvideopages(channels)
    self.loop_thru_channels()

  def loop_thru_channels(self):
    for channel in self.channels:
      self.dailysubs = self.session.query(DailySubscribers).\
        filter(DailySubscribers.ytchannelid==channel.ytchannelid).\
        order_by(DailySubscribers.date).all()
      # print('Channel', channel.nname, 'has', len(self.dailysubs), 'daily subscribers records.')
      if len(self.dailysubs) > 0:
        self.tabulate_subscribers_per_day(channel)

  def tabulate_subscribers_per_day(self, channel):
      days_n_subscribers = []
      for dailysub in self.dailysubs:
        strmonth = str(dailysub.date.month)
        strday   = str(dailysub.date.day)
        mon_day = '%s/%s' %(strday, strmonth)
        day_n_subscriber_tuple = (mon_day, dailysub.subscribers)
        days_n_subscribers.append(day_n_subscriber_tuple)
      days_n_subscribers = sorted(days_n_subscribers, key=lambda x : x[0])
      channel.days_n_subscribers = days_n_subscribers

  def print_days_n_subscribers_per_channel(self):
    print ('Fetched', len(self.channels), 'channels.')
    print('-'*50)
    for i, channel in enumerate(self.channels):
      if channel.days_n_subscribers is None:
        continue
      quantlist = list(map(lambda x: x[1], channel.days_n_subscribers))
      mini, maxi, diff, delt = calc_min_max_dif_del(quantlist)
      seq = i+1
      print(seq, channel.nname, len(channel.days_n_subscribers), channel.days_n_subscribers, mini, maxi, diff, delt)

def calc_min_max_dif_del(alist):
  if alist is None or len(alist) == 0:
    return (0, 0, 0, 0)
  mini = 1000 ** 4;   maxi = -1
  first = alist[0];   last = alist[-1]
  delt = last - first
  for n in alist:
    if n > maxi:
      maxi = n
    if n < mini:
      mini = n
  diff = maxi - mini
  return (mini, maxi, diff, delt)

def process():
  sd = SubscriberDays()
  sd.print_days_n_subscribers_per_channel()

if __name__ == '__main__':
  process()
