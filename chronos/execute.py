import os
import subprocess

from chronos.config import *
from chronos.venv import *

def execute(uid):
    # Check if script exists (technically it's the metadata that's checked)
    if os.path.isfile(SCRIPTS_FOLDER + os.path.sep + uid + os.path.sep + uid + '.py'):
        activate(uid)

        python_executeable = get_python(uid)

        process = subprocess.check_output([python_executeable, SCRIPTS_FOLDER + os.path.sep + uid + os.path.sep + uid + '.py'], universal_newlines=True)
        return process

    else:
        return False
