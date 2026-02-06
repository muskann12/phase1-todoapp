import subprocess
import sys
from src.services.task_service import create_task, clear_tasks, delete_task as service_delete_task
from src.models.task import TaskStatus


def test_delete_task_in_process():
    """Test delete task success message (in-process test for Phase I)"""
    clear_tasks()
    task = create_task("Buy milk", "Get organic milk")

    # Delete via service layer (in-process test)
    deleted = service_delete_task(task.id)

    assert deleted.title == "Buy milk"
    assert deleted.description == "Get organic milk"

    # Verify task is removed
    from src.services.task_service import get_task
    import pytest
    with pytest.raises(KeyError):
        get_task(task.id)

    clear_tasks()


def test_delete_help():
    """Test that --help displays usage information"""
    result = subprocess.run(
        [sys.executable, '-m', 'src.main', 'delete', '--help'],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert 'usage:' in result.stdout
    assert 'task_id' in result.stdout
    assert 'Delete an existing task' in result.stdout


def test_delete_nonexistent_task():
    """Test delete with non-existent task ID shows error"""
    clear_tasks()

    result = subprocess.run(
        [sys.executable, '-m', 'src.main', 'delete', 'nonexistent-id'],
        capture_output=True,
        text=True
    )

    assert result.returncode == 1
    assert 'Error: Task not found with ID: nonexistent-id' in result.stderr


def test_delete_missing_task_id():
    """Test delete without task ID shows argparse error"""
    result = subprocess.run(
        [sys.executable, '-m', 'src.main', 'delete'],
        capture_output=True,
        text=True
    )

    assert result.returncode == 2
    assert 'required: task_id' in result.stderr
