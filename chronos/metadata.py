# Python dependencies
from pathlib import Path
import datetime
import os
import logging
import json

# Third-party dependencies
from sqlalchemy import create_engine, MetaData, session, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
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
    logs = relationship("Log")


class Log(Model):
    """Log model to store output from each script execution."""
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    script = Column(Integer, ForeignKey("scripts.id"))
    text = Column(String)
    error = Column(String)
    date = Column(DateTime)
    exitcode = Column(Integer)


class Setting(Model):
    """Key/value storage for settings, and other persistent information."""
    __tablename__ = 'settings'

    key = Column(String, primary_key=True)
    value = Column(String)


class Task(Model):
    __tablename__ = 'tasks'

    task_id = Column(String, primary_key=True)
    task_arguments = Column(String)
    priority = Column(String)
    status = Column(String)
    output = Column(String)
    time_scheduled = Column(DateTime)
    time_started = Column(DateTime)
    time_finished = Column(DateTime)



logger.debug("Running database migrations")
# db.evolve(interactive=False)
logger.debug("Database migration complete")
