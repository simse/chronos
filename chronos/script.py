# Python dependencies
import shutil
from subprocess import Popen, PIPE

# Third-party dependencies
from loguru import logger

# First-party dependencies
from chronos.metadata import Session, Log
from chronos.metadata import Script as ScriptModel
from chronos.config import *
from chronos.venv import *
from chronos.event import event
from chronos.task import dispatch_task

class Script:
    """Script class used to interact with scripts."""

    def __init__(self, uid):
        """Initialise script class given UID."""

        session = Session()

        # UID
        self.uid = uid

        # Get database entry
        self.db = session.query(ScriptModel).get(uid)

        # Store dictionary version of model
        self.dict = {
            "name": self.db.name,
            "enabled": self.db.enabled,
            "triggers": self.db.triggers
        }

        # Get script folder
        self.folder = CHRONOS + os.path.sep + "scripts" + os.path.sep + self.uid

        # Get path of script
        self.path = self.folder + os.path.sep + self.uid + ".py"

        # Get path of requirements file
        self.requirements = self.folder + os.path.sep + "requirements.txt"

        # Get path of execute.sh script
        self.execute_path = self.folder + os.path.sep + "execute.sh"

        # Get path of install.sh script
        self.install_requirements_path = self.folder + os.path.sep + "install.sh"

        session.close()

    def delete(self):
        """Delete script."""
        session = Session()

        # Remove script folder
        shutil.rmtree(self.folder)

        # Remove all logs from script
        session.query(Log).filter(Log.script == self.uid).delete()

        # Delete metadata
        session.delete(self.db)
        session.commit()
        session.close()

        event.trigger("script_deleted", self.dict)

    def get_contents(self):
        """Read contents of script"""
        return open(self.path, "r").read()

    def get_requirements(self):
        """Read contents of requirements.txt"""
        return open(self.requirements, "r").read()

    def write_contents(self, script):
        """Write new contents to script"""
        return open(self.path, "w").write(script)

    def write_requirements(self, requirements):
        """Write new contents to requirements.txt"""
        return open(self.requirements, "w").write(requirements)

    def logs(self, limit=100):
        """Find all log entries for script"""
        logs = []

        session = Session()

        for log in session.query(Log).filter(Log.script == self.uid).order_by(Log.date.desc()).all():
            try:
                stdout = log.text.decode('utf-8')
            except AttributeError:
                stdout = log.text
            
            try:
                stderr = log.error.decode('utf-8')
            except AttributeError:
                stderr = log.error

            logs.append(
                {
                    "stdout": stdout,
                    "stderr": stderr,
                    "date": log.date,
                    "exitcode": log.exitcode,
                }
            )

        session.close()

        return logs

    def prune_logs(self, limit=500):
        return

        """log_count = (
            chronos.metadata.Log.select()
            .where(chronos.metadata.Log.script_id == self.db.id)
            .count()
        )

        if log_count > limit:
            to_delete = log_count - limit

            chronos.metadata.Log.delete().where(
                chronos.metadata.Log.script_id == self.db.id
            ).order_by(chronos.metadata.Log.date.asc()).limit(to_delete).execute()"""

    def to_dict(self):
        """Return dictionary with script metadata"""
        return {
            **{
                "uid": self.uid,
                "contents": self.get_contents(),
                "requirements": self.get_requirements(),
                "logs": self.logs(),
            },
            **self.dict,
        }

    def install_requirements(self):
        """Install requirements.txt"""
        dispatch_task("install_pip_requirements", {
            "script_uid": self.uid
        }, task_priority="NOW")

    def execute(self):
        session = Session()
        """Execute script"""
        script_path = self.execute_path

        logger.debug("Executing script: {}", self.dict["name"])

        # Run the script
        process = Popen(
            ["bash", script_path], stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=-1
        )

        while True:
            output = process.stdout.readline()

            if output == '' and process.poll() is not None:
                break
            if output:
                print (output.strip())

            rc = process.poll()

        output, error = process.communicate()

        # Log the output
        log = Log(
            script=self.db.uid, text=output, error=error, exitcode=process.returncode
        )
        session.add(log)
        session.commit()
        session.close()

        logger.debug("Script executed and output logged: {}", self.dict["name"])

        event.trigger("script_executed", self.dict)

        # Return stdout and stderr
        return {"stdout": output.decode("utf-8"), "stderr": error.decode("utf-8")}
