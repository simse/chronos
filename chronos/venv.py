# Python depedencies
import venv
import os

# Third-party depedencies


# First-party depedencies
from chronos.config import *


def get_venv_folder(uid):
    """Returns location of virtualenv folder given script UID"""
    return CHRONOS + os.path.sep + "scripts" + os.path.sep + uid + os.path.sep + ".venv"


def create_env(uid):
    """Asks venv module to generate a virtualenv"""
    venv_folder = get_venv_folder(uid)

    # Make sure path does not already exist
    if not os.path.isdir(venv_folder):
        v = venv.EnvBuilder(with_pip=True)
        v.create(venv_folder)


def get_activate(uid):
    """Returns location of virtualenv activate script given UID"""
    return get_venv_folder(uid) + "/bin/activate"


def get_python(uid):
    """Returns location of virtualenv python binary given UID"""
    return get_venv_folder(uid) + "/bin/python"
