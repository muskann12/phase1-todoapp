"""CLI command for marking tasks as complete."""

import argparse
import sys
from src.services.task_service import mark_complete
from src.models.task import TaskStatus


def complete_task_command(args: list[str]) -> None:
    """
    CLI command to mark a task as complete.

    Args:
        args: Command-line arguments (excluding 'complete')
    """
    parser = argparse.ArgumentParser(
        description="Mark a task as complete",
        prog="complete"
    )
    parser.add_argument(
        "task_id",
        help="The ID of the task to mark as complete"
    )

    try:
        parsed_args = parser.parse_args(args)
        task = mark_complete(parsed_args.task_id)

        # Display success message
        desc_display = task.description if task.description else "(none)"
        status_display = "Complete" if task.status == TaskStatus.COMPLETE else "Incomplete"
        print(f"Task marked as complete! ID: {task.id}, Title: {task.title}, Description: {desc_display}, Status: {status_display}")
        sys.exit(0)

    except KeyError:
        print(f"Error: Task not found with ID: {parsed_args.task_id}", file=sys.stderr)
        sys.exit(1)
