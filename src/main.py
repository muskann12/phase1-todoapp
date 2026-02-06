import sys
import shlex
import colorama

# Initialize colorama for cross-platform ANSI color support
colorama.init(autoreset=True)


def execute_command(command_line: str):
    """
    Execute a single command from the interactive shell or CLI.

    Args:
        command_line: Command string (e.g., "add Buy milk -d Get 2%")

    Returns:
        bool: True to continue, False to exit
    """
    # Parse command line respecting quotes
    try:
        parts = shlex.split(command_line)
    except ValueError as e:
        print(f"Error parsing command: {e}", file=sys.stderr)
        return True

    if not parts:
        return True

    command = parts[0].lower()
    args = parts[1:]

    # Handle exit commands
    if command in ('exit', 'quit', 'q'):
        return False

    # Handle help command
    if command in ('help', '?'):
        print("\nAvailable commands:")
        print("  add <title> [-d <description>]  - Add a new task")
        print("  view                             - View all tasks")
        print("  update <id> [--title T] [-d D]   - Update a task")
        print("  delete <id>                      - Delete a task")
        print("  complete <id>                    - Mark task as complete")
        print("  incomplete <id>                  - Mark task as incomplete")
        print("  toggle <id>                      - Toggle task status")
        print("  help, ?                          - Show this help")
        print("  exit, quit, q                    - Exit the application")
        print()
        return True

    # Route to appropriate command handler
    try:
        if command == 'add':
            from src.cli.add_task import add_task_command
            add_task_command(args)
        elif command == 'view':
            from src.cli.view_tasks import view_tasks_command
            view_tasks_command(args)
        elif command == 'update':
            from src.cli.update_task import update_task_command
            update_task_command(args)
        elif command == 'delete':
            from src.cli.delete_task import delete_task_command
            delete_task_command(args)
        elif command == 'complete':
            from src.cli.complete_task import complete_task_command
            complete_task_command(args)
        elif command == 'incomplete':
            from src.cli.incomplete_task import incomplete_task_command
            incomplete_task_command(args)
        elif command == 'toggle':
            from src.cli.toggle_task import toggle_task_command
            toggle_task_command(args)
        else:
            print(f"Unknown command: {command}", file=sys.stderr)
            print("Type 'help' for available commands", file=sys.stderr)
    except SystemExit:
        # Commands call sys.exit(), catch it in interactive mode
        pass

    return True


def interactive_mode():
    """Run the application in interactive menu-driven mode"""
    from src.cli.interactive_ui import (
        print_banner,
        print_task_table,
        show_menu,
        prompt_for_task_selection,
        prompt_for_input,
        print_success,
        print_error,
        pause
    )
    from src.services.task_service import (
        create_task,
        get_all_tasks,
        update_task,
        delete_task,
        toggle_status
    )

    # Display startup banner with task count
    print_banner()

    while True:
        try:
            # Show current tasks
            tasks = get_all_tasks()
            if tasks:
                print_task_table(tasks)

            # Show menu and get selection
            choice = show_menu()

            if choice is None:
                # Invalid input, loop again
                continue

            # Handle menu options
            if choice == 1:
                # Add Task
                title = prompt_for_input("Enter task title", allow_empty=False)
                if title:
                    description = prompt_for_input("Enter task description (optional)", allow_empty=True)
                    try:
                        task = create_task(title, description or "")
                        print_success(f"Task created: {task.title}")
                    except ValueError as e:
                        print_error(str(e))
                pause()

            elif choice == 2:
                # View Tasks - already shown above, just pause
                if not tasks:
                    print_error("No tasks available.")
                pause()

            elif choice == 3:
                # Update Task
                task = prompt_for_task_selection("update")
                if task:
                    print(f"\n  Current title: {task.title}")
                    print(f"  Current description: {task.description or '(none)'}")

                    new_title = prompt_for_input("Enter new title (or leave empty to keep current)", allow_empty=True)
                    new_desc = prompt_for_input("Enter new description (or leave empty to keep current)", allow_empty=True)

                    try:
                        # Only update if at least one field provided
                        if new_title or new_desc:
                            updated_task = update_task(
                                task.id,
                                title=new_title if new_title else None,
                                description=new_desc if new_desc else None
                            )
                            print_success(f"Task updated: {updated_task.title}")
                        else:
                            print_error("No updates provided.")
                    except (ValueError, KeyError) as e:
                        print_error(str(e))
                pause()

            elif choice == 4:
                # Delete Task
                task = prompt_for_task_selection("delete")
                if task:
                    # Confirm deletion
                    confirm = input(f"\n  Are you sure you want to delete '{task.title}'? (y/N): ").strip().lower()
                    if confirm == 'y':
                        try:
                            deleted_task = delete_task(task.id)
                            print_success(f"Task deleted: {deleted_task.title}")
                        except KeyError as e:
                            print_error(str(e))
                    else:
                        print_error("Deletion cancelled.")
                pause()

            elif choice == 5:
                # Toggle Task Status
                task = prompt_for_task_selection("toggle")
                if task:
                    try:
                        updated_task = toggle_status(task.id)
                        status_text = "completed" if updated_task.status.value == "complete" else "pending"
                        print_success(f"Task marked as {status_text}: {updated_task.title}")
                    except KeyError as e:
                        print_error(str(e))
                pause()

            elif choice == 6:
                # Exit
                print("\n  👋 Goodbye! Have a productive day!\n")
                break

        except (EOFError, KeyboardInterrupt):
            print("\n\n  👋 Goodbye! Have a productive day!\n")
            break
        except Exception as e:
            print_error(f"Unexpected error: {e}")
            pause()


def main():
    """Main entry point for the todo CLI application"""

    # If no arguments, enter interactive mode (maintains session)
    if len(sys.argv) < 2:
        interactive_mode()
        return

    # Single command mode (for scripts/automation)
    command = sys.argv[1]

    if command == 'add':
        from src.cli.add_task import add_task_command
        add_task_command(sys.argv[2:])
    elif command == 'view':
        from src.cli.view_tasks import view_tasks_command
        view_tasks_command(sys.argv[2:])
    elif command == 'update':
        from src.cli.update_task import update_task_command
        update_task_command(sys.argv[2:])
    elif command == 'delete':
        from src.cli.delete_task import delete_task_command
        delete_task_command(sys.argv[2:])
    elif command == 'complete':
        from src.cli.complete_task import complete_task_command
        complete_task_command(sys.argv[2:])
    elif command == 'incomplete':
        from src.cli.incomplete_task import incomplete_task_command
        incomplete_task_command(sys.argv[2:])
    elif command == 'toggle':
        from src.cli.toggle_task import toggle_task_command
        toggle_task_command(sys.argv[2:])
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        print("Available commands: add, view, update, delete, complete, incomplete, toggle", file=sys.stderr)
        print("Or run without arguments for interactive mode: python -m src.main", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
