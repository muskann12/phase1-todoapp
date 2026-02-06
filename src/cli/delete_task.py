import argparse
import sys

from src.services.task_service import delete_task


def delete_task_command(args: list[str] = None):
    """
    CLI command to delete an existing task by ID.

    Args:
        args: Command-line arguments (None = use sys.argv)

    Exit Codes:
        0: Success (task deleted)
        1: Error (task not found)
        2: Usage error (argparse validation failed)
    """
    parser = argparse.ArgumentParser(
        description="Delete an existing task by its unique ID",
        prog='todo delete'
    )

    # Positional argument
    parser.add_argument(
        'task_id',
        type=str,
        help='Unique task identifier (UUID)'
    )

    # Parse arguments
    parsed_args = parser.parse_args(args)

    # Call service layer
    try:
        deleted_task = delete_task(parsed_args.task_id)

        # Display success message
        print("Task deleted successfully!")
        print(f"ID: {deleted_task.id}")
        print(f"Title: {deleted_task.title}")
        print(f"Description: {deleted_task.description if deleted_task.description else '(none)'}")
        print(f"Status: {deleted_task.status.value.capitalize()}")

        sys.exit(0)

    except KeyError:
        print(f"Error: Task not found with ID: {parsed_args.task_id}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    delete_task_command()
