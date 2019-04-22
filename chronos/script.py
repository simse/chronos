# Python dependencies
import shutil
from subprocess import Popen, PIPE

# First-party dependencies
import chronos.metadata
from chronos.config import *
from chronos.venv import *

class Script():
    """Script class used to interact with scripts."""

    def __init__(self, uid):
        """Initialise script class given UID."""

        # UID
        self.uid = uid

        # Get database entry
        self.db = chronos.metadata.Script.get(chronos.metadata.Script.uid == uid)

        # Get script folder
        self.folder = CHRONOS + os.path.sep + 'scripts' + os.path.sep + self.uid

        # Get path of script
        self.path = self.folder + os.path.sep + self.uid + '.py'

        # Get path of requirements file
        self.requirements = self.folder + os.path.sep + 'requirements.txt'

        # Get path of execute.sh script
        self.execute_path = self.folder + os.path.sep + 'execute.sh'

        # Get path of install.sh script
        self.install_requirements_path = self.folder + os.path.sep + 'install.sh'


    def delete(self):
        """Delete script."""

        # Remove script folder
        shutil.rmtree(self.folder)

        # Remove all logs from script
        chronos.metadata.Log.delete().where(chronos.metadata.Log.script_id == self.db.id).execute()

        # Delete metadata
        self.db.delete_instance()

    def get_contents(self):
        """Read contents of script"""
        return open(self.path, 'r').read()

    def get_requirements(self):
        """Read contents of requirements.txt"""
        return open(self.requirements, 'r').read()

    def write_contents(self, script):
        """Write new contents to script"""
        return open(self.path, 'w').write(script)

    def write_requirements(self, requirements):
        """Write new contents to requirements.txt"""
        return open(self.requirements, 'w').write(requirements)

    def logs(self, limit=100):
        """Find all log entries for script"""
        logs = []

        for l in chronos.metadata.Log.select().where(chronos.metadata.Log.script_id == self.db.id).order_by(chronos.metadata.Log.date.desc()).limit(limit):
            logs.append({
                'text': l.text,
                'date': l.date,
                'exitcode': l.exitcode
            })

        return logs

    def to_dict(self):
        """Return dictionary with script metadata"""
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
        """Install requirements.txt"""
        process = subprocess.check_output(['bash', self.install_requirements_path], universal_newlines=True)

        return process

    def execute(self):
        """Execute script"""
        script_path = self.execute_path

        # Run the script
        process = Popen(['bash', script_path], stdin=PIPE, stdout=PIPE, stderr=PIPE,
        bufsize=-1)

        output, error = process.communicate()

        # Check if it errored or was successful
        process_output = ''
        if process.returncode == 0:
            process_output = output
        else:
            process_output = error

        # Log the output
        log = chronos.metadata.Log(script=self.db, text=process_output, exitcode=process.returncode)
        log.save()

        # Return text output
        return process_output
