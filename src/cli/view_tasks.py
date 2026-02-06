import argparse
import sys

from src.models.task import TaskStatus
from src.services.task_service import get_all_tasks


def view_tasks_command(args: list[str] = None):
    """
    CLI command to view all tasks.

    Args:
        args: Command-line arguments (None = use sys.argv)

    Exit Codes:
        0: Success (tasks displayed or empty-state message shown)
    """
    parser = argparse.ArgumentParser(
        description='View all tasks in your todo list',
        prog='todo view'
    )

    # No positional arguments or options needed for Phase I
    parser.parse_args(args)

    # Retrieve all tasks
    tasks = get_all_tasks()

    # Empty state handling
    if not tasks:
        print('No tasks found. Add your first task with: python -m src.main add "<title>"')
        sys.exit(0)

    # Display summary (User Story 2)
    total = len(tasks)
    incomplete = sum(1 for t in tasks if t.status == TaskStatus.INCOMPLETE)
    complete = total - incomplete

    print(f"Total: {total} | Incomplete: {incomplete} | Complete: {complete}")
    print()  # Blank line separator

    # Display tasks (User Story 1)
    for task in tasks:
        # Status indicator
        status_icon = "[✓]" if task.status == TaskStatus.COMPLETE else "[ ]"

        # Description handling
        description = task.description if task.description else "(none)"

        # Multi-line task display
        print(f"{status_icon} ID: {task.id}")
        print(f"    Title: {task.title}")
        print(f"    Description: {description}")
        print(f"    Status: {task.status.value.capitalize()}")
        print()  # Blank line between tasks

    sys.exit(0)


if __name__ == '__main__':
    view_tasks_command()
