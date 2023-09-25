# smart_tv_scheduler

## Application Structure
- services/task_manager.TaskManager - the main manager of tasks. Loads existing, ability to add and remove user tasks.
- services/scheduler.Scheduler - class used for scheduling tasks by TaskManager
- services/functions - tasks' business logics
- services/api - api provided by tv (getting the status)
- models/task.Task - pydantic model of a task
- data/system_tasks.json - file with preloaded system tasks
- data/user_tasks.json - custom tasks added by user

### Task model
```
{
  "<name>": {
    "start_at": <cron expression>,
    "function": <function name>,
    "params": {
      "<function param name>": "<function param value>"
    },
    "run_statuses": ["<tv status in which tv has to be in order to run the task>"]
  }
}
```

## How to install

Using poetry:
```
poetry shell
poetry install
```

Using pip:
```
pip install -r requirements.txt
```
or
```
pip install -r requirements-dev.txt
```

## Tests
In order to run tests run:
```
pytest
```

## What can be improved
- Change file system task saving on sqlite
- Improved customization of user tasks
- Error tolerance

