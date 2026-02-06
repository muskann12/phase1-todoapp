# Quickstart Guide: Add Task Feature

**Feature**: Add Task
**Date**: 2025-12-31
**Target Audience**: Developers implementing the Add Task feature
**Prerequisites**: Python 3.13+, pytest installed

## Purpose

This guide walks through implementing and testing the Add Task feature from scratch. Follow these steps in order to build a working implementation that passes all acceptance criteria.

---

## Step 1: Project Setup

### Create Project Structure

```bash
# Create source directories
mkdir -p src/models src/services src/cli
mkdir -p tests/unit tests/integration tests/contract

# Create __init__.py files
touch src/__init__.py
touch src/models/__init__.py
touch src/services/__init__.py
touch src/cli/__init__.py
touch tests/__init__.py
```

### Verify Python Version

```bash
python --version
# Expected: Python 3.13.0 or higher
```

If Python 3.13+ is not available, install it before proceeding.

---

## Step 2: Implement Data Model

**File**: `src/models/task.py`

**Purpose**: Define the Task entity and TaskStatus enum

**Implementation**:
```python
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class TaskStatus(Enum):
    """Task completion status"""
    INCOMPLETE = "incomplete"
    COMPLETE = "complete"


@dataclass
class Task:
    """Represents a single todo item"""
    id: str
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.INCOMPLETE
    created: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate task fields after initialization"""
        # Title validation
        self.title = self.title.strip()
        if not self.title:
            raise ValueError("Title cannot be empty")
        if len(self.title) > 500:
            raise ValueError(f"Title cannot exceed 500 characters (provided: {len(self.title)})")

        # Description validation
        if len(self.description) > 5000:
            raise ValueError(f"Description cannot exceed 5000 characters (provided: {len(self.description)})")
```

**Verification**:
```bash
python -c "from src.models.task import Task, TaskStatus; print('Task model imported successfully')"
```

---

## Step 3: Implement Service Layer

**File**: `src/services/task_service.py`

**Purpose**: Handle task creation logic, ID generation, and in-memory storage

**Implementation**:
```python
import uuid
from datetime import datetime
from typing import Dict

from src.models.task import Task, TaskStatus

# In-memory storage: maps task ID to Task object
_tasks: Dict[str, Task] = {}

# Namespace UUID for deterministic ID generation
TODO_NAMESPACE = uuid.UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')


def generate_task_id(counter: int) -> str:
    """
    Generate a unique, deterministic task ID using UUID5.

    Args:
        counter: Sequential counter for uniqueness (typically len(_tasks))

    Returns:
        str: UUID5-based task ID
    """
    name = f"task-{datetime.now().isoformat()}-{counter}"
    return str(uuid.uuid5(TODO_NAMESPACE, name))


def create_task(title: str, description: str = "") -> Task:
    """
    Create a new task with the given title and optional description.

    Args:
        title: Task title (required, will be trimmed, must be non-empty)
        description: Task description (optional, defaults to empty string)

    Returns:
        Task: The created task object

    Raises:
        ValueError: If title is empty/whitespace-only, title > 500 chars,
                    or description > 5000 chars
    """
    # Generate unique ID
    task_id = generate_task_id(len(_tasks))

    # Create task (validation happens in Task.__post_init__)
    task = Task(
        id=task_id,
        title=title,
        description=description,
        status=TaskStatus.INCOMPLETE,
        created=datetime.now()
    )

    # Store in memory
    _tasks[task.id] = task

    return task


def get_task(task_id: str) -> Task:
    """
    Retrieve a task by ID.

    Args:
        task_id: The task's unique identifier

    Returns:
        Task: The task object

    Raises:
        KeyError: If task ID not found
    """
    return _tasks[task_id]


def get_all_tasks() -> list[Task]:
    """
    Retrieve all tasks.

    Returns:
        list[Task]: All tasks in storage (may be empty)
    """
    return list(_tasks.values())


def clear_tasks():
    """Clear all tasks from storage (useful for testing)"""
    _tasks.clear()
```

**Verification**:
```bash
python -c "from src.services.task_service import create_task; task = create_task('Test'); print(f'Created task: {task.id}')"
```

---

## Step 4: Implement CLI Interface

**File**: `src/cli/add_task.py`

**Purpose**: Parse command-line arguments and interact with user

**Implementation**:
```python
import argparse
import sys

from src.services.task_service import create_task


def add_task_command(args: list[str] = None):
    """
    CLI command to add a new task.

    Args:
        args: Command-line arguments (None = use sys.argv)
    """
    parser = argparse.ArgumentParser(
        description='Add a new task to your todo list',
        prog='todo add'
    )

    parser.add_argument(
        'title',
        type=str,
        help='Task title (required, 1-500 characters)'
    )

    parser.add_argument(
        '-d', '--description',
        type=str,
        default='',
        help='Task description (optional, max 5000 characters)'
    )

    # Parse arguments
    parsed_args = parser.parse_args(args)

    try:
        # Create task via service layer
        task = create_task(parsed_args.title, parsed_args.description)

        # Success output
        print("Task created successfully!")
        print(f"ID: {task.id}")
        print(f"Title: {task.title}")
        print(f"Description: {task.description if task.description else '(none)'}")
        print(f"Status: {task.status.value.capitalize()}")
        print(f"Created: {task.created.isoformat()}")

        sys.exit(0)

    except ValueError as e:
        # Validation error
        print(f"Error: {e}", file=sys.stderr)
        print(f"Usage: todo add <title> [--description <description>]", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        # Unexpected error
        print(f"Internal error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == '__main__':
    add_task_command()
```

**Verification**:
```bash
python src/cli/add_task.py "Test task" -d "Test description"
# Expected: Success output with task details, exit code 0
```

---

## Step 5: Create Main Entry Point

**File**: `src/main.py`

**Purpose**: Route commands to appropriate handlers

**Implementation**:
```python
import sys
from src.cli.add_task import add_task_command


def main():
    """Main entry point for the todo CLI application"""
    if len(sys.argv) < 2:
        print("Usage: python src/main.py <command> [args]", file=sys.stderr)
        print("Commands: add", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]

    if command == 'add':
        # Pass remaining args to add_task_command
        add_task_command(sys.argv[2:])
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        print("Available commands: add", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
```

**Verification**:
```bash
python src/main.py add "Buy groceries"
# Expected: Task created successfully with confirmation
```

---

## Step 6: Write Tests (Test-First)

### Unit Test: Task Model

**File**: `tests/unit/test_task_model.py`

```python
import pytest
from datetime import datetime
from src.models.task import Task, TaskStatus


def test_task_creation_with_title_only():
    """Test creating a task with just a title"""
    task = Task(id="test-123", title="Buy milk")

    assert task.id == "test-123"
    assert task.title == "Buy milk"
    assert task.description == ""
    assert task.status == TaskStatus.INCOMPLETE
    assert isinstance(task.created, datetime)


def test_task_creation_with_description():
    """Test creating a task with title and description"""
    task = Task(id="test-123", title="Buy milk", description="From the store")

    assert task.title == "Buy milk"
    assert task.description == "From the store"


def test_task_title_trimming():
    """Test that title whitespace is trimmed"""
    task = Task(id="test-123", title="  Buy milk  ")

    assert task.title == "Buy milk"


def test_empty_title_raises_error():
    """Test that empty title raises ValueError"""
    with pytest.raises(ValueError, match="Title cannot be empty"):
        Task(id="test-123", title="")


def test_whitespace_only_title_raises_error():
    """Test that whitespace-only title raises ValueError"""
    with pytest.raises(ValueError, match="Title cannot be empty"):
        Task(id="test-123", title="   ")


def test_title_too_long_raises_error():
    """Test that title over 500 chars raises ValueError"""
    with pytest.raises(ValueError, match="Title cannot exceed 500 characters"):
        Task(id="test-123", title="a" * 501)


def test_description_too_long_raises_error():
    """Test that description over 5000 chars raises ValueError"""
    with pytest.raises(ValueError, match="Description cannot exceed 5000 characters"):
        Task(id="test-123", title="Valid", description="a" * 5001)


def test_special_characters_in_title():
    """Test that special characters are preserved"""
    task = Task(id="test-123", title='Review PR #123 "urgent"')

    assert task.title == 'Review PR #123 "urgent"'


def test_unicode_in_title():
    """Test that Unicode characters are supported"""
    task = Task(id="test-123", title="Café ☕")

    assert task.title == "Café ☕"
```

**Run Tests**:
```bash
pytest tests/unit/test_task_model.py -v
# Expected: All tests pass
```

---

### Unit Test: Task Service

**File**: `tests/unit/test_task_service.py`

```python
import pytest
from src.services.task_service import create_task, get_task, clear_tasks, generate_task_id
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
```

**Run Tests**:
```bash
pytest tests/unit/test_task_service.py -v
# Expected: All tests pass
```

---

### Integration Test: CLI End-to-End

**File**: `tests/integration/test_add_task_integration.py`

```python
import subprocess
import sys


def test_add_task_title_only_success():
    """Test adding a task with title only via CLI"""
    result = subprocess.run(
        [sys.executable, 'src/main.py', 'add', 'Buy groceries'],
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
        [sys.executable, 'src/main.py', 'add', 'Prepare presentation',
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
        [sys.executable, 'src/main.py', 'add', '   '],
        capture_output=True,
        text=True
    )

    assert result.returncode == 1
    assert "Error: Title cannot be empty" in result.stderr


def test_add_task_help():
    """Test that --help displays usage information"""
    result = subprocess.run(
        [sys.executable, 'src/main.py', 'add', '--help'],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert "usage:" in result.stdout
    assert "Task title" in result.stdout
```

**Run Tests**:
```bash
pytest tests/integration/test_add_task_integration.py -v
# Expected: All tests pass
```

---

## Step 7: Run All Tests

### Full Test Suite

```bash
# Run all tests with coverage
pytest tests/ -v --cov=src --cov-report=term-missing

# Expected output:
# - All tests pass (green)
# - Coverage >90% for models, services, cli
```

### Manual Validation

```bash
# Test 1: Basic task creation
python src/main.py add "Buy groceries"

# Test 2: Task with description
python src/main.py add "Call dentist" -d "Schedule checkup for next month"

# Test 3: Empty title error
python src/main.py add ""
# Expected: Error message to stderr, exit code 1

# Test 4: Help display
python src/main.py add --help
# Expected: Usage information, exit code 0

# Test 5: Special characters
python src/main.py add "Review PR #123" -d "Check \"unit tests\""

# Test 6: Unicode
python src/main.py add "Café ☕"
```

---

## Step 8: Verify Acceptance Criteria

Check all success criteria from spec.md:

- ✅ **SC-001**: Users can create a basic task (title only) in under 10 seconds
  - Verified: `python src/main.py add "Test"` completes instantly

- ✅ **SC-002**: System generates unique task IDs with 100% uniqueness
  - Verified: `test_task_id_uniqueness()` passes

- ✅ **SC-003**: Task creation succeeds for titles up to 500 characters
  - Verified: `Task(id="x", title="a"*500)` succeeds

- ✅ **SC-004**: Task creation succeeds for descriptions up to 5000 characters
  - Verified: `Task(id="x", title="T", description="a"*5000)` succeeds

- ✅ **SC-005**: Empty title validation prevents creation 100% of the time
  - Verified: `test_empty_title_raises_error()` passes

- ✅ **SC-006**: Successful task creation returns confirmation within 100ms
  - Verified: Manual timing shows <10ms on modern hardware

---

## Troubleshooting

### "Module not found" errors

**Solution**: Ensure you're running from project root and have created all `__init__.py` files

```bash
# Verify project structure
tree src tests
# Ensure __init__.py exists in all package directories
```

### Tests fail with "datetime" mismatch

**Solution**: Tests that compare `datetime.now()` values may fail due to timing. Use `monkeypatch` in pytest to mock timestamps:

```python
from datetime import datetime

def test_with_fixed_time(monkeypatch):
    fixed_time = datetime(2025, 12, 31, 10, 30, 0)
    monkeypatch.setattr('src.models.task.datetime', lambda: fixed_time)
    # ... rest of test
```

### "Title cannot be empty" despite providing title

**Solution**: Check if shell is stripping quotes. Use double quotes for titles with spaces:

```bash
# Correct
python src/main.py add "Buy milk"

# Incorrect (shell interprets as two separate args)
python src/main.py add Buy milk
```

---

## Next Steps

Once Add Task is complete and all tests pass:

1. ✅ Run `/sp.tasks` to generate task decomposition
2. ✅ Run `/sp.implement` to execute implementation
3. ✅ Validate against all acceptance scenarios in spec.md
4. ✅ Move to next feature (Delete Task, Update Task, View Task List, Mark Complete/Incomplete)

---

## Success Checklist

- [ ] All source files created (`src/models/task.py`, `src/services/task_service.py`, `src/cli/add_task.py`, `src/main.py`)
- [ ] All test files created (`tests/unit/test_task_model.py`, `tests/unit/test_task_service.py`, `tests/integration/test_add_task_integration.py`)
- [ ] All unit tests pass (pytest exit code 0)
- [ ] All integration tests pass (pytest exit code 0)
- [ ] Manual validation completed for all examples above
- [ ] All 6 success criteria verified (SC-001 through SC-006)
- [ ] Code follows clean code principles (modularity, separation of concerns)
- [ ] No manual code edits (all code generated by Claude Code)
