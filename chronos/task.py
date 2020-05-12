import json
import importlib
import datetime
import threading

from loguru import logger

from chronos.metadata import Task, Session
from chronos.event import event




def dispatch_task(task_id, task_arguments, task_priority="ROUTINE"):
    session = Session()
    task = Task(
        task_id=task_id,
        task_arguments=json.dumps(task_arguments),
        priority=task_priority,
        status="WAITING"
    )

    session.add(task)
    session.commit()
    logger.debug("Dispatched task: {}", task_id)

    session.close()

    return True


def execute_task(id):
    session = Session()
    task = session.query(Task).get(id)
    logger.debug("Processing task with ID: {}", id)
    task_uid = task.task_id
    task_module = importlib.import_module("chronos.tasks.{}".format(task_uid))

    logger.debug("Starting task with ID: {}", id)
    task.time_started = datetime.datetime.now()
    task.status = "STARTED"
    session.commit()

    task_module.run(task.task_arguments, event)

    task.time_finished = datetime.datetime.now()
    task.status = "FINISHED"
    session.commit()
    logger.debug("Finished task with ID: {}", id)

    session.close()

    return


def execute_next_task():
    session = Session()
    tasks = session.query(Task).filter(Task.status == "WAITING")

    # logger.debug("Executing next available task...")

    for task in tasks:
        if task.priority == "NOW":
            task_thread = threading.Thread(target=execute_task(task.id))
            task_thread.start()
            logger.debug("Next task has been scheduled")

            return

    if tasks.count() > 0:
        task_thread = threading.Thread(target=execute_task(tasks[0].id))
        task_thread.start()
       #  logger.debug("Next task has been scheduled")

    

    session.close()
        
