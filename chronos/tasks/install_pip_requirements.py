import json
from subprocess import Popen, PIPE

from chronos.script import Script


def run(arguments, event):
    arguments = json.loads(arguments)
    script_uid = arguments["script_uid"]
    task_id = arguments["task_id"]

    script = Script(script_uid)

    process = Popen(
        ["bash", script.install_requirements_path],
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
            event.trigger("task_output", {
                "task_id": task_id,
                "output": output
            })

    output, error = process.communicate()

    return process_output
