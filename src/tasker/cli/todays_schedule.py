#!/usr/bin/env python3
"""Create today's schedule from today's tasks"""
import argparse
import datetime
from dateutil.parser import isoparse
import os
import sys

from ..database import DATABASE, save_database
from ..schedule import Schedule

def quit_task_editing():
    pass

def delete_task(schedule: Schedule, task_id: int)\
        -> Schedule:
    if task_id is None:
        print("A task id must be selected for this command")
    elif 0 <= task_id < len(schedule.tasks):
        del schedule.tasks[task_id]
        print(f"Deleted task {task_id}")
    else:
        print("Selected task {task_id} is out of range")
    print("-"*os.get_terminal_size().columns)
    return schedule

def edit_start_time(schedule: Schedule, task_id: int,
        new_start_time: datetime.date) -> Schedule:
    if task_id is None:
        print("A task id must be selected for this command")
    elif 0 <= task_id < len(schedule.tasks):
        schedule.tasks[task_id].start = new_start_time
        print(f"Deleted task {task_id}")
    else:
        print("Selected task {task_id} is out of range")
    print("-"*os.get_terminal_size().columns)
    return schedule

def parse_task_args(args):
    parser = argparse.ArgumentParser(
            description="Edit tasks",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            exit_on_error=False)
    parser.set_defaults(func=None)
    subparsers = parser.add_subparsers(help="sub-command help")

    # Create parser for the quit task command
    parser_add = subparsers.add_parser("quit", 
            help="Quit")
    parser_add.set_defaults(func=quit_task_editing)

    # Create parser for the delete task command
    parser_add = subparsers.add_parser("delete", 
            help="Delete a task")
    parser_add.add_argument("task_id", type=int, 
            help="task id to delete")
    parser_add.set_defaults(func=delete_task)

    # Create parser for the edit start time command
    parser_add = subparsers.add_parser("edit_start",
            help="Edit the start time.")
    parser_add.add_argument("task_id", type=int, 
            help="task id to edit the start time of")
    parser_add.add_argument("new_start_time", 
            type=datetime.time.fromisoformat,
            help="The new start time.")
    parser_add.set_defaults(func=edit_start_time)

    # Parse arguments
    try:
        args = parser.parse_args(args=args)
    except argparse.ArgumentError:
        parser.print_help()
        print("-"*os.get_terminal_size().columns)
        return None

    # Check if a subcommand was given
    if args.func is None:
        parser.print_help()
        print("-"*os.get_terminal_size().columns)
        return None
    else:
        return args

def main(date: datetime.date) -> Schedule:
    """Return today's proposed schedule based on the recurring tasks.
    Parameters
    ----------
    date: datetime.date
        The date to propose a schedule for.
    """
    # Get the proposed schedule
    proposed_schedule = DATABASE.proposed_schedule(date)

   
    user_wants_to_quit = False
    while(not user_wants_to_quit):
        # Show the user the schedule
        print(f"Proposed Schedule:\n{proposed_schedule}")
        print("-"*os.get_terminal_size().columns)
        # Get user arguments
        user_args = input("Edits?: ").split()
        parsered_args = parse_task_args(user_args)

        if parsered_args is not None:
            if parsered_args.func == quit_task_editing:
                user_wants_to_quit = True
            else:
                func = parsered_args.func
                del parsered_args.func
                parsered_args.schedule = proposed_schedule
                proposed_schedule = func(**vars(parsered_args))

    # Finish with another set of dashes
    print("-"*os.get_terminal_size().columns)

    # Return the final schedule
    return proposed_schedule


def parse_arguments(args=None) -> None:
    """Returns the parsed arguments.

    Parameters
    ----------
    args: List of strings to be parsed by argparse.
        The default None results in argparse using the values passed into
        sys.args.
    """
    parser = argparse.ArgumentParser(
            description="Print out today's proposed schedule based on the "\
                        "recurring tasks.",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-d", "--date", default=datetime.datetime.now(),
                        type=isoparse)
    args = parser.parse_args(args=args)
    return args


def cli_interface() -> None:
    """Get program arguments from command line and run main"""
    args = parse_arguments()
    final_schedule = main(**vars(args))
    print(f"Final Schedule:\n{final_schedule}")
    sys.exit(0)


# Execute only if this file is being run as the entry file.
if __name__ == "__main__":
    cli_interface()
