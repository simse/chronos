# Python dependencies
from pathlib import Path
import datetime
import os
import logging
import json

# Third-party dependencies
from peewee import *
from playhouse.postgres_ext import *
import peeweedbevolve
from loguru import logger

# First-party dependencies
from chronos.config import CHRONOS


logger.debug("Connecting to local Chronos database")
db = PostgresqlDatabase('chronos', user='chronos', host='192.168.0.4', password='hotfla123As', port=5434)
logger.debug("Database connection succesful")

class Script(Model):
    """Script model to store metadata about scripts."""

    name = CharField()
    uid = CharField()
    enabled = BooleanField(default=True)
    triggers = JSONField(default={})

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


class Migration(Model):
    name = CharField()
    status = CharField()

    class Meta:
        database = db


logger.debug("Running database migrations")
db.evolve(interactive=False)
logger.debug("Database migration complete")
