"""Integration tests for incomplete command."""

import subprocess
import sys
from io import StringIO
from unittest.mock import patch
import pytest
from src.services.task_service import create_task, clear_tasks, mark_complete


def setup_function():
    """Clear storage before each test"""
    clear_tasks()


def test_incomplete_task_in_process():
    """Test incomplete command success in-process."""
    from src.cli.incomplete_task import incomplete_task_command

    # Setup: Create complete task
    clear_tasks()
    task = create_task("Review document", "")
    task = mark_complete(task.id)
    task_id = task.id

    # Execute: Run incomplete command in-process
    with patch("sys.argv", ["incomplete", task_id]):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            with patch("sys.exit") as mock_exit:
                incomplete_task_command([task_id])

    # Verify: Success message and exit code 0
    output = mock_stdout.getvalue()
    assert "Task marked as incomplete!" in output
    assert task_id in output
    assert "Status: Incomplete" in output
    mock_exit.assert_called_once_with(0)


def test_incomplete_help():
    """Test incomplete command help text."""
    # Execute: Run incomplete --help
    result = subprocess.run(
        ["python", "-m", "src.main", "incomplete", "--help"],
        capture_output=True,
        text=True
    )

    # Verify: Help text displays
    assert result.returncode == 0
    assert "Mark a task as incomplete" in result.stdout
    assert "task_id" in result.stdout


def test_incomplete_nonexistent_task():
    """Test incomplete command with non-existent task ID."""
    # Execute: Run incomplete with invalid ID
    result = subprocess.run(
        ["python", "-m", "src.main", "incomplete", "non-existent-id"],
        capture_output=True,
        text=True
    )

    # Verify: Error message and exit code 1
    assert result.returncode == 1
    assert "Error: Task not found with ID: non-existent-id" in result.stderr


def test_incomplete_missing_task_id():
    """Test incomplete command with missing task ID argument."""
    # Execute: Run incomplete without task ID
    result = subprocess.run(
        ["python", "-m", "src.main", "incomplete"],
        capture_output=True,
        text=True
    )

    # Verify: argparse error and exit code 2
    assert result.returncode == 2
    assert "required: task_id" in result.stderr
