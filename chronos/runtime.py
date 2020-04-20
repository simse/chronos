# Python dependencies
import os
from datetime import datetime
import threading

# Third-party dependencies
import cronex
from loguru import logger

# First-party dependencies
from chronos.util import *
from chronos.venv import *
import chronos.metadata
from chronos.script import Script
from chronos.task import dispatch_task


def create_script(name=None):
    """Create a new script by creating a virtualenv, creating .sh scripts and registering metadata."""
    if name is None:
        # Generate random UID if no name is given
        uid = generate_uid()
    else:
        # Convert name to UID by "sluggifying" it (e.g. "Simon's script" -> "simons-script")
        uid = for_uid(name)

    # Check that the scripts folder exists (important for first-time users)
    if not os.path.isdir(CHRONOS + os.path.sep + "scripts"):
        os.mkdir(CHRONOS + os.path.sep + "scripts")

    # Find script path given UID
    path = CHRONOS + os.path.sep + "scripts" + os.path.sep + uid

    # Create folder, if it doesn't already exist
    if not os.path.isdir(path):
        os.mkdir(path)
    else:
        return uid

    # Create virtual environment
    create_env(uid)

    # Create database entry
    script = chronos.metadata.Script(name=name, uid=uid)
    script.save()

    # Create script and requirements.txt file
    script_path = path + os.path.sep + uid + ".py"
    requirements_path = path + os.path.sep + "requirements.txt"
    open(script_path, "a").close()
    open(requirements_path, "a").close()

    # Create execute script
    # TODO: Move this script to a folder so it can be copied instead
    with open(path + os.path.sep + "execute.sh", "w") as file:
        file.write(
            '''#!/bin/bash
cd "{}"
source "{}"
python "{}"'''.format(
                path, get_activate(uid), script_path
            )
        )

    # Create pip install
    # TODO: Move this script to a folder so it can be copied instead
    with open(path + os.path.sep + "install.sh", "w") as file:
        file.write(
            '''#!/bin/bash
source "{}"
pip install -r "{}"'''.format(
                get_activate(uid), requirements_path
            )
        )

    return uid


def tick(second):
    """This function is called every second, and checks if anything needs to be executed."""
    if second == 1:
        logger.info("Main loop started")
    if second % 60 == 0:
        logger.info("Main loop is still alive, uptime is now: {} seconds", second)

    # Loop through every script metadata
    for script in chronos.metadata.Script.select():
        s = Script(script.uid)

        # Prune logs
        s.prune_logs()

        # Check that the script is enabled to run and that the interval is above 0
        if script.interval != 0 and script.enabled:
            # Check that the interval is a multiple of the current tick
            if second % script.interval == 0:
                # Execute script in seperate thread, such that the loop is not affected
                # x = threading.Thread(target=s.execute)
                # x.start()
                dispatch_task(
                    "execute_script", {"script_uid": script.uid}, task_priority="NOW"
                )

        if script.cron is not None and script.enabled and second % 60 == 0:
            # Evaluate cron expression
            cron = cronex.CronExpression(script.cron)
            time = tuple(list(datetime.now().timetuple())[:5])

            if cron.check_trigger(time):
                # Execute script in seperate thread, such that the loop is not affected
                x = threading.Thread(target=s.execute)
                x.start()
