import json
import importlib
import datetime
import threading

from loguru import logger

from chronos.metadata import Task, Session
from chronos.event import event


def dispatch_task(task_id, task_arguments={}, task_priority="ROUTINE"):
    session = Session()
    task = Task(
        task_id=task_id,
        task_arguments=json.dumps(task_arguments),
        priority=task_priority,
        status="WAITING",
    )

    session.add(task)
    session.commit()
    logger.debug("Dispatched task: {}", task_id)
    event.trigger("task_dispatched", {"task_id": task_id})

    execute_task_in_thread(task.id)
    session.close()

    return True


def execute_task(id):
    session = Session()
    task = session.query(Task).get(id)
    logger.debug("Processing task with ID: {}", id)
    task_uid = task.task_id
    task_module = importlib.import_module("chronos.tasks.{}".format(task_uid))
    task_id_dict = {"task_id": id}

    logger.debug("Starting task with ID: {}", id)
    task.time_started = datetime.datetime.now()
    task.status = "STARTED"
    session.flush()
    session.commit()

    event.trigger("task_started", task_id_dict)
    arguments = {**json.loads(task.task_arguments), **task_id_dict}

    try:
        task.output = task_module.run(json.dumps(arguments), event)
    except Exception as error:
        logger.error("Task with ID: {} errored with exception: {}", id, error)

    event.trigger("task_finished", task_id_dict)

    task.time_finished = datetime.datetime.now()
    task.status = "FINISHED"
    session.flush()
    session.commit()
    logger.debug("Finished task with ID: {}", id)

    session.close()

    return


def execute_task_in_thread(id):
    task_thread = threading.Thread(target=execute_task(id))
    task_thread.start()


def execute_next_task():
    session = Session()
    tasks = session.query(Task).filter(Task.status == "WAITING")

    # logger.debug("Executing next available task...")

    for task in tasks:
        if task.priority == "NOW":
            task_thread = threading.Thread(target=execute_task(task.id))
            task_thread.start()
            # logger.debug("Next task has been scheduled")

            return

    if tasks.count() > 0:
        task_thread = threading.Thread(target=execute_task(tasks[0].id))
        task_thread.start()
    #  logger.debug("Next task has been scheduled")

    session.close()
