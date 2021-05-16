#!/usr/bin/env python3
"""Create today's schedule from today's tasks"""
import argparse
import datetime
from dateutil.parser import isoparse
import sys

from ..database import DATABASE, save_database


def main(date: datetime.date) -> str:
    """Return today's proposed schedule based on the recurring tasks.
    """
    return str(DATABASE.proposed_schedule(date))


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
    print(main(**vars(args)))
    sys.exit(0)


# Execute only if this file is being run as the entry file.
if __name__ == "__main__":
    cli_interface()
