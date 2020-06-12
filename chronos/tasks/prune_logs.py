from chronos.metadata import Script as ScriptModel
from chronos.metadata import Session
from chronos.script import Script


def run(arguments, event):
    session = Session()

    for script in session.query(ScriptModel).all():
        script = Script(script.uid)
        script.prune_logs()

    return
