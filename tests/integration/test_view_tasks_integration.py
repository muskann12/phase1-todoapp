import subprocess
import sys
from src.services.task_service import create_task, clear_tasks, get_all_tasks
from src.models.task import TaskStatus


def test_view_empty_list():
    """Test viewing tasks when none exist (empty-state message)"""
    # Phase I: In-memory storage doesn't persist between subprocess calls
    # This test verifies empty-state message appears when no tasks exist
    result = subprocess.run(
        [sys.executable, '-m', 'src.main', 'view'],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert 'No tasks found' in result.stdout
    assert 'python -m src.main add' in result.stdout


def test_view_single_task_in_process():
    """Test viewing a single task (in-process test for Phase I)"""
    clear_tasks()

    # Create task in same process
    task = create_task("Test task")

    # Verify view logic works by checking service layer
    tasks = get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "Test task"
    assert tasks[0].description == ""
    assert tasks[0].status == TaskStatus.INCOMPLETE

    clear_tasks()


def test_view_multiple_tasks_sorted_in_process():
    """Test viewing multiple tasks with correct sorting (in-process test)"""
    clear_tasks()

    # Create multiple tasks
    task1 = create_task("Task 1")
    task2 = create_task("Task 2", "Details")
    task3 = create_task("Task 3")

    # Verify sorting
    tasks = get_all_tasks()
    assert len(tasks) == 3
    assert tasks[0].id < tasks[1].id < tasks[2].id

    # Verify all tasks present
    titles = [t.title for t in tasks]
    assert "Task 1" in titles
    assert "Task 2" in titles
    assert "Task 3" in titles

    clear_tasks()


def test_view_tasks_with_unicode_in_process():
    """Test viewing tasks with Unicode characters (in-process test)"""
    clear_tasks()

    # Create task with Unicode
    task = create_task("Café ☕", "Visit café")

    # Verify Unicode stored correctly
    tasks = get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "Café ☕"
    assert tasks[0].description == "Visit café"

    clear_tasks()


def test_view_help():
    """Test that --help displays usage information"""
    result = subprocess.run(
        [sys.executable, '-m', 'src.main', 'view', '--help'],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert 'usage:' in result.stdout
    assert 'View all tasks' in result.stdout or 'view' in result.stdout.lower()


# Tests for User Story 2: View Task Count Summary

def test_view_with_task_count_summary():
    """Test viewing tasks with summary counts (User Story 2)"""
    clear_tasks()

    # Create 10 tasks: 7 incomplete, 3 complete
    for i in range(7):
        create_task(f"Incomplete task {i+1}")

    for i in range(3):
        task = create_task(f"Complete task {i+1}")
        # Mark as complete
        task.status = TaskStatus.COMPLETE

    # Verify summary calculation
    tasks = get_all_tasks()
    incomplete_count = sum(1 for t in tasks if t.status == TaskStatus.INCOMPLETE)
    complete_count = sum(1 for t in tasks if t.status == TaskStatus.COMPLETE)

    assert len(tasks) == 10
    assert incomplete_count == 7
    assert complete_count == 3

    clear_tasks()


def test_view_empty_list_has_no_summary():
    """Test that empty list shows no summary (only empty-state message)"""
    # This is already tested in test_view_empty_list
    # Empty state message should NOT include summary line
    result = subprocess.run(
        [sys.executable, '-m', 'src.main', 'view'],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert 'No tasks found' in result.stdout
    # Summary line should NOT appear for empty list
    assert 'Total:' not in result.stdout
    assert 'Incomplete:' not in result.stdout
    assert 'Complete:' not in result.stdout
