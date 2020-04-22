import json
import importlib
import datetime
import threading

from loguru import logger

from chronos.metadata import Task
from chronos.event import event


def dispatch_task(task_id, task_arguments, task_priority="ROUTINE"):
    task = Task(
        task_id=task_id,
        task_arguments=json.dumps(task_arguments),
        priority=task_priority,
    )

    task.save()
    logger.debug("Dispatched task: {}", task_id)

    return True


def execute_task(task):
    logger.debug("Processing task with ID: {}", task.id)
    task_uid = task.task_id
    task_module = importlib.import_module("chronos.tasks.{}".format(task_uid))

    logger.debug("Starting task with ID: {}", task.id)
    task.time_started = datetime.datetime.now()
    task.status = "STARTED"
    task.save()

    task_module.run(task.task_arguments, event)

    task.time_finished = datetime.datetime.now()
    task.status = "FINISHED"
    task.save()
    logger.debug("Finished task with ID: {}", task.id)

    return


def execute_next_task():
    tasks = (
        Task.select()
        .where(Task.status == "WAITING")
        .order_by(Task.time_scheduled.asc())
        .order_by(Task.priority.desc())
    )

    if len(tasks) > 0:
        task_thread = threading.Thread(target=execute_task(tasks[0]))
        task_thread.start()
