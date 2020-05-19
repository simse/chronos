import json
from subprocess import PIPE, Popen

from chronos.script import Script
from chronos.metadata import Log, Session


def run(arguments, event):
    arguments = json.loads(arguments)
    script_uid = arguments["script_uid"]
    task_id = arguments["task_id"]

    script = Script(script_uid)

    process = Popen(
        ["bash", script.execute_path],
        stdout=PIPE,
        shell=False
    )

    process_output = ""
    exitcode = 0

    while True:
        output = process.stdout.readline()
        if process.poll() is not None:
            break

        if output:
            event.trigger("task_output", {
                "task_id": task_id,
                "script_uid": script_uid,
                "output": output.decode("utf-8").strip(),
                "task": "execute"
            })

    """
    while True:
        output = process.stdout.readline().decode('utf-8')

        if not output:
            break

        if output:
            process_output += output
            event.trigger("log_output", {
                "task_id": task_id,
                "script_uid": script_uid,
                "output": output
            })

            print(output)"""

    exitcode = process.poll()


    session = Session()
    log = Log(
        script=script_uid, text=process_output, error="", exitcode=exitcode
    )
    session.add(log)
    session.commit()
    session.close()

    event.trigger("task_output", {
        "task_id": task_id,
        "output": "",
        "script_uid": script.uid,
        "task": "execute"
    })
    event.trigger("script_executed", script.to_dict())
    event.trigger("action_complete", {
        "action": "execute",
        "uid": script.uid
    })

    return process_output
