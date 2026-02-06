import argparse
import sys

from src.services.task_service import update_task


def update_task_command(args: list[str] = None):
    """
    CLI command to update an existing task's title and/or description.

    Args:
        args: Command-line arguments (None = use sys.argv)

    Exit Codes:
        0: Success (task updated)
        1: Error (task not found, validation failed, no updates)
        2: Usage error (argparse validation failed)
    """
    parser = argparse.ArgumentParser(
        description="Update an existing task's title and/or description",
        prog='todo update'
    )

    # Positional argument
    parser.add_argument(
        'task_id',
        type=str,
        help='Unique task identifier (UUID)'
    )

    # Optional flags
    parser.add_argument(
        '--title',
        type=str,
        default=None,
        help='New task title (1-500 characters)'
    )

    parser.add_argument(
        '--description',
        type=str,
        default=None,
        help='New task description (0-5000 characters, optional)'
    )

    # Parse arguments
    parsed_args = parser.parse_args(args)

    # Validate at least one update provided
    if parsed_args.title is None and parsed_args.description is None:
        print("Error: No updates provided. Use --title and/or --description", file=sys.stderr)
        sys.exit(1)

    # Call service layer
    try:
        updated_task = update_task(
            task_id=parsed_args.task_id,
            title=parsed_args.title,
            description=parsed_args.description
        )

        # Display success message
        print("Task updated successfully!")
        print(f"ID: {updated_task.id}")
        print(f"Title: {updated_task.title}")
        print(f"Description: {updated_task.description if updated_task.description else '(none)'}")
        print(f"Status: {updated_task.status.value.capitalize()}")

        sys.exit(0)

    except KeyError:
        print(f"Error: Task not found with ID: {parsed_args.task_id}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    update_task_command()
