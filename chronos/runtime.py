import os
import threading

from chronos.util import *
from chronos.venv import *
import chronos.metadata
from chronos.script import Script

def create_script(name=None):
    if name is None:
        uid = generate_uid()
    else:
        uid = for_uid(name)

    if not os.path.isdir(CHRONOS + os.path.sep + 'scripts'):
        os.mkdir(CHRONOS + os.path.sep + 'scripts')

    path = CHRONOS + os.path.sep + 'scripts' + os.path.sep + uid

    # Create folder
    if not os.path.isdir(path):
        os.mkdir(path)
    else:
        return uid

    # Create virtual environment
    create_env(uid)

    script = chronos.metadata.Script(name=name, uid=uid)
    script.save()

    # Create script and requirements.txt file
    script_path = path + os.path.sep + uid + '.py'
    requirements_path = path + os.path.sep + 'requirements.txt'
    open(script_path, 'a').close()
    open(requirements_path, 'a').close()

    # Create execute script
    with open(path + os.path.sep + 'execute.sh', 'w') as file:
        file.write('''
#!/bin/bash
source "{}"
python "{}"
        '''.format(get_activate(uid), script_path))

    # Create pip install
    with open(path + os.path.sep + 'install.sh', 'w') as file:
        file.write('''
#!/bin/bash
source "{}"
pip install -r "{}"
        '''.format(get_activate(uid), requirements_path))


    return uid

def tick(second):
    print('Tick: {}'.format(second))

    # Loop through every script metadata
    for script in chronos.metadata.Script.select():
        if script.interval != 0 and script.enabled:
            if second % script.interval == 0:
                s = Script(script.uid)
                x = threading.Thread(target=s.execute)
                x.start()
