#!/usr/bin/env python3
"""Checks all pending tasks with the tag "Reminder"."""

import sys

from .check_off_tasks import main, parse_arguments


def cli_interface() -> None:
    """Run check_off_tasks for pending Reminder tasks"""
    main(["+Reminder", "status:pending"])
    sys.exit(0)

if __name__ == "__main__":
    cli_interface()
