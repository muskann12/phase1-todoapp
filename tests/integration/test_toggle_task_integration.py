"""Integration tests for toggle command."""

import subprocess
import sys
from io import StringIO
from unittest.mock import patch
import pytest
from src.services.task_service import create_task, clear_tasks, mark_complete


def setup_function():
    """Clear storage before each test"""
    clear_tasks()


def test_toggle_task_in_process():
    """Test toggle command success in-process."""
    from src.cli.toggle_task import toggle_task_command

    # Setup: Create incomplete task
    clear_tasks()
    task = create_task("Buy milk", "")
    task_id = task.id

    # Execute: Run toggle command in-process
    with patch("sys.argv", ["toggle", task_id]):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            with patch("sys.exit") as mock_exit:
                toggle_task_command([task_id])

    # Verify: Success message and exit code 0
    output = mock_stdout.getvalue()
    assert "Task status toggled!" in output
    assert task_id in output
    assert "Status: Complete" in output
    mock_exit.assert_called_once_with(0)


def test_toggle_help():
    """Test toggle command help text."""
    # Execute: Run toggle --help
    result = subprocess.run(
        ["python", "-m", "src.main", "toggle", "--help"],
        capture_output=True,
        text=True
    )

    # Verify: Help text displays
    assert result.returncode == 0
    assert "Toggle a task's completion status" in result.stdout
    assert "task_id" in result.stdout


def test_toggle_nonexistent_task():
    """Test toggle command with non-existent task ID."""
    # Execute: Run toggle with invalid ID
    result = subprocess.run(
        ["python", "-m", "src.main", "toggle", "non-existent-id"],
        capture_output=True,
        text=True
    )

    # Verify: Error message and exit code 1
    assert result.returncode == 1
    assert "Error: Task not found with ID: non-existent-id" in result.stderr


def test_toggle_missing_task_id():
    """Test toggle command with missing task ID argument."""
    # Execute: Run toggle without task ID
    result = subprocess.run(
        ["python", "-m", "src.main", "toggle"],
        capture_output=True,
        text=True
    )

    # Verify: argparse error and exit code 2
    assert result.returncode == 2
    assert "required: task_id" in result.stderr
