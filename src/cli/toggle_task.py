"""CLI command for toggling task status."""

import argparse
import sys
from src.services.task_service import toggle_status
from src.models.task import TaskStatus


def toggle_task_command(args: list[str]) -> None:
    """
    CLI command to toggle a task's completion status.

    Args:
        args: Command-line arguments (excluding 'toggle')
    """
    parser = argparse.ArgumentParser(
        description="Toggle a task's completion status",
        prog="toggle"
    )
    parser.add_argument(
        "task_id",
        help="The ID of the task to toggle"
    )

    try:
        parsed_args = parser.parse_args(args)
        task = toggle_status(parsed_args.task_id)

        # Display success message
        desc_display = task.description if task.description else "(none)"
        status_display = "Complete" if task.status == TaskStatus.COMPLETE else "Incomplete"
        print(f"Task status toggled! ID: {task.id}, Title: {task.title}, Description: {desc_display}, Status: {status_display}")
        sys.exit(0)

    except KeyError:
        print(f"Error: Task not found with ID: {parsed_args.task_id}", file=sys.stderr)
        sys.exit(1)
