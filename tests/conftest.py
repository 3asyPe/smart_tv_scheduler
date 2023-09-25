import pytest
import tempfile

from unittest.mock import Mock

from models.task import Task
from services.scheduler import Scheduler


@pytest.fixture
def scheduler(mocker):
    return Mock(spec=Scheduler)


@pytest.fixture
def test_task():
    return Task(
        name="test",
        start_at="*/1 * * * *",
        function="analytics",
        run_statuses=["active"],
        params={},
    )


@pytest.fixture
def test_task_2():
    return Task(
        name="test_2",
        start_at="*/1 * * * *",
        function="launch_application",
        run_statuses=["standby"],
        params={},
    )


@pytest.fixture(autouse=True)
def tasks_dir(mocker):
    with tempfile.TemporaryDirectory() as tmpdirname:
        mocker.patch("config.config.USER_TASKS_PATH", f"{tmpdirname}/user_tasks.json")
        mocker.patch(
            "config.config.SYSTEM_TASKS_PATH", f"{tmpdirname}/system_tasks.json"
        )
        yield tmpdirname
