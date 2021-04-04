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

  def __init__(self, name, uf, partido, phone):
    self.name = name
    self.uf = uf
    self.partido = partido
    self.phone = phone

  @staticmethod
  def get_name_partido_dash_separated(line):
    pp = line.split('-')
    name = pp[0]
    name = name.lstrip(' ').rstrip(' ')
    partido = 's/n'
    if len(pp) > 1:
      partido = pp[1]
      partido = partido.lstrip(' ').rstrip(' ')
    return name, partido

  def __str__(self):
    outstr = '[{phone}] [{name}] [{uf}] [{partido}]'\
      .format(name=self.name, uf=self.uf, partido=self.partido, phone=self.phone)
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
      phone = line[:13]
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
    print('repeated', repeat, phonesdict[repeat.phone])
  return phonesdict


def insert_into_db(phonesdict):
  session = Session()
  for i, phone in enumerate(phonesdict):
    seq = i + 1
    dw = phonesdict[phone]
    existent = session.query(SADeput) \
        .filter(
          SADeput.name == dw.name, SADeput.uf == dw.uf, SADeput.partido == dw.partido, SADeput.phone == dw.phone
        ) \
        .first()
    if existent:
      print(seq, 'exists', str(dw))
      continue
    sadeput = SADeput()
    sadeput.name = dw.name
    sadeput.uf = dw.uf
    sadeput.partido = dw.partido
    sadeput.phone = dw.phone
    session.add(sadeput)
    session.commit()
    print(seq, 'inserted', str(dw))
  session.close()


def process():
  phonesdict = parse_input_file()
  insert_into_db(phonesdict)


if __name__ == '__main__':
  process()
