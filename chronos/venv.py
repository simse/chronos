import venv
import os
import sys
import subprocess
from chronos.config import *

def get_venv_folder(uid):
    return CHRONOS + os.path.sep + 'scripts' + os.path.sep + uid + os.path.sep + '.venv'

def create_env(uid):
    venv_folder = get_venv_folder(uid)

    if not os.path.isdir(venv_folder):
        v = venv.EnvBuilder(with_pip=True)

        v.create(venv_folder)


def get_activate(uid):
    venv_folder = get_venv_folder(uid)

    return venv_folder + '/bin/activate'


def get_python(uid):
    venv_folder = get_venv_folder(uid)

    python = ''
    if sys.platform == 'win32':
        python = venv_folder + '\\Scripts\\python.exe'
    else:
        python = venv_folder + '/bin/python'.format(os.path.sep)

    return python
