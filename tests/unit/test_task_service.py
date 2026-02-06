import pytest
from src.services.task_service import create_task, get_task, get_all_tasks, clear_tasks, generate_task_id, update_task, delete_task
from src.models.task import TaskStatus


def setup_function():
    """Clear storage before each test"""
    clear_tasks()


def test_create_task_with_title():
    """Test creating a task with title only"""
    task = create_task("Buy milk")

    assert task.title == "Buy milk"
    assert task.description == ""
    assert task.status == TaskStatus.INCOMPLETE
    assert task.id is not None


def test_create_task_with_description():
    """Test creating a task with title and description"""
    task = create_task("Buy milk", "From the store")

    assert task.title == "Buy milk"
    assert task.description == "From the store"


def test_task_id_uniqueness():
    """Test that created tasks have unique IDs"""
    task1 = create_task("Task 1")
    task2 = create_task("Task 2")

    assert task1.id != task2.id


def test_get_task_by_id():
    """Test retrieving a task by ID"""
    task = create_task("Buy milk")
    retrieved = get_task(task.id)

    assert retrieved.id == task.id
    assert retrieved.title == task.title


def test_get_nonexistent_task_raises_error():
    """Test that getting nonexistent task raises KeyError"""
    with pytest.raises(KeyError):
        get_task("nonexistent-id")


def test_create_task_with_empty_title_raises_error():
    """Test that empty title raises ValueError"""
    with pytest.raises(ValueError, match="Title cannot be empty"):
        create_task("")


def test_create_task_with_long_title_raises_error():
    """Test that title over 500 chars raises ValueError"""
    with pytest.raises(ValueError, match="Title cannot exceed 500 characters"):
        create_task("a" * 501)


def test_get_all_tasks():
    """Test retrieving all tasks"""
    task1 = create_task("Task 1")
    task2 = create_task("Task 2")

    all_tasks = get_all_tasks()

    assert len(all_tasks) == 2
    assert task1 in all_tasks
    assert task2 in all_tasks


def test_clear_tasks():
    """Test clearing all tasks"""
    create_task("Task 1")
    create_task("Task 2")

    clear_tasks()

    assert len(get_all_tasks()) == 0


# Tests for View Task List feature (User Story 1)

def test_get_all_tasks_empty():
    """Test retrieving tasks when none exist"""
    clear_tasks()  # Ensure clean state
    tasks = get_all_tasks()
    assert tasks == []
    assert len(tasks) == 0


def test_get_all_tasks_returns_sorted_by_id():
    """Test that tasks are sorted by ID in ascending order"""
    clear_tasks()

    # Create tasks (IDs will be generated sequentially)
    task1 = create_task("First task")
    task2 = create_task("Second task")
    task3 = create_task("Third task")

    tasks = get_all_tasks()

    assert len(tasks) == 3
    # Verify ascending ID order (each task ID is less than the next)
    assert tasks[0].id < tasks[1].id < tasks[2].id
    # Verify all created tasks are in the list
    task_titles = {t.title for t in tasks}
    assert task_titles == {"First task", "Second task", "Third task"}


def test_get_all_tasks_does_not_modify_storage():
    """Test that get_all_tasks is read-only (no side effects)"""
    clear_tasks()

    task1 = create_task("Task 1")
    task2 = create_task("Task 2")

    # Get tasks twice
    tasks_before = get_all_tasks()
    tasks_after = get_all_tasks()

    # Verify same results (deterministic)
    assert len(tasks_before) == len(tasks_after)
    assert tasks_before[0].id == tasks_after[0].id
    assert tasks_before[1].id == tasks_after[1].id


# Tests for Update Task feature - User Story 1

def test_update_task_title_only():
    """Test updating only the title"""
    clear_tasks()
    task = create_task("Original title", "Original description")

    updated = update_task(task.id, title="New title")

    assert updated.title == "New title"
    assert updated.description == "Original description"
    assert updated.id == task.id
    assert updated.created == task.created
    assert updated.status == TaskStatus.INCOMPLETE


def test_update_task_preserves_description():
    """Test that updating title preserves description"""
    clear_tasks()
    task = create_task("Title", "Important description")

    updated = update_task(task.id, title="New title")

    assert updated.title == "New title"
    assert updated.description == "Important description"


def test_update_task_nonexistent_id_raises_keyerror():
    """Test updating non-existent task raises KeyError"""
    clear_tasks()

    with pytest.raises(KeyError, match="Task not found with ID"):
        update_task("nonexistent-id", title="New title")


def test_update_task_empty_title_raises_valueerror():
    """Test empty title raises ValueError"""
    clear_tasks()
    task = create_task("Original title")

    with pytest.raises(ValueError, match="Title cannot be empty"):
        update_task(task.id, title="")


def test_update_task_title_too_long_raises_valueerror():
    """Test title over 500 chars raises ValueError"""
    clear_tasks()
    task = create_task("Original title")

    with pytest.raises(ValueError, match="Title cannot exceed 500 characters"):
        update_task(task.id, title="a" * 501)


# Tests for Update Task feature - User Story 2

def test_update_task_description_only():
    """Test updating only the description"""
    clear_tasks()
    task = create_task("Original title", "Original description")

    updated = update_task(task.id, description="New description")

    assert updated.title == "Original title"
    assert updated.description == "New description"
    assert updated.id == task.id
    assert updated.created == task.created
    assert updated.status == TaskStatus.INCOMPLETE


def test_update_task_preserves_title():
    """Test that updating description preserves title"""
    clear_tasks()
    task = create_task("Important title", "Description")

    updated = update_task(task.id, description="New description")

    assert updated.title == "Important title"
    assert updated.description == "New description"


def test_update_task_empty_description_allowed():
    """Test that empty description is allowed (clearing description)"""
    clear_tasks()
    task = create_task("Title", "Original description")

    updated = update_task(task.id, description="")

    assert updated.title == "Title"
    assert updated.description == ""


def test_update_task_description_too_long_raises_valueerror():
    """Test description over 5000 chars raises ValueError"""
    clear_tasks()
    task = create_task("Title", "Original description")

    with pytest.raises(ValueError, match="Description cannot exceed 5000 characters"):
        update_task(task.id, description="a" * 5001)


# Tests for Update Task feature - User Story 3

def test_update_task_both_title_and_description():
    """Test updating both title and description simultaneously"""
    clear_tasks()
    task = create_task("Original title", "Original description")

    updated = update_task(task.id, title="New title", description="New description")

    assert updated.title == "New title"
    assert updated.description == "New description"
    assert updated.id == task.id
    assert updated.created == task.created
    assert updated.status == TaskStatus.INCOMPLETE


def test_update_task_no_updates_raises_valueerror():
    """Test that providing neither title nor description raises ValueError"""
    clear_tasks()
    task = create_task("Title", "Description")

    with pytest.raises(ValueError, match="No updates provided"):
        update_task(task.id)


def test_update_task_preserves_immutable_fields():
    """Test that id, created, and status are preserved during update"""
    clear_tasks()
    task = create_task("Original title", "Original description")
    original_id = task.id
    original_created = task.created
    original_status = task.status

    updated = update_task(task.id, title="New title", description="New description")

    assert updated.id == original_id
    assert updated.created == original_created
    assert updated.status == original_status


# Tests for Delete Task feature - User Story 1

def test_delete_task_returns_deleted_task():
    """Test that delete_task() returns the deleted Task object"""
    clear_tasks()
    task = create_task("Buy milk", "Get organic milk")

    deleted = delete_task(task.id)

    assert deleted.id == task.id
    assert deleted.title == "Buy milk"
    assert deleted.description == "Get organic milk"
    assert deleted.status == TaskStatus.INCOMPLETE


def test_delete_task_removes_from_storage():
    """Test that deleted task is removed from storage"""
    clear_tasks()
    task = create_task("Buy milk")

    delete_task(task.id)

    # Verify task no longer exists
    with pytest.raises(KeyError):
        get_task(task.id)


def test_delete_task_nonexistent_id_raises_keyerror():
    """Test that deleting non-existent task raises KeyError"""
    clear_tasks()

    with pytest.raises(KeyError, match="Task not found with ID"):
        delete_task("nonexistent-id")


def test_delete_task_works_for_any_status():
    """Test that delete works regardless of task status"""
    clear_tasks()
    task1 = create_task("Incomplete task")
    task2 = create_task("Complete task")
    # Note: Status update functionality doesn't exist yet,
    # but this test verifies deletion doesn't check status

    deleted1 = delete_task(task1.id)
    deleted2 = delete_task(task2.id)

    assert deleted1.status == TaskStatus.INCOMPLETE
    assert deleted2.status == TaskStatus.INCOMPLETE


def test_delete_task_with_unicode():
    """Test deleting task with Unicode characters"""
    clear_tasks()
    task = create_task("Café ☕", "日本語 🎉")

    deleted = delete_task(task.id)

    assert deleted.title == "Café ☕"
    assert deleted.description == "日本語 🎉"


def test_delete_task_only_removes_specified_task():
    """Test that delete only removes the specified task, not others"""
    clear_tasks()
    task1 = create_task("Task 1")
    task2 = create_task("Task 2")
    task3 = create_task("Task 3")

    delete_task(task2.id)

    # Verify task1 and task3 still exist
    assert get_task(task1.id).title == "Task 1"
    assert get_task(task3.id).title == "Task 3"

    # Verify task2 is gone
    with pytest.raises(KeyError):
        get_task(task2.id)


# Tests for Toggle Task Status feature - User Story 1: Mark Complete

def test_mark_complete_returns_completed_task():
    """Test that mark_complete returns task with COMPLETE status."""
    # Import will be added after function implementation
    from src.services.task_service import mark_complete

    # Setup: Create incomplete task
    clear_tasks()
    task = create_task("Buy milk", "")
    task_id = task.id

    # Execute: Mark as complete
    result = mark_complete(task_id)

    # Verify: Task status is COMPLETE
    assert result.status == TaskStatus.COMPLETE
    assert result.id == task_id
    assert result.title == "Buy milk"


def test_mark_complete_updates_storage():
    """Test that mark_complete updates task in storage dict."""
    from src.services.task_service import mark_complete

    # Setup: Create incomplete task
    clear_tasks()
    task = create_task("Buy milk", "")
    task_id = task.id

    # Execute: Mark as complete
    mark_complete(task_id)

    # Verify: Task in storage has COMPLETE status (via get_task)
    updated_task = get_task(task_id)
    assert updated_task.status == TaskStatus.COMPLETE


def test_mark_complete_nonexistent_id_raises_keyerror():
    """Test that mark_complete raises KeyError for non-existent ID."""
    from src.services.task_service import mark_complete

    # Setup: Non-existent ID
    clear_tasks()
    task_id = "non-existent-id"

    # Execute & Verify: Raises KeyError
    with pytest.raises(KeyError):
        mark_complete(task_id)


def test_mark_complete_idempotent():
    """Test that marking complete task as complete is idempotent."""
    from src.services.task_service import mark_complete

    # Setup: Create complete task
    clear_tasks()
    task = create_task("Buy milk", "")
    task = mark_complete(task.id)
    assert task.status == TaskStatus.COMPLETE

    # Execute: Mark as complete again
    result = mark_complete(task.id)

    # Verify: Still COMPLETE, no error
    assert result.status == TaskStatus.COMPLETE
    assert result.id == task.id


# Tests for Toggle Task Status feature - User Story 2: Mark Incomplete

def test_mark_incomplete_returns_incomplete_task():
    """Test that mark_incomplete returns task with INCOMPLETE status."""
    from src.services.task_service import mark_incomplete, mark_complete

    # Setup: Create complete task
    clear_tasks()
    task = create_task("Review document", "")
    task = mark_complete(task.id)

    # Execute: Mark as incomplete
    result = mark_incomplete(task.id)

    # Verify: Task status is INCOMPLETE
    assert result.status == TaskStatus.INCOMPLETE
    assert result.id == task.id


def test_mark_incomplete_updates_storage():
    """Test that mark_incomplete updates task in storage dict."""
    from src.services.task_service import mark_incomplete, mark_complete

    # Setup: Create complete task
    clear_tasks()
    task = create_task("Review document", "")
    task = mark_complete(task.id)

    # Execute: Mark as incomplete
    mark_incomplete(task.id)

    # Verify: Task in storage has INCOMPLETE status (via get_task)
    updated_task = get_task(task.id)
    assert updated_task.status == TaskStatus.INCOMPLETE


def test_mark_incomplete_nonexistent_id_raises_keyerror():
    """Test that mark_incomplete raises KeyError for non-existent ID."""
    from src.services.task_service import mark_incomplete

    clear_tasks()
    with pytest.raises(KeyError):
        mark_incomplete("non-existent-id")


def test_mark_incomplete_idempotent():
    """Test that marking incomplete task as incomplete is idempotent."""
    from src.services.task_service import mark_incomplete

    # Setup: Create incomplete task
    clear_tasks()
    task = create_task("Review document", "")
    assert task.status == TaskStatus.INCOMPLETE

    # Execute: Mark as incomplete again
    result = mark_incomplete(task.id)

    # Verify: Still INCOMPLETE, no error
    assert result.status == TaskStatus.INCOMPLETE


# Tests for Toggle Task Status feature - User Story 3: Toggle Status

def test_toggle_status_incomplete_to_complete():
    """Test that toggle flips INCOMPLETE to COMPLETE."""
    from src.services.task_service import toggle_status

    # Setup: Create incomplete task
    clear_tasks()
    task = create_task("Buy milk", "")
    assert task.status == TaskStatus.INCOMPLETE

    # Execute: Toggle status
    result = toggle_status(task.id)

    # Verify: Status is now COMPLETE
    assert result.status == TaskStatus.COMPLETE


def test_toggle_status_complete_to_incomplete():
    """Test that toggle flips COMPLETE to INCOMPLETE."""
    from src.services.task_service import toggle_status, mark_complete

    # Setup: Create complete task
    clear_tasks()
    task = create_task("Buy milk", "")
    task = mark_complete(task.id)
    assert task.status == TaskStatus.COMPLETE

    # Execute: Toggle status
    result = toggle_status(task.id)

    # Verify: Status is now INCOMPLETE
    assert result.status == TaskStatus.INCOMPLETE


def test_toggle_status_nonexistent_id_raises_keyerror():
    """Test that toggle_status raises KeyError for non-existent ID."""
    from src.services.task_service import toggle_status

    clear_tasks()
    with pytest.raises(KeyError):
        toggle_status("non-existent-id")
