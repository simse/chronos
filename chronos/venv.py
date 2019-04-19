import venv
import os
from chronos.config import *

def get_venv_folder(uid):
    return CHRONOS + os.path.sep + 'scripts' + os.path.sep + uid + os.path.sep + '.venv'

def create_env(uid):
    venv_folder = get_venv_folder(uid)

    if not os.path.isdir(venv_folder):
        v = venv.EnvBuilder(with_pip=True)

        v.create(venv_folder)


def get_activate(uid):
    return get_venv_folder(uid) + '/bin/activate'


def get_python(uid):
    return get_venv_folder(uid) + '/bin/python'
