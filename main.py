import logging
from time import sleep

from config import config
from models.task import Task
from services.task_manager import TaskManager


logging.basicConfig(level=config.LOG_LEVEL)


if __name__ == "__main__":
    task_manager = TaskManager().start()

    # Add some test tasks
    task_manager.create_task(
        Task(
            name="test",
            start_at="*/1 * * * *",
            function="analytics",
            run_statuses=["active"],
            params={},
        )
    )

    sleep(3)

    task_manager.create_task(
        Task(
            name="test_2",
            start_at="*/1 * * * *",
            function="analytics",
            run_statuses=["active"],
            params={},
        )
    )

    sleep(70)

    task_manager.delete_task(task_name="test")

    while True:
        pass
