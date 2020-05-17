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
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE,
        bufsize=-1,
    )

    process_output = ""
    exitcode = 0

    while True:
        output = process.stdout.readline().decode('utf-8')

        if process.poll() is not None:
            exitcode = process.poll()

            break

        if output:
            process_output += output
            event.trigger("log_output", {
                "task_id": task_id,
                "script_uid": script_uid,
                "output": output
            })




    session = Session()
    log = Log(
        script=script_uid, text=process_output, error="", exitcode=exitcode
    )
    session.add(log)
    session.commit()
    session.close()

    return process_output
