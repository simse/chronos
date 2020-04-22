import json
import os

from chronos.script import Script
from chronos.config import CHRONOS
from chronos.util import generate_uid, for_uid
from chronos.venv import *
import chronos.metadata


def run(arguments, event):
    arguments = json.loads(arguments)
    name = arguments["name"]

    """Create a new script by creating a virtualenv, creating .sh scripts and registering metadata."""
    if name is "":
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

    event.trigger("script_created", Script(uid).dict)

    return uid
