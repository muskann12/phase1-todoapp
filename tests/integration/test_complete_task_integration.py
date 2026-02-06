"""Integration tests for complete command."""

import subprocess
import sys
from io import StringIO
from unittest.mock import patch
import pytest
from src.services.task_service import create_task, clear_tasks


def setup_function():
    """Clear storage before each test"""
    clear_tasks()


def test_complete_task_in_process():
    """Test complete command success in-process."""
    from src.cli.complete_task import complete_task_command

    # Setup: Create incomplete task
    clear_tasks()
    task = create_task("Buy milk", "")
    task_id = task.id

    # Execute: Run complete command in-process
    with patch("sys.argv", ["complete", task_id]):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            with patch("sys.exit") as mock_exit:
                complete_task_command([task_id])

    # Verify: Success message and exit code 0
    output = mock_stdout.getvalue()
    assert "Task marked as complete!" in output
    assert task_id in output
    assert "Status: Complete" in output
    mock_exit.assert_called_once_with(0)


def test_complete_help():
    """Test complete command help text."""
    # Execute: Run complete --help
    result = subprocess.run(
        ["python", "-m", "src.main", "complete", "--help"],
        capture_output=True,
        text=True
    )

    # Verify: Help text displays
    assert result.returncode == 0
    assert "Mark a task as complete" in result.stdout
    assert "task_id" in result.stdout


def test_complete_nonexistent_task():
    """Test complete command with non-existent task ID."""
    # Execute: Run complete with invalid ID
    result = subprocess.run(
        ["python", "-m", "src.main", "complete", "non-existent-id"],
        capture_output=True,
        text=True
    )

    # Verify: Error message and exit code 1
    assert result.returncode == 1
    assert "Error: Task not found with ID: non-existent-id" in result.stderr


def test_complete_missing_task_id():
    """Test complete command with missing task ID argument."""
    # Execute: Run complete without task ID
    result = subprocess.run(
        ["python", "-m", "src.main", "complete"],
        capture_output=True,
        text=True
    )

    # Verify: argparse error and exit code 2
    assert result.returncode == 2
    assert "required: task_id" in result.stderr
