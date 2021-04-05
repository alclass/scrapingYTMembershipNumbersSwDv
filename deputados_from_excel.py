#!/usr/bin/env python3
"""
deputados_whatsapp
"""
import os
import xlrd
from config import get_local_dados_foldername
from models.sa_models.ytchannelsubscribers_samodels import DeputadoWhatsappSA as SADeput
from fs.db.sqlalchdb.sqlalchemy_conn import Session


filename = 'deputados-from-camara_2021-04-04.xls'


class DeputadoExcel:

  def __init__(self, nomeparlamentar, partido, uf, titular_outro, anexopredio, ngabinete, fixphone, email, nomecivil):
    """
      Colum map
      'Nome Parlamentar'
      'Partido'
      'UF'
      'Titular/Suplente/Efetivado'
      'Anexo'
      'Gabinete'
      'Telefone'
      'Mês Aniversário'
      'Dia Aniversário'
      'Correio Eletrônico'
      'Nome Civil'
    """
    self.nomeparlamentar = nomeparlamentar
    self.partido = partido
    self.uf = uf
    self.titular_outro = titular_outro
    self.anexopredio = int(anexopredio)
    self.ngabinete = int(ngabinete)
    self.fixphone = fixphone
    self.email_to_reduce = email
    # @property self.email = None
    self.emlmidstr = None
    self.nomecivil = nomecivil
    self.reduce_email_to_emlmidstr()

  def reduce_email_to_emlmidstr(self):
    emlmidstr = self.email_to_reduce.lstrip('dep.')
    emlmidstr = emlmidstr.rstrip('@camara.leg.br')
    self.emlmidstr = emlmidstr

  @property
  def email(self):
    if self.emlmidstr.startswith('dep.') and self.emlmidstr.endswith('@camara.leg.br'):
      return self.emlmidstr
    return '{dep}{emlmidstr}{afteratsign}'.format(dep='dep.', emlmidstr=self.emlmidstr, afteratsign='@camara.leg.br')

  def __str__(self):
    outstr = """
    nomeparlamentar = {nomeparlamentar}
    nomecivil = {nomecivil}
    uf = {uf}
    partido = {partido}
    fixphone = {fixphone}
    titular_outro = {titular_outro}
    ngabinete = {ngabinete}
    anexopredio = {anexopredio}
    email = {email}
    """.format(
      nomeparlamentar=self.nomeparlamentar,
      partido=self.partido,
      uf=self.uf,
      titular_outro=self.titular_outro,
      anexopredio=self.anexopredio,
      ngabinete=self.ngabinete,
      fixphone=self.fixphone,
      email=self.email,
      nomecivil=self.nomecivil
    )
    return outstr


def parse_input_file():
  """
  Colum map
  'Nome Parlamentar'
  'Partido'
  'UF'
  'Titular/Suplente/Efetivado'
  'Anexo'
  'Gabinete'
  'Telefone'
  'Mês Aniversário'
  'Dia Aniversário'
  'Correio Eletrônico'
  'Nome Civil'
  :return:
  """
  filepath = os.path.join(get_local_dados_foldername(), filename)
  wb = xlrd.open_workbook_xls(filename=filepath)
  # first_sheet_name = wb[0]
  sh = wb.sheet_by_index(0)
  print("{0} {1} {2}".format(sh.name, sh.nrows, sh.ncols))
  print("Cell D30 is {0}".format(sh.cell_value(rowx=29, colx=3)))
  deputados = []
  for i in range(1, sh.nrows):
    row = None
    try:
      row = sh.row(i)
      nomeparlamentar = row[0].value
      partido = row[1].value
      uf = row[2].value
      titular_outro = row[3].value
      anexopredio = row[4].value
      ngabinete = int(row[5].value)
      fixphone = row[6].value
      fixphone = fixphone.replace('-', '')
      email = row[9].value
      nomecivil = row[10].value
      deput_excel = DeputadoExcel(
        nomeparlamentar, partido, uf, titular_outro, anexopredio, ngabinete, fixphone, email, nomecivil
      )
      # print(deput_excel)
      deputados.append(deput_excel)
    except ValueError as e:
      print(row)
      raise ValueError(e)
  return deputados


def insert_into_db(phonesdict):
  session = Session()
  for i, phone in enumerate(phonesdict):
    seq = i + 1
    dw = phonesdict[phone]
    existent = session.query(SADeput) \
        .filter(
          SADeput.name == dw.name, SADeput.uf == dw.uf, SADeput.partido == dw.partido, SADeput.phone == dw.cellphone
        ) \
        .first()
    if existent:
      print(seq, 'exists', str(dw))
      continue
    sadeput = SADeput()
    sadeput.name = dw.name
    sadeput.uf = dw.uf
    sadeput.partido = dw.partido
    sadeput.phone = dw.cellphone
    session.add(sadeput)
    session.commit()
    print(seq, 'inserted', str(dw))
  session.close()


def db_insert_or_update_if_needed(deputados):
  session = Session()
  n_inserts = 0
  n_inserts_or_updates = 0
  for i, deput_excel in enumerate(deputados):
    seq = i + 1
    nomeparlamentar = deput_excel.nomeparlamentar
    uf = deput_excel.uf
    partido = deput_excel.partido
    do_commit = False
    deput_sa = session.query(SADeput) \
        .filter(
          SADeput.nomeparlamentar == nomeparlamentar, SADeput.uf == uf, SADeput.partido == partido
        ) \
        .first()
    if deput_sa:
      print(seq, 'exists deput_sa (updating if needed)', deput_sa)
    else:
      deput_sa = SADeput()
      do_commit = True
      print(seq, 'does not exist deput_sa (inserting)', deput_sa)
      deput_sa.name = deput_excel.nomeparlamentar
      deput_sa.uf = deput_excel.uf
      deput_sa.partido = deput_excel.partido
      n_inserts += 1
      session.add(deput_sa)
    if deput_sa.nomeparlamentar != deput_excel.nomeparlamentar:
      deput_sa.nomeparlamentar = deput_excel.nomeparlamentar
      do_commit = True
    if deput_sa.nomecivil != deput_excel.nomecivil:
      deput_sa.nomecivil = deput_excel.nomecivil
      do_commit = True
    if deput_sa.fixphone != deput_excel.fixphone:
      deput_sa.fixphone = deput_excel.fixphone
      do_commit = True
    if deput_sa.titular_outro != deput_excel.titular_outro:
      deput_sa.titular_outro = deput_excel.titular_outro
      do_commit = True
    if deput_sa.ngabinete != deput_excel.ngabinete:
      deput_sa.ngabinete = deput_excel.ngabinete
      do_commit = True
    if deput_sa.anexopredio != deput_excel.anexopredio:
      deput_sa.anexopredio = deput_excel.anexopredio
      do_commit = True
    if deput_sa.emlmidstr != deput_excel.emlmidstr:
      deput_sa.emlmidstr = deput_excel.emlmidstr
      do_commit = True
    if do_commit:
      n_inserts_or_updates += 1
      print('updating', deput_sa.nomeparlamentar)
      session.commit()
  print('n_inserts_or_updates', n_inserts_or_updates, 'n_inserts', n_inserts)
  session.close()


def process():
  deputados = parse_input_file()
  db_insert_or_update_if_needed(deputados)


if __name__ == '__main__':
  process()
