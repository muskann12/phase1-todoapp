"""
Interactive UI utilities for the Todo CLI application.

This module provides helper functions for the menu-driven interactive mode,
including ANSI color support, table rendering, and menu display.
"""
import sys
from typing import Optional
from colorama import Fore, Style
from src.models.task import Task, TaskStatus
from src.services.task_service import get_all_tasks


# Cross-platform color codes using colorama
class Colors:
    """Cross-platform ANSI color codes using colorama"""
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    RED = Fore.RED
    CYAN = Fore.CYAN
    BOLD = Style.BRIGHT
    RESET = Style.RESET_ALL


def colorize(text: str, color: str) -> str:
    """
    Apply ANSI color to text with cross-platform support via colorama.

    Args:
        text: Text to colorize
        color: Color code (use Colors class constants)

    Returns:
        str: Colorized text with auto-reset
    """
    # Colorama handles the cross-platform conversion automatically
    return f"{color}{text}{Colors.RESET}"


def get_task_summary() -> dict:
    """
    Get summary statistics for all tasks.

    Returns:
        dict: Contains 'total', 'completed', 'pending' counts
    """
    tasks = get_all_tasks()
    total = len(tasks)
    completed = sum(1 for t in tasks if t.status == TaskStatus.COMPLETE)
    pending = total - completed

    return {
        'total': total,
        'completed': completed,
        'pending': pending
    }


def print_banner():
    """Display colorful startup banner with task count"""
    summary = get_task_summary()

    print()
    print(colorize("=" * 60, Colors.CYAN))
    print(colorize("         EVOLUTION OF TODO - PHASE I", Colors.BOLD + Colors.BLUE))
    print(colorize("           Interactive Menu System", Colors.BLUE))
    print(colorize("=" * 60, Colors.CYAN))

    # Task count summary
    if summary['total'] == 0:
        print(colorize("\n  You have no tasks yet. Let's get started!", Colors.YELLOW))
    else:
        completed_color = Colors.GREEN if summary['completed'] > 0 else Colors.YELLOW
        pending_color = Colors.YELLOW if summary['pending'] > 0 else Colors.GREEN

        print(f"\n  You have {colorize(str(summary['total']), Colors.BOLD)} tasks:")
        print(f"    {colorize(str(summary['completed']), completed_color)} completed")
        print(f"    {colorize(str(summary['pending']), pending_color)} pending")

    print()


def print_task_table(tasks: list[Task]):
    """
    Display tasks in a colorful table format with indices.

    Args:
        tasks: List of Task objects to display
    """
    if not tasks:
        print(colorize("  No tasks to display.", Colors.YELLOW))
        return

    # Table header
    print(colorize("\n  YOUR TASKS", Colors.BOLD + Colors.BLUE))
    print(colorize("  " + "─" * 58, Colors.CYAN))

    # Column headers
    header = f"  {'No':<4} {'Status':<10} {'Title':<30} {'Description':<15}"
    print(colorize(header, Colors.BOLD + Colors.BLUE))
    print(colorize("  " + "─" * 58, Colors.CYAN))

    # Task rows
    for idx, task in enumerate(tasks, start=1):
        # Status with color
        if task.status == TaskStatus.COMPLETE:
            status_text = colorize("[✓] Done", Colors.GREEN)
        else:
            status_text = colorize("[ ] Pending", Colors.YELLOW)

        # Truncate long text
        title = task.title[:28] + ".." if len(task.title) > 30 else task.title
        desc = task.description[:13] + ".." if len(task.description) > 15 else task.description
        desc = desc if desc else colorize("(none)", Colors.CYAN)

        # Row
        row = f"  {idx:<4} {status_text:<20} {title:<30} {desc:<15}"
        print(row)

    print(colorize("  " + "─" * 58, Colors.CYAN))
    print()


def show_menu() -> Optional[int]:
    """
    Display the main menu and get user selection.

    Returns:
        Optional[int]: Selected menu option (1-6), or None if invalid
    """
    print(colorize("\n  MAIN MENU", Colors.BOLD + Colors.CYAN))
    print(colorize("  " + "─" * 40, Colors.CYAN))
    print("  1️⃣  Add Task")
    print("  2️⃣  View Tasks")
    print("  3️⃣  Update Task")
    print("  4️⃣  Delete Task")
    print("  5️⃣  Mark Complete / Incomplete")
    print("  6️⃣  Exit")
    print(colorize("  " + "─" * 40, Colors.CYAN))

    try:
        choice = input(colorize("\n  Select an option (1-6): ", Colors.BOLD)).strip()

        if choice.isdigit() and 1 <= int(choice) <= 6:
            return int(choice)
        else:
            print(colorize("\n  ❌ Invalid selection. Please choose 1-6.", Colors.RED))
            return None
    except (EOFError, KeyboardInterrupt):
        print("\n")
        return 6  # Treat interrupt as exit


def get_task_by_index(index: int) -> Optional[Task]:
    """
    Get a task by its display index (1-based).

    Args:
        index: Display index (1, 2, 3, ...)

    Returns:
        Optional[Task]: Task object if found, None otherwise
    """
    tasks = get_all_tasks()

    if 1 <= index <= len(tasks):
        return tasks[index - 1]
    return None


def prompt_for_task_selection(action: str = "select") -> Optional[Task]:
    """
    Show task table and prompt user to select a task by index.

    Args:
        action: Action verb for prompt (e.g., "update", "delete")

    Returns:
        Optional[Task]: Selected task, or None if cancelled/invalid
    """
    tasks = get_all_tasks()

    if not tasks:
        print(colorize("\n  ❌ No tasks available.", Colors.RED))
        return None

    # Show table
    print_task_table(tasks)

    # Get selection
    try:
        choice = input(colorize(f"\n  Enter task number to {action} (or 0 to cancel): ", Colors.BOLD)).strip()

        if choice == '0':
            print(colorize("  Operation cancelled.", Colors.YELLOW))
            return None

        if choice.isdigit():
            index = int(choice)
            task = get_task_by_index(index)

            if task:
                return task
            else:
                print(colorize(f"\n  ❌ Invalid task number. Please choose 1-{len(tasks)}.", Colors.RED))
                return None
        else:
            print(colorize("\n  ❌ Please enter a valid number.", Colors.RED))
            return None

    except (EOFError, KeyboardInterrupt):
        print(colorize("\n  Operation cancelled.", Colors.YELLOW))
        return None


def prompt_for_input(prompt: str, allow_empty: bool = False) -> Optional[str]:
    """
    Prompt user for text input with validation.

    Args:
        prompt: Prompt text to display
        allow_empty: Whether to allow empty input

    Returns:
        Optional[str]: User input, or None if cancelled
    """
    try:
        value = input(colorize(f"\n  {prompt}: ", Colors.BOLD)).strip()

        if not value and not allow_empty:
            print(colorize("  ❌ Input cannot be empty.", Colors.RED))
            return None

        return value

    except (EOFError, KeyboardInterrupt):
        print(colorize("\n  Operation cancelled.", Colors.YELLOW))
        return None


def print_success(message: str):
    """Print success message in green"""
    print(colorize(f"\n  ✅ {message}", Colors.GREEN))


def print_error(message: str):
    """Print error message in red"""
    print(colorize(f"\n  ❌ {message}", Colors.RED))


def print_info(message: str):
    """Print info message in cyan"""
    print(colorize(f"\n  ℹ️  {message}", Colors.CYAN))


def pause():
    """Pause and wait for user to press Enter"""
    try:
        input(colorize("\n  Press Enter to continue...", Colors.CYAN))
    except (EOFError, KeyboardInterrupt):
        print()
