#!/usr/bin/env python3
"""Checks all tasks with given filters"""

import argparse
import datetime
from dateutil.parser import isoparse
import json
import subprocess
import os
import sys


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


def main(filters: list[str]) -> int:
    """Run through the tasks matching the given filter, asking the user if they 
    have been completed.
    """

    # Get Reminder tasks
    tasks = run_task_export(filters)

    # Sort by due date
    tasks.sort(key=lambda t: t["due"])

    # Go through each task
    for t in tasks:
        print(f"{t['id']} -- \"{t['description']}\" -- ", end="")
        print(f"Due: {time_till_due(isoparse(t['due']))}")
        done = input("Completed?: ").lower()[0]
        if done == "y":
            print(complete_task(t['id']), end="")
        print("-"*os.get_terminal_size().columns)


def parse_arguments(args=None) -> None:
    """Returns the parsed arguments.

    Parameters
    ----------
    args: List of strings to be parsed by argparse.
        The default None results in argparse using the values passed into
        sys.args.
    """
    parser = argparse.ArgumentParser(
            description="Run through the tasks matching the given filter, "
                        "asking the user if they have been completed.",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("filters", nargs='+', help="The filters to use.")
    args = parser.parse_args(args=args)
    return args


def cli_interface() -> None:
    """Get program arguments from command line and run main"""
    args = parse_arguments()
    main(**vars(args))
    sys.exit(0)


# Execute only if this file is being run as the entry file.
if __name__ == "__main__":
    cli_interface()
