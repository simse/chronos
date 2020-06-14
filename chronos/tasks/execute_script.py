import json
from datetime import datetime
from subprocess import PIPE, Popen

import maya

from chronos.script import Script
from chronos.metadata import Log, Session


def run(arguments, event):
    arguments = json.loads(arguments)
    script_uid = arguments["script_uid"]
    task_id = arguments["task_id"]

    event.trigger("action_started", {"uid": script_uid, "action": "execute"})

    script = Script(script_uid)

    process = Popen(
        ["bash", script.execute_path], stdout=PIPE, stderr=PIPE, shell=False
    )

    exitcode = 0
    process_output = ""

    while True:
        output = process.stdout.readline()
        process_output += output.decode("utf-8")
        if process.poll() is not None:
            break

        if output:
            event.trigger(
                "task_output",
                {
                    "task_id": task_id,
                    "script_uid": script_uid,
                    "output": output.decode("utf-8"),
                    "task": "execute",
                },
            )

    exitcode = process.poll()

    stdout, stderr = process.communicate()

    if stderr:
        event.trigger(
            "task_output",
            {
                "task_id": task_id,
                "script_uid": script_uid,
                "output": stderr.decode("utf-8"),
                "task": "execute",
            },
        )

    session = Session()
    log = Log(script=script_uid, text=process_output, error=stderr, exitcode=exitcode)
    session.add(log)
    session.commit()
    session.close()

    event.trigger(
        "task_output",
        {"task_id": task_id, "output": "", "script_uid": script.uid, "task": "execute"},
    )
    script = script.to_dict()

    # Decode bytes to string
    try:
        stderr = stderr.decode("utf-8")
    except AttributeError:
        pass

    try:
       process_output =process_output.decode("utf-8")
    except AttributeError:
        pass

    script["logs"].insert(
        0,
        {
            "date": maya.now().rfc2822(),
            "stderr": stderr,
            "stdout": process_output,
            "exitcode": exitcode,
        },
    )
    event.trigger("script_executed", script)

    event.trigger("script_updated", script)
    event.trigger("action_complete", {"action": "execute", "uid": script["uid"]})

    return stdout
