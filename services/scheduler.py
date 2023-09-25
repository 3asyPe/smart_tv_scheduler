from logging import getLogger

from typing import Optional

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from services.api import get_tv_status
from models.task import Task
from services.functions import TASKS


logger = getLogger(__name__)


class Scheduler:
    def __init__(self):
        self.client = BackgroundScheduler()
        self.tasks = {}

    def run(self, tasks: Optional[list[Task]] = None):
        if tasks is None:
            tasks = []

        for task in tasks:
            self.add_task(task)

        self.client.start()

    def add_task(self, task: Task):
        if task.name in self.tasks:
            self.remove_task(task.name)

        job = self.client.add_job(
            func=self.run_task,
            kwargs={"task": task},
            trigger=CronTrigger.from_crontab(task.start_at),
        )
        self.tasks[task.name] = {
            "task": task,
            "job": job,
        }

    def remove_task(self, task_name: str):
        if task_name not in self.tasks:
            return

        job = self.tasks[task_name]["job"]
        self.client.remove_job(job_id=job.id)
        self.tasks.pop(task_name)

    def run_task(self, task: Task):
        logger.info(f"Running task {task.name}")
        if get_tv_status() not in task.run_statuses:
            return

        if task.function not in TASKS:
            logger.error(f'Function "{task.function}" not found')

        TASKS[task.function](**task.params)
