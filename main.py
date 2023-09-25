from time import sleep

from models.task import Task
from services.task_manager import TaskManager


if __name__ == "__main__":
    task_manager = TaskManager().start()

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

    sleep(10)

    task_manager.delete_task(task_name="test")

    while True:
        pass
