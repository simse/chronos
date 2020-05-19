import shutil
import json
import os

from chronos.script import Script
from chronos.metadata import Session, Log


def run(arguments, event):
    arguments = json.loads(arguments)
    uid = arguments["uid"]

    script = Script(uid)

    session = Session()

    # Remove script folder
    shutil.rmtree(script.folder)

    # Remove all logs from script
    session.query(Log).filter(Log.script == script.uid).delete()

    # Delete metadata
    session.delete(script.db)
    session.commit()
    session.close()

    event.trigger("script_deleted", script.to_dict())
    event.trigger("action_complete", {
        "action": "delete",
        "uid": script.uid
    })

    return uid
