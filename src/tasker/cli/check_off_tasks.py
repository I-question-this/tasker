#!/usr/bin/env python3
"""Checks all tasks with given filters"""
import argparse
from dateutil.parser import isoparse
import sys

from ..util import complete_task, run_task_export, time_till_due   


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
