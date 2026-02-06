import argparse
import sys

from src.services.task_service import create_task


def add_task_command(args: list[str] = None):
    """
    CLI command to add a new task.

    Args:
        args: Command-line arguments (None = use sys.argv)
    """
    parser = argparse.ArgumentParser(
        description='Add a new task to your todo list',
        prog='todo add'
    )

    parser.add_argument(
        'title',
        type=str,
        help='Task title (required, 1-500 characters)'
    )

    parser.add_argument(
        '-d', '--description',
        type=str,
        default='',
        help='Task description (optional, max 5000 characters)'
    )

    # Parse arguments
    parsed_args = parser.parse_args(args)

    try:
        # Create task via service layer
        task = create_task(parsed_args.title, parsed_args.description)

        # Success output
        print("Task created successfully!")
        print(f"ID: {task.id}")
        print(f"Title: {task.title}")
        print(f"Description: {task.description if task.description else '(none)'}")
        print(f"Status: {task.status.value.capitalize()}")
        print(f"Created: {task.created.isoformat()}")

        sys.exit(0)

    except ValueError as e:
        # Validation error
        print(f"Error: {e}", file=sys.stderr)
        print(f"Usage: todo add <title> [--description <description>]", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        # Unexpected error
        print(f"Internal error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == '__main__':
    add_task_command()
