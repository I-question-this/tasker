#!/usr/bin/env python3
"""Create today's schedule from today's tasks"""
import argparse
import datetime
import os
import sys

from ..database import DATABASE, save_database
from ..schedule import Schedule

def main() -> Schedule:
    """Return today's proposed schedule based on the recurring tasks.
    Parameters
    ----------
    date: datetime.date
        The date to propose a schedule for.
    """
    # Get the proposed schedule
    schedules = {}
    for i in range(0,7):
        d = datetime.datetime(year=1970, month=1, day=5)
        d += datetime.timedelta(days=i)
        schedules[d] = DATABASE.proposed_schedule(d)

    return schedules


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
    args = parser.parse_args(args=args)
    return args


def cli_interface() -> None:
    """Get program arguments from command line and run main"""
    args = parse_arguments()
    schedules = main(**vars(args))
    for d in sorted(schedules):
        print(f"{d.strftime('%A')}\n{schedules[d]}")
    sys.exit(0)


# Execute only if this file is being run as the entry file.
if __name__ == "__main__":
    cli_interface()
