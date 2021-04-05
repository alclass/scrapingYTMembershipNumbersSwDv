#!/usr/bin/env python3
"""
deputados_whatsapp
"""
import os
from config import get_local_dados_foldername
from models.sa_models.ytchannelsubscribers_samodels import DeputadoWhatsappSA as SADeput
from fs.db.sqlalchdb.sqlalchemy_conn import Session


filename = 'deputados-whatsapp.txt'
linestartwith = '<option value="'
lineendswith = '</option>'


class DeputadoWhatsapp:

  def __init__(self, nomeparlamentar, uf, partido, cellphone):
    self.nomeparlamentar = nomeparlamentar
    self.uf = uf
    self.partido = partido
    self.cellphone = cellphone

  @staticmethod
  def get_name_partido_dash_separated(line):
    pp = line.split(' - ')
    nomeparlamentar = pp[0]
    nomeparlamentar = nomeparlamentar.lstrip(' ').rstrip(' ')
    partido = 's/n'
    if len(pp) > 1:
      partido = pp[1]
      partido = partido.lstrip(' ').rstrip(' ')
    return nomeparlamentar, partido

  def __str__(self):
    outstr = '<DeputWA n="{nomeparlamentar}" e="{uf}" p="{partido}" whatsapp="{cellphone}">'\
      .format(nomeparlamentar=self.nomeparlamentar, uf=self.uf, partido=self.partido, cellphone=self.cellphone)
    return outstr


def parse_input_file():
  phonesdict = {}
  repeats = []
  filepath = os.path.join(get_local_dados_foldername(), filename)
  for i, line in enumerate(open(filepath).readlines()):
    name, uf, partido, phone = None, None, None, None
    if line.startswith(linestartwith):
      line = line.lstrip(linestartwith)
      line = line.rstrip(' \t\r\n')
      if line.endswith(lineendswith):
        line = line.rstrip(lineendswith)
      phone = line[2:13]  # leave out the first 2 digits (the phone's country code) for they are all 55!
      uf = line[15:17]
      line = line[20:]
      name, partido = DeputadoWhatsapp.get_name_partido_dash_separated(line)
    if name is None or uf is None or partido is None or phone is None:
      print('Some is None', name, uf, partido, phone)
      continue
    dw = DeputadoWhatsapp(name, uf, partido, phone)
    supposed_dw = phonesdict.get(phone, None)
    if supposed_dw is not None:
      repeats.append(dw)
    phonesdict[phone] = dw
    seq = i + 1
    print(seq, dw)

  print('total', len(phonesdict))
  for repeat in repeats:
    print('repeated', repeat, phonesdict[repeat.cellphone])
  return phonesdict


def db_insert_or_update_if_needed(phonesdict):
  session = Session()
  n_not_inserted = 0
  n_updates = 0
  for i, cellphone in enumerate(phonesdict):
    seq = i + 1
    dw = phonesdict[cellphone]
    do_commit = False
    sadeput = session.query(SADeput) \
        .filter(
          SADeput.nomeparlamentar == dw.nomeparlamentar,
          # SADeput.uf == dw.uf,
          # SADeput.partido == dw.partido,
        ) \
        .first()
    if sadeput is None:
      n_not_inserted += 1
      print(n_not_inserted, seq,
            'this script does not insert '
            '(either nomeparlamentar is wrong or outdated or needs polishing) =>', str(dw))
      continue
    if sadeput.cellphone != dw.cellphone:
      do_commit = True
      sadeput.cellphone = dw.cellphone
    if do_commit:
      n_updates += 1
      print('n_updates', n_updates, 'committing', sadeput)
      session.commit()
  print('n_updates', n_updates, 'n_not_inserted', n_not_inserted)
  session.close()


def process():
  phonesdict = parse_input_file()
  db_insert_or_update_if_needed(phonesdict)


if __name__ == '__main__':
  process()
