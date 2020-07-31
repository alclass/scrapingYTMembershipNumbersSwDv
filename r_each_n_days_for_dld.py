#!/usr/bin/env python3
"""
Usage:
  $<this_script> <parameters>
Where parameters are:
  1) --from=<FROM_MEANS>
  2) --to=<TO_MEANS>
where either FROM_MEANS and TO_MEANS can hold the following values:
  1) DICT means a dictfile will be read (or written) with the each N days dictionary
  2) JSON the same as above for DICT but the file is of json-typed instead of dictfile-typed
  3) DB means information will be read (or written) to the configured DB

Defaults:
  the FROM default is DICT; the TO default is DB

Error case: if FROM and TO are equal, an error will be raised.
"""
import sys
from models.procdb.EachNDaysForDownloadSyncerMod import EachNDaysForDownloadSyncer
from models.procdb.EachNDaysForDownloadSyncerMod import StaticEachNDays

DEFAULT_FROM_ARG = 'DICT'
DEFAULT_TO_ARG = 'DB'


def translate_from_to_args(pdict):
  from_arg, to_arg = None, None
  try:
    from_arg = pdict['FROM']
  except IndexError:
    pass
  if from_arg is None:
    # set default for from_arg
    from_arg = DEFAULT_FROM_ARG
  try:
    to_arg = pdict['TO']
  except IndexError:
    pass
  if to_arg is None:
    # set default for to_arg
    to_arg = DEFAULT_TO_ARG

  from_arg = from_arg.upper()
  to_arg = to_arg.upper()
  if from_arg == to_arg:
    error_msg = 'Error: FROM (%s) and TO (%s) are the same. Please, look up doc-help with parameter --help ' \
                'to see options.' % (from_arg, to_arg)
    raise ValueError(error_msg)
  if from_arg == 'DICT':
    from_means = EachNDaysForDownloadSyncer.EACH_N_DAYS_ORIGIN_DICTFILE
  elif from_arg == 'JSON':
    from_means = EachNDaysForDownloadSyncer.EACH_N_DAYS_ORIGIN_JSONFILE
  elif from_arg == 'DB':
    from_means = EachNDaysForDownloadSyncer.EACH_N_DAYS_ORIGIN_DB
  else:
    error_msg = 'FROM (%s) is not available as option. Please, look up doc-help with parameter --help ' \
                'to see options.' % (str(from_arg))
    raise ValueError(error_msg)
  if to_arg == 'DICT':
    to_means = EachNDaysForDownloadSyncer.EACH_N_DAYS_TARGET_DICTFILE
  elif to_arg == 'JSON':
    to_means = EachNDaysForDownloadSyncer.EACH_N_DAYS_TARGET_JSONFILE
  elif to_arg == 'DB':
    to_means = EachNDaysForDownloadSyncer.EACH_N_DAYS_TARGET_DB
  else:
    error_msg = 'TO (%s) is not available as option. Please, look up doc-help with parameter --help' \
                ' to see options.' % (str(to_arg))
    raise ValueError(error_msg)
  return from_means, to_means


def do_sync_to_each_n_days_for_dld(dict_args):
  from_means, to_means = translate_from_to_args(dict_args)
  print('-'*50)
  print('Entered parameters')
  print('-'*50)
  print('from_means =', from_means)
  print('to_means   =', to_means)
  print('-'*50)
  ans = input('Are you sure? (Y/n)')
  if ans not in ['y', 'Y', '']:
    return
  print('-'*50)
  syncer = EachNDaysForDownloadSyncer(from_means, to_means)
  syncer.sync_means()
  print(' :: Running syncer.sync_means()')
  print(syncer)


def analyze():
  StaticEachNDays.show_dowloadables_at_moment()
  from_means = EachNDaysForDownloadSyncer.EACH_N_DAYS_ORIGIN_DB
  to_means = EachNDaysForDownloadSyncer.EACH_N_DAYS_TARGET_DICTFILE
  syncer = EachNDaysForDownloadSyncer(from_means, to_means)
  syncer.analyze_equality_from_to_means_recsize()


def get_args():
  dict_args = {'FROM': None, 'TO': None}
  for arg in sys.argv:
    if arg.startswith('--help'):
      print(__doc__)
      sys.exit()
    elif arg.startswith('-f='):
      dict_args['FROM'] = arg[len('-f='):]
    elif arg.startswith('-t='):
      dict_args['TO'] = arg[len('-t='):]
  return dict_args


def process():
  dict_args = get_args()
  do_sync_to_each_n_days_for_dld(dict_args)


if __name__ == '__main__':
  process()
