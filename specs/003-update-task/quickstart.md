# Quickstart: Update Task Implementation

**Feature**: 003-update-task
**Date**: 2025-12-31
**Audience**: Developers implementing this feature

## Overview

This quickstart guide provides a step-by-step implementation roadmap for the Update Task feature. Follow the Test-First Development (RED-GREEN-REFACTOR) workflow as mandated by the Constitution.

---

## Prerequisites

Before starting implementation:

1. ✅ **Specification approved**: `specs/003-update-task/spec.md`
2. ✅ **Plan approved**: `specs/003-update-task/plan.md`
3. ✅ **Existing features implemented**:
   - Add Task (001-add-task) - provides Task model and create_task()
   - View Task List (002-view-task-list) - for verifying updates

4. ✅ **Environment setup**:
   - Python 3.13+ installed
   - pytest installed (`pip install pytest pytest-cov`)
   - Project repository cloned, branch `003-update-task` checked out

---

## Implementation Steps

### Step 1: Add Service Layer Function

**File**: `src/services/task_service.py`

**Add** `update_task()` function below `get_all_tasks()`:

```python
def update_task(task_id: str, title: str | None = None, description: str | None = None) -> Task:
    """
    Update an existing task's title and/or description.

    Args:
        task_id: The task's unique identifier
        title: New title (None = unchanged)
        description: New description (None = unchanged)

    Returns:
        Task: The updated task object

    Raises:
        KeyError: If task ID not found
        ValueError: If no updates provided or validation fails
    """
    # Validate task exists
    if task_id not in _tasks:
        raise KeyError(f"Task not found with ID: {task_id}")

    # Validate at least one update provided
    if title is None and description is None:
        raise ValueError("No updates provided. Use title and/or description parameters")

    # Get existing task
    existing_task = _tasks[task_id]

    # Determine new values (preserve if None)
    new_title = title if title is not None else existing_task.title
    new_description = description if description is not None else existing_task.description

    # Create updated task (triggers validation in __post_init__)
    updated_task = Task(
        id=existing_task.id,           # Preserve (immutable)
        title=new_title,               # New or existing
        description=new_description,   # New or existing
        status=existing_task.status,   # Preserve (not updated here)
        created=existing_task.created  # Preserve (immutable)
    )

    # Replace in storage
    _tasks[task_id] = updated_task

    return updated_task
```

---

### Step 2: Write Unit Tests (RED Phase)

**File**: `tests/unit/test_task_service.py`

**Add** tests for `update_task()` at the end of the file:

```python
# Tests for Update Task feature

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


def test_update_task_description_only():
    """Test updating only the description"""
    clear_tasks()
    task = create_task("Title", "Original description")

    updated = update_task(task.id, description="New description")

    assert updated.title == "Title"
    assert updated.description == "New description"
    assert updated.id == task.id


def test_update_task_both_fields():
    """Test updating both title and description"""
    clear_tasks()
    task = create_task("Old title", "Old description")

    updated = update_task(task.id, title="New title", description="New description")

    assert updated.title == "New title"
    assert updated.description == "New description"


def test_update_task_clear_description():
    """Test clearing description with empty string"""
    clear_tasks()
    task = create_task("Title", "Has description")

    updated = update_task(task.id, description="")

    assert updated.description == ""


def test_update_task_nonexistent_id():
    """Test updating non-existent task raises KeyError"""
    clear_tasks()

    with pytest.raises(KeyError):
        update_task("nonexistent-id", title="New title")


def test_update_task_no_updates_provided():
    """Test error when neither title nor description provided"""
    clear_tasks()
    task = create_task("Title")

    with pytest.raises(ValueError, match="No updates provided"):
        update_task(task.id)


def test_update_task_empty_title():
    """Test empty title raises ValueError"""
    clear_tasks()
    task = create_task("Original title")

    with pytest.raises(ValueError, match="Title cannot be empty"):
        update_task(task.id, title="")


def test_update_task_title_too_long():
    """Test title over 500 chars raises ValueError"""
    clear_tasks()
    task = create_task("Original title")

    with pytest.raises(ValueError, match="Title cannot exceed 500 characters"):
        update_task(task.id, title="a" * 501)


def test_update_task_description_too_long():
    """Test description over 2000 chars raises ValueError"""
    clear_tasks()
    task = create_task("Title")

    with pytest.raises(ValueError, match="Description cannot exceed 2000 characters"):
        update_task(task.id, description="a" * 2001)


def test_update_task_preserves_status():
    """Test that updating task preserves status field"""
    clear_tasks()
    task = create_task("Title")
    task.status = TaskStatus.COMPLETE  # Manually set to complete
    _tasks[task.id] = task  # Update storage

    updated = update_task(task.id, title="New title")

    assert updated.status == TaskStatus.COMPLETE  # Status preserved
```

**Run tests** → Verify RED phase (tests should fail - update_task doesn't exist yet):

```bash
pytest tests/unit/test_task_service.py -v
```

Expected: All new tests FAIL (update_task not defined)

---

### Step 3: Implement Service Function (GREEN Phase)

Implement `update_task()` function as shown in Step 1 above.

**Run tests** → Verify GREEN phase:

```bash
pytest tests/unit/test_task_service.py -v
```

Expected: All tests PASS

---

### Step 4: Create CLI Command File

**File**: `src/cli/update_task.py` (new file)

```python
import argparse
import sys

from src.services.task_service import update_task


def update_task_command(args: list[str] = None):
    """
    CLI command to update an existing task's title and/or description.

    Args:
        args: Command-line arguments (None = use sys.argv)

    Exit Codes:
        0: Success (task updated)
        1: Error (task not found, validation failed, no updates)
        2: Usage error (argparse validation failed)
    """
    parser = argparse.ArgumentParser(
        description="Update an existing task's title and/or description",
        prog='todo update'
    )

    # Positional argument
    parser.add_argument(
        'task_id',
        type=str,
        help='Unique task identifier (UUID)'
    )

    # Optional flags
    parser.add_argument(
        '--title',
        type=str,
        default=None,
        help='New task title (1-500 characters)'
    )

    parser.add_argument(
        '--description',
        type=str,
        default=None,
        help='New task description (0-2000 characters, optional)'
    )

    # Parse arguments
    parsed_args = parser.parse_args(args)

    # Validate at least one update provided
    if parsed_args.title is None and parsed_args.description is None:
        print("Error: No updates provided. Use --title and/or --description", file=sys.stderr)
        sys.exit(1)

    # Call service layer
    try:
        updated_task = update_task(
            task_id=parsed_args.task_id,
            title=parsed_args.title,
            description=parsed_args.description
        )

        # Display success message
        print("Task updated successfully!")
        print(f"ID: {updated_task.id}")
        print(f"Title: {updated_task.title}")
        print(f"Description: {updated_task.description if updated_task.description else '(none)'}")
        print(f"Status: {updated_task.status.value.capitalize()}")

        sys.exit(0)

    except KeyError:
        print(f"Error: Task not found with ID: {parsed_args.task_id}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    update_task_command()
```

---

### Step 5: Update Main Router

**File**: `src/main.py`

**Update** the `main()` function to add "update" command routing:

```python
def main():
    """Main entry point for the todo CLI application"""
    if len(sys.argv) < 2:
        print("Usage: python -m src.main <command> [args]", file=sys.stderr)
        print("Commands: add, view, update", file=sys.stderr)  # Add "update"
        sys.exit(1)

    command = sys.argv[1]

    if command == 'add':
        from src.cli.add_task import add_task_command
        add_task_command(sys.argv[2:])
    elif command == 'view':
        from src.cli.view_tasks import view_tasks_command
        view_tasks_command(sys.argv[2:])
    elif command == 'update':  # NEW
        from src.cli.update_task import update_task_command
        update_task_command(sys.argv[2:])
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        print("Available commands: add, view, update", file=sys.stderr)  # Add "update"
        sys.exit(1)
```

---

### Step 6: Write Integration Tests

**File**: `tests/integration/test_update_task_integration.py` (new file)

```python
import subprocess
import sys
from src.services.task_service import create_task, clear_tasks, update_task as service_update_task
from src.models.task import TaskStatus


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
    assert '--description' in result.stdout


def test_update_task_title_in_process():
    """Test updating task title (in-process test for Phase I)"""
    clear_tasks()
    task = create_task("Original title", "Description")

    # Update via service layer
    updated = service_update_task(task.id, title="New title")

    assert updated.title == "New title"
    assert updated.description == "Description"

    clear_tasks()


def test_update_task_description_in_process():
    """Test updating task description (in-process test)"""
    clear_tasks()
    task = create_task("Title", "Original description")

    # Update via service layer
    updated = service_update_task(task.id, description="New description")

    assert updated.title == "Title"
    assert updated.description == "New description"

    clear_tasks()


def test_update_task_both_fields_in_process():
    """Test updating both title and description"""
    clear_tasks()
    task = create_task("Old title", "Old description")

    # Update via service layer
    updated = service_update_task(task.id, title="New title", description="New description")

    assert updated.title == "New title"
    assert updated.description == "New description"

    clear_tasks()


def test_update_task_unicode_in_process():
    """Test updating with Unicode characters"""
    clear_tasks()
    task = create_task("Title", "Description")

    # Update with Unicode
    updated = service_update_task(task.id, title="Café ☕", description="日本語")

    assert updated.title == "Café ☕"
    assert updated.description == "日本語"

    clear_tasks()


def test_update_task_preserves_immutable_fields():
    """Test that update preserves ID, created, and status"""
    clear_tasks()
    task = create_task("Title", "Description")
    original_id = task.id
    original_created = task.created

    # Manually set status to COMPLETE
    task.status = TaskStatus.COMPLETE
    from src.services.task_service import _tasks
    _tasks[task.id] = task

    # Update task
    updated = service_update_task(task.id, title="New title")

    assert updated.id == original_id
    assert updated.created == original_created
    assert updated.status == TaskStatus.COMPLETE

    clear_tasks()
```

**Run tests** → Verify all integration tests pass:

```bash
pytest tests/integration/test_update_task_integration.py -v
```

---

### Step 7: Manual Validation

Test the CLI directly:

```bash
# Create a task
python -m src.main add "Buy milk"

# View to get task ID
python -m src.main view
# Copy the task ID from output

# Update title
python -m src.main update <TASK_ID> --title "Buy organic milk"

# Update description
python -m src.main update <TASK_ID> --description "Get from Trader Joe's"

# Update both
python -m src.main update <TASK_ID> --title "Buy almond milk" --description "Unsweetened"

# Test errors
python -m src.main update nonexistent-id --title "Test"  # Should error
python -m src.main update <TASK_ID>  # Should error (no updates)
python -m src.main update <TASK_ID> --title ""  # Should error (empty title)

# Test help
python -m src.main update --help
```

---

### Step 8: Run Full Test Suite

```bash
# Run all tests with coverage
pytest --cov=src tests/

# Verify coverage for update_task feature
# Expected: 100% coverage for src/services/task_service.py
```

---

## File Checklist

After implementation, verify these files exist:

- ✅ `src/services/task_service.py` - contains `update_task()` function
- ✅ `src/cli/update_task.py` - contains `update_task_command()` function
- ✅ `src/main.py` - updated with "update" command routing
- ✅ `tests/unit/test_task_service.py` - contains ~10 unit tests for update_task()
- ✅ `tests/integration/test_update_task_integration.py` - contains ~6 integration tests

---

## Success Criteria Verification

After implementation, verify all success criteria from spec.md:

- ✅ **SC-001**: Users can update task title in single command using task ID
- ✅ **SC-002**: Users can update task description in single command using task ID
- ✅ **SC-003**: Users can update both title and description simultaneously
- ✅ **SC-004**: System provides clear error messages for all failure scenarios
- ✅ **SC-005**: Task status and created timestamp remain unchanged after updates
- ✅ **SC-006**: Updated task information immediately reflected in View Task List
- ✅ **SC-007**: Users can clear task description by updating to empty string
- ✅ **SC-008**: Unicode characters correctly stored and displayed
- ✅ **SC-009**: Command help documentation clearly explains usage and provides examples

---

## Troubleshooting

### Tests fail with "ModuleNotFoundError"
→ Ensure you're running tests from repository root, not tests/ directory

### Tests fail with "update_task not found"
→ Check import in test file: `from src.services.task_service import update_task`

### Integration tests fail with "Task not found"
→ In-memory storage doesn't persist between subprocess calls - use in-process testing pattern

### Unicode tests fail
→ Verify Python 3.13+ is being used (UTF-8 default encoding)

---

## Next Steps

After implementation complete:

1. Run `/sp.tasks` to generate task decomposition
2. Run `/sp.implement` to execute implementation via Claude Code
3. Create commit with message following project convention
4. Create pull request for code review
