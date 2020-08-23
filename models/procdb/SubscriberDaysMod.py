#!/usr/bin/env python3
import collections as coll
from models.procdb.SubscriberInsertorMod import Session
from models.sa_models.ytchannelsubscribers_samodels import YTChannelSA
from models.sa_models.ytchannelsubscribers_samodels import YTDailySubscribersSA
from models.gen_models.YtVideosPageMod import transpose_sqlalchs_to_ytvideopages
import fs.numberfunctions.statisticsmod as statM

subs_report_ntconstr = coll.namedtuple('SubsReport', 'seq nname d1 subs1 d2 subs2 d3 subs3 mini maxi diff delt')


def fill_in_subs_report_nt(seq, nname, d1, subs1, d2, subs2, d3, subs3, mini, maxi, diff, delt):
  return subs_report_ntconstr(
    seq=seq, nname=nname,
    d1=d1, subs1=subs1, d2=d2, subs2=subs2, d3=d3, subs3=subs3,
    mini=mini, maxi=maxi, diff=diff, delt=delt
  )


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

  def print_days_n_subscribers_per_channel(self, n_of_date_desc_rows=3):
    report_namedtuple_list = []
    print('Fetched', len(self.channels), 'channels.')
    print('-'*50)
    for i, channel in enumerate(self.channels):
      days_n_subscribers = channel.get_days_n_subscribers_within_desc_up_to_n_rows(n_of_date_desc_rows)
      if days_n_subscribers is None or len(days_n_subscribers) == 0:
        continue
      quantlist = list(map(lambda x: x[1], reversed(days_n_subscribers)))
      mini, maxi, diff, delt = statM.calc_min_max_dif_del(quantlist)
      seq = i+1
      print(seq, channel.nname, len(days_n_subscribers), days_n_subscribers, mini, maxi, diff, delt)
      days_n_subscribers = list(reversed(days_n_subscribers))
      date_n_subs = days_n_subscribers.pop()
      d1, subs1 = date_n_subs
      d1 = str(d1)
      date_n_subs = days_n_subscribers.pop()
      d2, subs2 = date_n_subs
      d2 = str(d2)
      date_n_subs = days_n_subscribers.pop()
      d3, subs3 = date_n_subs
      d3 = str(d3)
      report_namedtuple = fill_in_subs_report_nt(
        seq, channel.nname, d1, subs1, d2, subs2, d3, subs3, mini, maxi, diff, delt
      )
      report_namedtuple_list.append(report_namedtuple)
    return report_namedtuple_list


def adhoc_test():
  pass


def process():
  adhoc_test()


if __name__ == '__main__':
  process()
