# Python dependencies
import datetime
import os

# Third-party dependencies
from peewee import *

# First-party dependencies
from chronos.config import CHRONOS

#print("Connecting to database at: {}".format(CHRONOS + os.path.sep + 'chronos.db'))
"""
Connect to SQLite database. Uses CHRONOS environment variable to find location.
"""
db = SqliteDatabase(CHRONOS + os.path.sep + 'chronos.db')


class Script(Model):
    """Script model to store metadata about scripts."""
    name = CharField()
    uid = CharField()
    interval = IntegerField(default=0)
    enabled = BooleanField(default=True)

    class Meta:
        database = db


class Log(Model):
    """Log model to store output from each script execution."""
    script = ForeignKeyField(Script, backref='logs')
    text = TextField()
    date = DateTimeField(default=datetime.datetime.utcnow)
    exitcode = IntegerField(default=0)

    class Meta:
        database = db


class Setting(Model):
    """Key/value storage for settings, and other persistent information."""
    key = CharField()
    value = TextField()

    class Meta:
        database = db


# Opens database connection
db.connect()

# Makes sure tables exist (ie. creates new table if a new table has been defined since last execution)
db.create_tables([Script, Log, Setting])
