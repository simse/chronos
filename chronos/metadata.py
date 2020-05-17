# Python dependencies
from pathlib import Path
import datetime
import os
import logging
import json
import sqlite3

# Third-party dependencies
from sqlalchemy import create_engine, MetaData, Column, Integer, String, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
import alembic.config
from loguru import logger

# First-party dependencies
from chronos.config import CHRONOS


# Detect if old database type is still there
conn = None
scripts = None
logs = None
try:
    conn = sqlite3.connect(CHRONOS + "/chronos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='setting'")
    rows = cursor.fetchall()

    if len(rows) == 1:
        logger.debug("Detected old database, converting to new format...")

        cursor.execute("SELECT * FROM script")
        scripts = cursor.fetchall()

        cursor.execute("SELECT * FROM log")
        logs = cursor.fetchall()

        logger.debug("Conversion step 1 finished: gathered data")

        logger.debug("Backing up database and removing...")
        database_path = Path(CHRONOS + "/chronos.db")
        database_path.rename(CHRONOS + "/" + str(int(datetime.datetime.utcnow().timestamp() * 1000)) + "-old-chronos.db")
        logger.debug("Database backed up, creating new format...")

except Error as e:
    print(e)
finally:
    if conn:
        conn.close()


logger.debug("Connecting to local Chronos database")
db = create_engine("sqlite:///" + CHRONOS + "/chronos.db", echo=False)
meta = MetaData()
Session = scoped_session(sessionmaker(bind=db))
Base = declarative_base(metadata=meta)
logger.debug("Database connection succesful")


class Script(Base):
    """Script model to store metadata about scripts."""
    __tablename__ = 'scripts'

    name = Column(String)
    uid = Column(String, primary_key=True)
    enabled = Column(Boolean)
    triggers = Column(JSON)
    created = Column(DateTime, default=datetime.datetime.utcnow)
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



def migrate():
    logger.info("Running database migrations...")
    alembicArgs = [
        "upgrade",
        "head",
    ]
    alembic.config.main(argv=alembicArgs)
    logger.info("Database migrations succesful")


if scripts is not None:
    session = Session()
    logger.debug("Running conversion step 2: inserting data into new database...")

    script_lookup = {}

    for script in scripts:
        script_id = script[0]
        script_name = script[1]
        script_uid = script[2]
        script_enabled = script[4]
        script_triggers = []

        if script[6] != 0 and script[3] != 0:
            script_triggers.append({
                'type': 'interval',
                'options': {
                    'interval': script[3]
                } 
            })


        if script[5] != None and script[7] != 0:
            script_triggers.append({
                'type': 'cron',
                'options': {
                    'expression': script[5]
                } 
            })

        script_lookup[script_id] = script_uid

        session.add(Script(
            name=script_name,
            uid=script_uid,
            enabled=(script_enabled == 1),
            triggers=script_triggers
        ))

    if logs is not None:

        # logger.debug(len(logs))

        for log in logs:
            try:
                script_uid = script_lookup[log[1]]
                text = log[2]
                date = log[3]
                exitcode = log[4]
                error = log[5]

                session.add(Log(
                    script=script_uid,
                    text=text,
                    exitcode=exitcode,
                    error=error,
                    date=datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
                ))

            except(KeyError):
                continue

    session.commit()
    session.close()
    logger.debug("Database format conversion complete.")
