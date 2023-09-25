import pytest

from unittest.mock import Mock

from services.scheduler import Scheduler


@pytest.fixture(autouse=True)
def background_scheduler(mocker):
    mock = Mock()
    mock.add_job.return_value = Mock()
    mocker.patch("services.scheduler.BackgroundScheduler", return_value=mock)
    return mock


def test_add_task(test_task, background_scheduler):
    scheduler = Scheduler()
    scheduler.add_task(test_task)

    assert scheduler.tasks == {
        test_task.name: {
            "task": test_task,
            "job": background_scheduler.add_job.return_value,
        }
    }


def test_add_task_with_already_existing_name(test_task, background_scheduler):
    scheduler = Scheduler()
    scheduler.add_task(test_task)
    scheduler.add_task(test_task)

    assert scheduler.tasks == {
        test_task.name: {
            "task": test_task,
            "job": background_scheduler.add_job.return_value,
        }
    }


def test_remove_task(test_task, background_scheduler):
    scheduler = Scheduler()
    scheduler.add_task(test_task)
    scheduler.remove_task(test_task.name)

    assert scheduler.tasks == {}


def test_remove_non_existent_task(test_task, background_scheduler):
    scheduler = Scheduler()
    scheduler.remove_task(test_task.name)

    assert scheduler.tasks == {}


def test_run_task(test_task, test_task_2, background_scheduler, mocker):
    mocker.patch("services.scheduler.get_tv_status", return_value="active")

    func_1 = Mock()
    func_2 = Mock()

    mocker.patch(
        "services.scheduler.TASKS",
        {
            "analytics": func_1,
            "launch_application": func_2,
        },
    )

    scheduler = Scheduler()
    scheduler.run_task(test_task)
    scheduler.run_task(test_task_2)  # shouldn't run because of status

    func_1.assert_called_once()
    func_2.assert_not_called()
