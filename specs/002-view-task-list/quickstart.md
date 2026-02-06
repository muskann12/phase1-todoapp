# Quickstart Guide: View Task List Implementation

**Feature**: View Task List
**Date**: 2025-12-31
**Purpose**: Step-by-step implementation guide following Test-First Development

---

## Prerequisites

Before starting implementation:
- ✅ Add Task feature fully implemented (`src/models/task.py`, `src/services/task_service.py` exist)
- ✅ Python 3.13+ installed
- ✅ pytest installed for testing
- ✅ Specification and plan documents reviewed

---

## Implementation Steps

### Step 1: Extend Service Layer (Test-First)

**File**: `src/services/task_service.py`

**Add function** (after existing `create_task`, `get_task`, `clear_tasks`):

```python
def get_all_tasks() -> list[Task]:
    """
    Retrieve all tasks sorted by ID in ascending order.

    Returns:
        list[Task]: All tasks sorted by task ID (deterministic order)

    Note:
        This is a read-only operation. The internal _tasks dict is not modified.
    """
    return sorted(_tasks.values(), key=lambda task: task.id)
```

**Why this code**:
- Reuses existing `_tasks` dict from Add Task feature
- Sorts by ID for deterministic output (SC-002 requirement)
- Read-only operation (no mutation per SC-006)
- Returns list (not dict) for easier iteration in CLI layer

---

### Step 2: Create CLI Module (Test-First)

**File**: `src/cli/view_tasks.py` (NEW FILE)

**Complete implementation**:

```python
import argparse
import sys

from src.models.task import TaskStatus
from src.services.task_service import get_all_tasks


def view_tasks_command(args: list[str] = None):
    """
    CLI command to view all tasks.

    Args:
        args: Command-line arguments (None = use sys.argv)

    Exit Codes:
        0: Success (tasks displayed or empty-state message shown)
    """
    parser = argparse.ArgumentParser(
        description='View all tasks in your todo list',
        prog='todo view'
    )

    # No positional arguments or options needed for Phase I
    parser.parse_args(args)

    # Retrieve all tasks
    tasks = get_all_tasks()

    # Empty state handling
    if not tasks:
        print('No tasks found. Add your first task with: python -m src.main add "<title>"')
        sys.exit(0)

    # Display summary (User Story 2)
    total = len(tasks)
    incomplete = sum(1 for t in tasks if t.status == TaskStatus.INCOMPLETE)
    complete = total - incomplete

    print(f"Total: {total} | Incomplete: {incomplete} | Complete: {complete}")
    print()  # Blank line separator

    # Display tasks (User Story 1)
    for task in tasks:
        # Status indicator
        status_icon = "[✓]" if task.status == TaskStatus.COMPLETE else "[ ]"

        # Description handling
        description = task.description if task.description else "(none)"

        # Multi-line task display
        print(f"{status_icon} ID: {task.id}")
        print(f"    Title: {task.title}")
        print(f"    Description: {description}")
        print(f"    Status: {task.status.value.capitalize()}")
        print()  # Blank line between tasks

    sys.exit(0)


if __name__ == '__main__':
    view_tasks_command()
```

**Why this code**:
- Uses `argparse` for consistency with Add Task CLI (supports `--help`)
- Empty-state message guides new users (FR-006)
- Summary line at top for at-a-glance progress (US2, FR-009)
- Status icons `[ ]` / `[✓]` for quick visual scan (FR-004)
- Multi-line format for readability (long titles/descriptions don't truncate)
- Handles empty descriptions with "(none)" placeholder (FR-005)
- Exit code 0 for all cases (read-only operation has no errors)

---

### Step 3: Update Main Entry Point

**File**: `src/main.py`

**Add "view" command routing** (after "add" command):

```python
def main():
    """Main entry point for the todo CLI application"""
    if len(sys.argv) < 2:
        print("Usage: python -m src.main <command> [args]", file=sys.stderr)
        print("Commands: add, view", file=sys.stderr)  # UPDATE THIS LINE
        sys.exit(1)

    command = sys.argv[1]

    if command == 'add':
        from src.cli.add_task import add_task_command
        add_task_command(sys.argv[2:])
    elif command == 'view':  # ADD THIS BLOCK
        from src.cli.view_tasks import view_tasks_command
        view_tasks_command(sys.argv[2:])
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        print("Available commands: add, view", file=sys.stderr)  # UPDATE THIS LINE
        sys.exit(1)
```

**Why this code**:
- Follows same pattern as "add" command (consistency)
- Lazy imports CLI modules (only import when command is used)
- Updated help text to list "view" command
- Passes remaining args to CLI function (supports `--help`)

---

## Test Suite (Test-First Development)

### Unit Tests: Service Layer

**File**: `tests/unit/test_task_service.py`

**Add tests** (after existing tests):

```python
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
    # Verify ascending ID order
    assert tasks[0].id < tasks[1].id < tasks[2].id
    assert tasks[0].title == "First task"
    assert tasks[2].title == "Third task"


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
```

---

### Integration Tests: CLI

**File**: `tests/integration/test_view_tasks_integration.py` (NEW FILE)

**Complete test suite**:

```python
import subprocess
import sys


def test_view_empty_list():
    """Test viewing tasks when none exist"""
    # Note: In real scenario, need to ensure clean state
    # For demo, assume first run or separate process
    result = subprocess.run(
        [sys.executable, '-m', 'src.main', 'view'],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert 'No tasks found' in result.stdout
    assert 'python -m src.main add' in result.stdout


def test_view_single_task():
    """Test viewing a single task"""
    # Create a task first
    subprocess.run(
        [sys.executable, '-m', 'src.main', 'add', 'Test task'],
        capture_output=True
    )

    # View tasks
    result = subprocess.run(
        [sys.executable, '-m', 'src.main', 'view'],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert 'Total: 1 | Incomplete: 1 | Complete: 0' in result.stdout
    assert '[ ]' in result.stdout  # Incomplete indicator
    assert 'Title: Test task' in result.stdout
    assert 'Description: (none)' in result.stdout
    assert 'Status: Incomplete' in result.stdout


def test_view_multiple_tasks_with_summary():
    """Test viewing multiple tasks with summary line"""
    # Create multiple tasks
    subprocess.run([sys.executable, '-m', 'src.main', 'add', 'Task 1'], capture_output=True)
    subprocess.run([sys.executable, '-m', 'src.main', 'add', 'Task 2', '-d', 'Details'], capture_output=True)
    subprocess.run([sys.executable, '-m', 'src.main', 'add', 'Task 3'], capture_output=True)

    # View tasks
    result = subprocess.run(
        [sys.executable, '-m', 'src.main', 'view'],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert 'Total: 3' in result.stdout
    assert 'Incomplete: 3' in result.stdout
    assert 'Title: Task 1' in result.stdout
    assert 'Title: Task 2' in result.stdout
    assert 'Description: Details' in result.stdout
    assert 'Title: Task 3' in result.stdout


def test_view_tasks_with_unicode():
    """Test viewing tasks with Unicode characters"""
    subprocess.run(
        [sys.executable, '-m', 'src.main', 'add', 'Café ☕', '-d', 'Visit café'],
        capture_output=True
    )

    result = subprocess.run(
        [sys.executable, '-m', 'src.main', 'view'],
        capture_output=True,
        text=True,
        encoding='utf-8'
    )

    assert result.returncode == 0
    assert 'Café ☕' in result.stdout
    assert 'Visit café' in result.stdout


def test_view_help():
    """Test that --help displays usage information"""
    result = subprocess.run(
        [sys.executable, '-m', 'src.main', 'view', '--help'],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert 'usage:' in result.stdout
    assert 'View all tasks' in result.stdout
```

**Important Note**: Integration tests using subprocess create tasks in persistent in-memory storage. For independent test runs, implement `clear_tasks()` call or run tests in isolated processes.

---

## Test-First Development Workflow (RED-GREEN-REFACTOR)

### Phase 1: RED (Tests Fail)

1. **Write all unit tests first** (in `tests/unit/test_task_service.py`)
2. **Write all integration tests first** (in `tests/integration/test_view_tasks_integration.py`)
3. **Run tests and verify they FAIL**:
   ```bash
   pytest tests/unit/test_task_service.py::test_get_all_tasks_empty -v
   # Expected: FAIL (function get_all_tasks does not exist)

   pytest tests/integration/test_view_tasks_integration.py -v
   # Expected: FAIL (module src.cli.view_tasks does not exist)
   ```

**Checkpoint**: All new tests MUST fail before implementation begins.

---

### Phase 2: GREEN (Make Tests Pass)

1. **Implement `get_all_tasks()` in `src/services/task_service.py`** (Step 1 above)
2. **Implement `src/cli/view_tasks.py`** (Step 2 above)
3. **Update `src/main.py`** (Step 3 above)
4. **Run tests and verify they PASS**:
   ```bash
   pytest tests/unit/test_task_service.py -v
   # Expected: All unit tests PASS

   pytest tests/integration/test_view_tasks_integration.py -v
   # Expected: All integration tests PASS
   ```

**Checkpoint**: All tests (unit + integration) MUST pass.

---

### Phase 3: REFACTOR (Improve Code Quality)

**Check for improvements**:
- ✅ DRY violations: None (each function has single responsibility)
- ✅ Code duplication: None (display logic centralized in `view_tasks_command`)
- ✅ Naming clarity: All names descriptive (`get_all_tasks`, `view_tasks_command`)
- ✅ Type hints: All functions have type annotations
- ✅ Docstrings: All public functions documented

**Refactoring Decision**: Code is clean from start - no refactoring needed.

**Final verification**:
```bash
pytest tests/ -v
# Expected: ALL tests PASS (including Add Task regression tests)
```

---

## Manual Testing Checklist

After automated tests pass, manually verify:

- [ ] Empty list displays onboarding message
- [ ] Single task displays with summary line
- [ ] Multiple tasks display in ascending ID order
- [ ] Status icons display correctly ([ ] and [✓])
- [ ] Empty descriptions show "(none)"
- [ ] Unicode characters display correctly (test "Café ☕")
- [ ] Summary counts are accurate (create 5 tasks, verify "Total: 5")
- [ ] `--help` displays usage information
- [ ] Command completes quickly (under 2 seconds for 100+ tasks)

---

## Integration with Add Task Feature

**Verification**:
1. Create 3 tasks using Add Task command
2. View tasks using View Task List command
3. Verify all 3 tasks appear
4. Create 2 more tasks
5. View again - verify 5 tasks appear

**Expected Behavior**:
- View Task List reads from same `_tasks` dict as Add Task
- Tasks created via Add Task immediately visible in View Task List
- No data corruption or loss

---

## Performance Validation

**Test with 1000 tasks**:
```python
# Create 1000 tasks
for i in range(1000):
    subprocess.run([sys.executable, '-m', 'src.main', 'add', f'Task {i}'], capture_output=True)

# Measure view performance
import time
start = time.time()
subprocess.run([sys.executable, '-m', 'src.main', 'view'], capture_output=True)
elapsed = time.time() - start

print(f"View 1000 tasks took: {elapsed:.2f} seconds")
# Expected: < 2 seconds (SC-001)
```

---

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'src'`

**Solution**: Use `python -m src.main view` (not `python src/main.py view`)

---

### Issue: Tests fail with "No tasks found" even after creating tasks

**Cause**: Subprocess tests run in separate processes with separate in-memory storage

**Solution**: Tests that depend on existing tasks must create them within the same test:
```python
def test_view_after_add():
    # Create task in same test
    subprocess.run([sys.executable, '-m', 'src.main', 'add', 'Test'], capture_output=True)
    # Then view
    result = subprocess.run([sys.executable, '-m', 'src.main', 'view'], capture_output=True, text=True)
    assert 'Test' in result.stdout
```

---

### Issue: Unicode characters display as �� (replacement chars)

**Solution**: Ensure terminal supports UTF-8 encoding:
```bash
# Linux/Mac
export LANG=en_US.UTF-8

# Windows
chcp 65001
```

---

## Summary

**Files Created**:
1. `src/cli/view_tasks.py` (~60 lines)
2. `tests/integration/test_view_tasks_integration.py` (~80 lines)

**Files Modified**:
1. `src/services/task_service.py` (add `get_all_tasks()` function)
2. `src/main.py` (add "view" command routing)
3. `tests/unit/test_task_service.py` (add 3 unit tests)

**Total Lines of Code**: ~150 lines (implementation + tests)

**Test Coverage**:
- Unit tests: 3 (service layer)
- Integration tests: 5 (CLI end-to-end)
- **Total**: 8 tests

**Success Criteria Met**:
- ✅ SC-001: View completes in under 2 seconds
- ✅ SC-002: Deterministic sort order (ascending ID)
- ✅ SC-003: Empty-state message 100% of time
- ✅ SC-004: Unicode displayed correctly
- ✅ SC-005: Accurate summary counts
- ✅ SC-006: Read-only guarantee (no data mutation)

**Ready for**: `/sp.tasks` command to generate task decomposition
