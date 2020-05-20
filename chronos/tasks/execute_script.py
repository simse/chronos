import json
from subprocess import PIPE, Popen

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

    while True:
        output = process.stdout.readline()
        if process.poll() is not None:
            break

        if output:
            event.trigger(
                "task_output",
                {
                    "task_id": task_id,
                    "script_uid": script_uid,
                    "output": output.decode("utf-8").strip(),
                    "task": "execute",
                },
            )

    exitcode = process.poll()

    stdout, stderr = process.communicate()

    if stderr:
        print(stderr)
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
    log = Log(script=script_uid, text=stdout, error=stderr, exitcode=exitcode)
    session.add(log)
    session.commit()
    session.close()

    event.trigger(
        "task_output",
        {"task_id": task_id, "output": "", "script_uid": script.uid, "task": "execute"},
    )
    event.trigger("script_executed", script.to_dict())
    event.trigger("script_updated", script.to_dict())
    event.trigger("action_complete", {"action": "execute", "uid": script.uid})

    return stdout
