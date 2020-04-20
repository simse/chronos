# Python dependencies
from pathlib import Path
import datetime
import os
import logging

# Third-party dependencies
from peewee import *
from peewee_migrate import Router
from loguru import logger

# First-party dependencies
from chronos.config import CHRONOS

# print("Connecting to database at: {}".format(CHRONOS + os.path.sep + 'chronos.db'))
"""
Connect to SQLite database. Uses CHRONOS environment variable to find location.
"""
database_url = CHRONOS + os.path.sep + "chronos.db"
logger.debug("Connecting to database at: {}", database_url)
db = SqliteDatabase(database_url)
logger.debug("Database connection succesful")


class Script(Model):
    """Script model to store metadata about scripts."""

    name = CharField()
    uid = CharField()
    interval = IntegerField(default=0)
    cron = CharField()
    interval_enabled = BooleanField(default=True)
    cron_enabled = BooleanField(default=True)
    enabled = BooleanField(default=True)

    class Meta:
        database = db


class Log(Model):
    """Log model to store output from each script execution."""

    script = ForeignKeyField(Script, backref="logs")
    text = TextField()
    error = TextField()
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


class Task(Model):
    task_id = CharField()
    task_arguments = TextField(default="{}")
    priority = CharField(default="ROUTINE")
    status = CharField(default="WAITING")
    output = TextField(null=True)
    time_scheduled = DateTimeField(default=datetime.datetime.utcnow)
    time_started = DateTimeField(null=True)
    time_finished = DateTimeField(null=True)

    class Meta:
        database = db


logger.debug("Running database migrations")
logging.getLogger("peewee_migrate").setLevel(
    logging.CRITICAL
)  # Surpress output from peewee_migrate
router = Router(db)
router.run()
logger.debug("Database migration complete")
