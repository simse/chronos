# Python dependencies
from pathlib import Path
import datetime
import os
import logging
import json

# Third-party dependencies
from sqlalchemy import create_engine, MetaData, Column, Integer, String, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from loguru import logger

# First-party dependencies
from chronos.config import CHRONOS


logger.debug("Connecting to local Chronos database")
db = create_engine("sqlite:///" + CHRONOS + "/chronos.db", echo=False)
Session = scoped_session(sessionmaker(bind=db))
Base = declarative_base()
logger.debug("Database connection succesful")


class Script(Base):
    """Script model to store metadata about scripts."""
    __tablename__ = 'scripts'

    name = Column(String)
    uid = Column(String, primary_key=True)
    enabled = Column(Boolean)
    triggers = Column(JSON)
    logs = relationship("Log")


class Log(Base):
    """Log model to store output from each script execution."""
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    script = Column(Integer, ForeignKey("scripts.uid"))
    text = Column(String)
    error = Column(String)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    exitcode = Column(Integer)


class Setting(Base):
    """Key/value storage for settings, and other persistent information."""
    __tablename__ = 'settings'

    key = Column(String, primary_key=True)
    value = Column(String)


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    task_id = Column(String)
    task_arguments = Column(String)
    priority = Column(String)
    status = Column(String)
    output = Column(String)
    time_scheduled = Column(DateTime, default=datetime.datetime.utcnow)
    time_started = Column(DateTime)
    time_finished = Column(DateTime)



Base.metadata.create_all(db)

logger.debug("Running database migrations")
# db.evolve(interactive=False)
logger.debug("Database migration complete")
