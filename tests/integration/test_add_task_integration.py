import subprocess
import sys


def test_add_task_title_only_success():
    """Test adding a task with title only via CLI"""
    result = subprocess.run(
        [sys.executable, '-m', 'src.main', 'add', 'Buy groceries'],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert "Task created successfully!" in result.stdout
    assert "Title: Buy groceries" in result.stdout
    assert "Description: (none)" in result.stdout
    assert "Status: Incomplete" in result.stdout


def test_add_task_with_description_success():
    """Test adding a task with title and description via CLI"""
    result = subprocess.run(
        [sys.executable, '-m', 'src.main', 'add', 'Prepare presentation',
         '--description', 'Include Q4 metrics'],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert "Title: Prepare presentation" in result.stdout
    assert "Description: Include Q4 metrics" in result.stdout


def test_add_task_empty_title_error():
    """Test that empty title produces error"""
    result = subprocess.run(
        [sys.executable, '-m', 'src.main', 'add', '   '],
        capture_output=True,
        text=True
    )

    assert result.returncode == 1
    assert "Error: Title cannot be empty" in result.stderr


def test_add_task_help():
    """Test that --help displays usage information"""
    result = subprocess.run(
        [sys.executable, '-m', 'src.main', 'add', '--help'],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert "usage:" in result.stdout
    assert "Task title" in result.stdout
