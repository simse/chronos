import datetime
import os

from peewee import *

from chronos.config import CHRONOS

print("Connecting to database at: {}".format(CHRONOS + os.path.sep + 'chronos.db'))
db = SqliteDatabase(CHRONOS + os.path.sep + 'chronos.db')

class Script(Model):
    name = CharField()
    uid = CharField()
    interval = IntegerField(default=0)
    enabled = BooleanField(default=True)

    class Meta:
        database = db

class Log(Model):
    script = ForeignKeyField(Script, backref='logs')
    text = TextField()
    date = DateTimeField(default=datetime.datetime.utcnow)
    exitcode = IntegerField(default=0)

    class Meta:
        database = db


db.connect()
db.create_tables([Script, Log])
