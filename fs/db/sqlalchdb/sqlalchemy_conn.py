#!/usr/bin/python3
'''
In other to make mysql work with sqlalchemy, two things were done:
  1) Ubuntu's package python3-dev and libmysqlclient-dev were installed;
  2) after that, mysqlclient was installed via pip.

Because in this machine, a virtualenv is taken by the IDE (PyCharm),
 mysqlclient was installed both globally (so that app could be run without activating
 virtualenv and then also installed locally. so that PyCharm could also run app).

SqlAlchemy

=> to learn how to use Foreign Keys in SqlAlchemy
  => docs.sqlalchemy.org/en/13/orm/join_conditions.html?highlight=foreign key

'''
from sqlalchemy import create_engine
import config

this_db = config.THIS_DATABASE;
user         = config.DATABASE_DICT[this_db]['USER']
password     = config.DATABASE_DICT[this_db]['PASSWORD']
address      = config.DATABASE_DICT[this_db]['ADDRESS']
port         = config.DATABASE_DICT[this_db]['PORT']
databasename = config.DATABASE_DICT[this_db]['DATABASENAME']

engine_line = this_db + '://' + user + ':' + password + '@' + address + '/' + databasename

if engine_line.startswith('mysql'):
  engine_line = engine_line + '?charset=utf8mb4'

sqlalchemy_engine = create_engine(engine_line)
# print (engine_line)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=sqlalchemy_engine)