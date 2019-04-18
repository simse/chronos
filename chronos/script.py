import shutil

from chronos.config import *
from chronos.venv import *
import chronos.metadata

class Script():

    def __init__(self, uid):
        self.uid = uid
        self.db = chronos.metadata.Script.get(chronos.metadata.Script.uid == uid)
        self.folder = CHRONOS + os.path.sep + 'scripts' + os.path.sep + self.uid
        self.path = self.folder + os.path.sep + self.uid + '.py'
        self.execute_path = self.folder + os.path.sep + 'execute.sh'
        self.install_requirements_path = self.folder + os.path.sep + 'install.sh'
        self.requirements = self.folder + os.path.sep + 'requirements.txt'

    def delete(self):
        shutil.rmtree(self.folder)
        chronos.metadata.Log.delete().where(script_id == self.db.id).execute()
        self.db.delete_instance()

    def get_contents(self):
        return open(self.path, 'r').read()

    def get_requirements(self):
        return open(self.requirements, 'r').read()

    def write_contents(self, script):
        return open(self.path, 'w').write(script)

    def logs(self):
        logs = []

        for l in chronos.metadata.Log.select().where(chronos.metadata.Log.script_id == self.db.id).order_by(chronos.metadata.Log.date.desc()).limit(100):
            logs.append({
                'text': l.text,
                'date': l.date,
                'exitcode': l.exitcode
            })

        return logs

    def to_dict(self):
        return {
            'uid': self.uid,
            'name': self.db.name,
            'interval': self.db.interval,
            'enabled': self.db.enabled,
            'contents': self.get_contents(),
            'requirements': self.get_requirements(),
            'logs': self.logs()
        }

    def install_requirements(self):
        process = subprocess.check_output(['bash', self.install_requirements_path], universal_newlines=True)

        return process

    def execute(self):
        script_path = self.execute_path

        process = Popen(['bash', script_path], stdin=PIPE, stdout=PIPE, stderr=PIPE,
        bufsize=-1)

        output, error = p.communicate()


        # Log the output
        log = chronos.metadata.Log(script=self.db, text=process, exitcode=exitcode)
        log.save()

        return process
