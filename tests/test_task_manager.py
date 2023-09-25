import json
import pytest

from config import config
from services.task_manager import TaskManager


@pytest.fixture
def created_system_task(test_task):
    with open(config.SYSTEM_TASKS_PATH, "w+t") as file:
        json.dump(
            {test_task.name: test_task.model_dump(exclude={"name"})},
            file,
        )
    yield test_task


@pytest.fixture
def created_user_task(test_task_2):
    with open(config.USER_TASKS_PATH, "w+t") as file:
        json.dump(
            {test_task_2.name: test_task_2.model_dump(exclude={"name"})},
            file,
        )
    yield test_task_2


def test_load_system_tasks(scheduler, created_system_task):
    TaskManager(scheduler=scheduler).load_system_tasks()

    scheduler.add_task.assert_called_once_with(created_system_task)


def test_load_user_tasks(scheduler, created_user_task):
    TaskManager(scheduler=scheduler).load_user_tasks()

    scheduler.add_task.assert_called_once_with(created_user_task)


def test_create_task(scheduler, created_user_task, test_task, created_system_task):
    TaskManager(scheduler=scheduler).create_task(test_task)

    with open(config.USER_TASKS_PATH, "r") as file:
        assert json.load(file) == {
            test_task.name: test_task.model_dump(exclude={"name"}),
            created_user_task.name: created_user_task.model_dump(exclude={"name"}),
        }

    with open(config.SYSTEM_TASKS_PATH, "r") as file:
        assert json.load(file) == {
            created_system_task.name: created_system_task.model_dump(exclude={"name"})
        }

    scheduler.add_task.assert_called_once_with(test_task)


def test_delete_task(scheduler, created_user_task, test_task_2, created_system_task):
    TaskManager(scheduler=scheduler).delete_task(test_task_2.name)

    with open(config.USER_TASKS_PATH, "r") as file:
        assert json.loads(file.read().strip()) == {}

    with open(config.SYSTEM_TASKS_PATH, "r") as file:
        assert json.load(file) == {
            created_system_task.name: created_system_task.model_dump(exclude={"name"})
        }

    scheduler.remove_task.assert_called_once_with(test_task_2.name)
