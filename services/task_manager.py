import json
from config import config
from typing import Optional
from models.task import Task
from services.scheduler import Scheduler


class TaskManager:
    def __init__(self, scheduler: Optional[Scheduler] = None):
        self.scheduler = scheduler or Scheduler()

    def start(self):
        self.load_system_tasks()
        self.load_user_tasks()
        self.scheduler.run()

        return self

    def load_tasks(self, file_name: str) -> None:
        tasks = self._load_file(file_name=file_name)
        for name, task in tasks.items():
            self.scheduler.add_task(Task(name=name, **task))

    def load_system_tasks(self) -> None:
        self.load_tasks(config.SYSTEM_TASKS_PATH)

    def load_user_tasks(self) -> None:
        self.load_tasks(config.USER_TASKS_PATH)

    def create_task(self, task: Task) -> Task:
        tasks = self._load_file(file_name=config.USER_TASKS_PATH)
        tasks[task.name] = task.model_dump(exclude={"name"})

        with open(config.USER_TASKS_PATH, "w") as f:
            f.write(json.dumps(tasks))

        self.scheduler.add_task(task)

        return task

    def delete_task(self, task_name: str) -> None:
        tasks = self._load_file(file_name=config.USER_TASKS_PATH)
        tasks.pop(task_name)

        with open(config.USER_TASKS_PATH, "w") as f:
            f.write(json.dumps(tasks))

        self.scheduler.remove_task(task_name)

    def _load_file(self, file_name: str) -> dict:
        with open(file_name, "a+") as file:
            file.seek(0)
            content = file.read().strip()

        if not content:
            return {}

        return json.loads(content)
