# Python dependencies
import shutil
from subprocess import Popen, PIPE

# Third-party dependencies
from playhouse.shortcuts import model_to_dict
from loguru import logger

# First-party dependencies
import chronos.metadata
from chronos.config import *
from chronos.venv import *
from chronos.event import event


class Script:
    """Script class used to interact with scripts."""

    def __init__(self, uid):
        """Initialise script class given UID."""

        # UID
        self.uid = uid

        # Get database entry
        self.db = chronos.metadata.Script.get(chronos.metadata.Script.uid == uid)

        # Store dictionary version of model
        self.dict = model_to_dict(self.db)

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

    def delete(self):
        """Delete script."""

        # Remove script folder
        shutil.rmtree(self.folder)

        # Remove all logs from script
        chronos.metadata.Log.delete().where(
            chronos.metadata.Log.script_id == self.db.id
        ).execute()

        # Delete metadata
        self.db.delete_instance()

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

        for l in (
            chronos.metadata.Log.select()
            .where(chronos.metadata.Log.script_id == self.db.id)
            .order_by(chronos.metadata.Log.date.desc())
            .limit(limit)
        ):
            logs.append(
                {
                    "stdout": l.text,
                    "stderr": l.error,
                    "date": l.date,
                    "exitcode": l.exitcode,
                }
            )

        return logs

    def prune_logs(self, limit=500):
        log_count = (
            chronos.metadata.Log.select()
            .where(chronos.metadata.Log.script_id == self.db.id)
            .count()
        )

        if log_count > limit:
            to_delete = log_count - limit

            chronos.metadata.Log.delete().where(
                chronos.metadata.Log.script_id == self.db.id
            ).order_by(chronos.metadata.Log.date.asc()).limit(to_delete).execute()

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
        process = Popen(
            ["bash", self.install_requirements_path],
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            bufsize=-1,
        )

        output, error = process.communicate()

        # Check if it errored or was successful
        process_output = ""
        if process.returncode == 0:
            process_output = output
        else:
            process_output = error

        return process_output.decode("utf-8")

    def execute(self):
        """Execute script"""
        script_path = self.execute_path

        logger.debug("Executing script: {}", self.dict["name"])

        # Run the script
        process = Popen(
            ["bash", script_path], stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=-1
        )

        output, error = process.communicate()

        # Log the output
        log = chronos.metadata.Log(
            script=self.db, text=output, error=error, exitcode=process.returncode
        )
        log.save()

        logger.debug("Script executed and output logged: {}", self.dict["name"])

        event.trigger("script_executed", self.dict)

        # Return stdout and stderr
        return {"stdout": output.decode("utf-8"), "stderr": error.decode("utf-8")}
