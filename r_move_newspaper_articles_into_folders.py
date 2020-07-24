#!/usr/bin/env python3
import os
import fs.filefunctions.pathfunctions as pathfs
import models.gen_models.DatedFileMod as dtflmod

class NewsArticlesTreeWalker:

  def __init__(self):
    self.moved = 0; self.ins_or_upd = 0; self.passcount = 0; self.os_del = 0; self.db_del = 0
    self.base_abspath = dtflmod.get_newsarticles_base_abspath_from_db_or_cfg()

  def db_inspect_delete(self):
    print ('NewsArticlesTreeWalker.db_delete() not implemented yet')

  def db_inspect_ins_or_upd(self):
    for fromplace_n_filename in self.walk_up_tree_generator():
      _, filename = fromplace_n_filename
      insertor = dtflmod.HTMLDatedFileInsertDB(self.base_abspath, filename)
      if insertor.insert():
        self.ins_or_upd += 1
      else:
        print('Insert not happened: ', insertor)

  def os_move_to_canonplace(self):
    for fromplace_n_filename in self.walk_up_tree_generator():
      fromplace_abspath, filename = fromplace_n_filename
      printfile = filename if len(filename) < 20 else filename[:20]
      print('Move File: ', self.moved, '/', self.passcount, printfile)
      mover = dtflmod.MoveableFile(self.base_abspath, fromplace_abspath, filename)
      if mover.move():
        self.moved += 1

  def os_repeats_delete(self):
    print ('NewsArticlesTreeWalker.os_delete() not implemented yet')

  def walk_up_tree_generator(self):
    for fromplace_abspath, _, filenames in os.walk(self.base_abspath):
      for filename in filenames:
        self.passcount += 1
        if not pathfs.is_htmldatedfilename_under_convention(filename):
          continue
        fromplace_n_filename = fromplace_abspath, filename
        yield fromplace_n_filename

  def report(self):
    print(' [Report]')
    print('=> base_abspath =', self.base_abspath)
    print('=> moved =', self.moved, ' => passcount =', self.passcount, ' => ins/upd =', self.ins_or_upd)

def process():
  walker = NewsArticlesTreeWalker()
  walker.os_move_to_canonplace()
  walker.report()

if __name__ == '__main__':
  process()
