# Python dependencies
from pathlib import Path
import datetime
import os
import logging
import json

# Third-party dependencies
from sqlalchemy import create_engine, MetaData, session, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from loguru import logger

# First-party dependencies
from chronos.config import CHRONOS


logger.debug("Connecting to local Chronos database")
db = create_engine("sqlite:///" + CHRONOS + "/chronos.db", echo=False)
metadata = MetaData()
Base = declarative_base()
logger.debug("Database connection succesful")


class Script(Base):
    """Script model to store metadata about scripts."""
    __tablename__ = 'scripts'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    uid = Column(String)
    enabled = Column(Boolean)
    triggers = Column(String)


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
