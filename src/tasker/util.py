"""Utility methods"""
import datetime
import json
import subprocess
import os

def complete_task(id: int) -> str:
    """Return the output of completing the given task id.

    Parameters
    ----------
    id: int
        The id of the task to complete.

    Returns
    -------
    str
        The output of task from completing the given task id.
    """
    # Prepare command
    command = ["task", f"{id}", "done"]

    # Run command
    completed_process = subprocess.run(command, capture_output=True)

    # Return result
    return completed_process.stdout.decode("utf-8")


def run_task_export(filters: list[str]) -> list:
    """Returns JSON of exporting with the given filters
    
    Parameters
    ----------
    filters: list[str]
        The list of filters to use.
    
    Returns
    -------
    list
        The list of tasks that match the given filter.
    """
    # Prepare command
    command = ["task"]
    command.extend(filters)
    command.append("export")

    # Run command
    completed_process = subprocess.run(command, capture_output=True)

    # Return JSON
    return json.loads(completed_process.stdout.decode("utf-8"))


def time_till_due(due:datetime.datetime) -> datetime.timedelta:
    """Return the timedelta of now and the given due date.
    
    Parameters
    ----------
    due: datetime.datetime
        The due date

    Returns
    -------
    datetime.timedelta
        The timedelta between now and the given due date.
    """
    # Get the current time
    now = datetime.datetime.now()

    # Put now in the same timezone as due
    now = now.replace(tzinfo=due.tzinfo)

    # Return the time delta
    return due - now
