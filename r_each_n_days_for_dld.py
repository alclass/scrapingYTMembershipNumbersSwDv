#!/usr/bin/python3
from models.procdb.EachNDaysForDownloadSyncerMod import EachNDaysForDownloadSyncer
from models.procdb.EachNDaysForDownloadSyncerMod import StaticEachNDays

def do_sync_to_each_n_days_for_dld():
  from_means = EachNDaysForDownloadSyncer.EACH_N_DAYS_ORIGIN_DICTFILE
  to_means = EachNDaysForDownloadSyncer.EACH_N_DAYS_TARGET_DB
  syncer = EachNDaysForDownloadSyncer(from_means, to_means)
  syncer.sync_means()
  print ('syncer.sync_means()')
  print (syncer)

def process():
  StaticEachNDays.show_dowloadables_at_moment()
  from_means = EachNDaysForDownloadSyncer.EACH_N_DAYS_ORIGIN_DICTFILE
  to_means = EachNDaysForDownloadSyncer.EACH_N_DAYS_TARGET_DB
  syncer = EachNDaysForDownloadSyncer(from_means, to_means)
  syncer.analyze_equality_from_to_means_recsize()

if __name__ == '__main__':
  process()
