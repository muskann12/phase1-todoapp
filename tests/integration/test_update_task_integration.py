import subprocess
import sys
from src.services.task_service import create_task, clear_tasks, update_task as service_update_task
from src.models.task import TaskStatus


def test_update_title_in_process():
    """Test updating task title (in-process test for Phase I)"""
    clear_tasks()
    task = create_task("Original title", "Description")

    # Update via service layer
    updated = service_update_task(task.id, title="New title")

    assert updated.title == "New title"
    assert updated.description == "Description"

    clear_tasks()


def test_update_help():
    """Test that --help displays usage information"""
    result = subprocess.run(
        [sys.executable, '-m', 'src.main', 'update', '--help'],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert 'usage:' in result.stdout
    assert 'task_id' in result.stdout
    assert '--title' in result.stdout


def test_update_description_in_process():
    """Test updating task description (in-process test for Phase I)"""
    clear_tasks()
    task = create_task("Title", "Original description")

    # Update via service layer
    updated = service_update_task(task.id, description="New description")

    assert updated.title == "Title"
    assert updated.description == "New description"

    clear_tasks()


def test_update_both_title_and_description_in_process():
    """Test updating both title and description simultaneously (in-process test for Phase I)"""
    clear_tasks()
    task = create_task("Original title", "Original description")

    # Update via service layer
    updated = service_update_task(task.id, title="New title", description="New description")

    assert updated.title == "New title"
    assert updated.description == "New description"

    clear_tasks()


def test_update_with_unicode_characters():
    """Test updating task with Unicode characters"""
    clear_tasks()
    task = create_task("Café ☕", "Original description")

    # Update with Unicode characters
    updated = service_update_task(task.id, title="日本語", description="Emoji 🎉 test")

    assert updated.title == "日本語"
    assert updated.description == "Emoji 🎉 test"

    clear_tasks()
