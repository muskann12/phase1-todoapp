# Quickstart: Test-First Development Workflow

**Feature**: 005-toggle-task-status
**Date**: 2026-01-01
**Phase**: 1 (Design)

## Overview

This guide defines the Test-First Development (TDD) workflow for implementing the Toggle Task Status feature. The implementation follows the strict RED-GREEN-REFACTOR cycle as mandated by Constitution Principle V (NON-NEGOTIABLE).

**Total Tests**: 23 tests (11 unit + 12 integration)
**Test Coverage Target**: ≥90% service layer, ≥80% CLI layer

---

## TDD Workflow: RED-GREEN-REFACTOR

### Phase Structure

The implementation is organized into phases following user story priorities:

1. **Setup Phase**: Infrastructure (if needed)
2. **Foundational Phase**: Shared dependencies (if needed)
3. **User Story 1 (P1 - MVP)**: Mark Task as Complete
4. **User Story 2 (P2)**: Mark Task as Incomplete
5. **User Story 3 (P3)**: Toggle Task Status
6. **Polish Phase**: Coverage, documentation, manual testing

Each user story follows the same TDD cycle:
- 🔴 **RED**: Write tests FIRST, verify they FAIL
- 🟢 **GREEN**: Implement minimal code to pass tests
- 🔵 **REFACTOR**: Clean up code, verify no regressions

---

## User Story 1: Mark Task as Complete (P1 - MVP)

### 🔴 RED Phase: Write Tests First

#### Unit Tests (test_task_service.py)

**Location**: `tests/unit/test_task_service.py`

**Test 1: Successfully mark incomplete task as complete**
```python
def test_mark_complete_returns_completed_task():
    """Test that mark_complete returns task with COMPLETE status."""
    # Setup: Create incomplete task
    task = create_task("Buy milk", "")
    task_id = task.id

    # Execute: Mark as complete
    result = mark_complete(task_id)

    # Verify: Task status is COMPLETE
    assert result.status == TaskStatus.COMPLETE
    assert result.id == task_id
    assert result.title == "Buy milk"
```

**Test 2: Verify task is updated in storage**
```python
def test_mark_complete_updates_storage():
    """Test that mark_complete updates task in storage dict."""
    # Setup: Create incomplete task
    task = create_task("Buy milk", "")
    task_id = task.id

    # Execute: Mark as complete
    mark_complete(task_id)

    # Verify: Task in storage has COMPLETE status
    assert tasks[task_id].status == TaskStatus.COMPLETE
```

**Test 3: Raise error for non-existent task ID**
```python
def test_mark_complete_nonexistent_id_raises_keyerror():
    """Test that mark_complete raises KeyError for non-existent ID."""
    # Setup: Non-existent ID
    task_id = "non-existent-id"

    # Execute & Verify: Raises KeyError
    with pytest.raises(KeyError):
        mark_complete(task_id)
```

**Test 4: Idempotent behavior (mark complete task as complete)**
```python
def test_mark_complete_idempotent():
    """Test that marking complete task as complete is idempotent."""
    # Setup: Create complete task
    task = create_task("Buy milk", "")
    task = mark_complete(task.id)
    assert task.status == TaskStatus.COMPLETE

    # Execute: Mark as complete again
    result = mark_complete(task.id)

    # Verify: Still COMPLETE, no error
    assert result.status == TaskStatus.COMPLETE
    assert result.id == task.id
```

#### Integration Tests (test_complete_task_integration.py)

**Location**: `tests/integration/test_complete_task_integration.py`

**Test 1: Complete command success (in-process)**
```python
def test_complete_task_in_process():
    """Test complete command success in-process."""
    # Setup: Create incomplete task
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
```

**Test 2: Complete command help**
```python
def test_complete_help():
    """Test complete command help text."""
    # Execute: Run complete --help
    result = subprocess.run(
        ["python", "src/main.py", "complete", "--help"],
        capture_output=True,
        text=True
    )

    # Verify: Help text displays
    assert result.returncode == 0
    assert "Mark a task as complete" in result.stdout
    assert "task_id" in result.stdout
```

**Test 3: Complete command with non-existent task ID**
```python
def test_complete_nonexistent_task():
    """Test complete command with non-existent task ID."""
    # Execute: Run complete with invalid ID
    result = subprocess.run(
        ["python", "src/main.py", "complete", "non-existent-id"],
        capture_output=True,
        text=True
    )

    # Verify: Error message and exit code 1
    assert result.returncode == 1
    assert "Error: Task not found with ID: non-existent-id" in result.stderr
```

**Test 4: Complete command with missing task ID**
```python
def test_complete_missing_task_id():
    """Test complete command with missing task ID argument."""
    # Execute: Run complete without task ID
    result = subprocess.run(
        ["python", "src/main.py", "complete"],
        capture_output=True,
        text=True
    )

    # Verify: argparse error and exit code 2
    assert result.returncode == 2
    assert "required: task_id" in result.stderr
```

#### Checkpoint: Verify RED Phase

**Command**: `pytest tests/unit/test_task_service.py::test_mark_complete* -v`

**Expected Result**: All 4 unit tests FAIL with ImportError or AttributeError
```
FAILED tests/unit/test_task_service.py::test_mark_complete_returns_completed_task - AttributeError: module 'src.services.task_service' has no attribute 'mark_complete'
FAILED tests/unit/test_task_service.py::test_mark_complete_updates_storage - AttributeError: ...
FAILED tests/unit/test_task_service.py::test_mark_complete_nonexistent_id_raises_keyerror - AttributeError: ...
FAILED tests/unit/test_task_service.py::test_mark_complete_idempotent - AttributeError: ...
```

**Command**: `pytest tests/integration/test_complete_task_integration.py -v`

**Expected Result**: All 4 integration tests FAIL
```
FAILED tests/integration/test_complete_task_integration.py::test_complete_task_in_process - ImportError: cannot import name 'complete_task_command'
FAILED tests/integration/test_complete_task_integration.py::test_complete_help - ...
FAILED tests/integration/test_complete_task_integration.py::test_complete_nonexistent_task - ...
FAILED tests/integration/test_complete_task_integration.py::test_complete_missing_task_id - ...
```

**✅ Checkpoint PASS**: All tests fail (no implementation exists yet)

---

### 🟢 GREEN Phase: Implement to Pass Tests

#### Step 1: Implement Service Layer

**File**: `src/services/task_service.py`

**Add mark_complete function**:
```python
def mark_complete(task_id: str) -> Task:
    """
    Mark a task as complete.

    Args:
        task_id: The ID of the task to mark as complete

    Returns:
        Task: The updated task with COMPLETE status

    Raises:
        KeyError: If task with given ID does not exist
    """
    if task_id not in tasks:
        raise KeyError(f"Task not found with ID: {task_id}")

    task = tasks[task_id]
    updated_task = Task(
        id=task.id,
        title=task.title,
        description=task.description,
        status=TaskStatus.COMPLETE,
        created=task.created
    )
    tasks[task_id] = updated_task
    return updated_task
```

**Verify Service Tests**:
```bash
pytest tests/unit/test_task_service.py::test_mark_complete* -v
```

**Expected**: All 4 unit tests PASS

---

#### Step 2: Implement CLI Layer

**File**: `src/cli/complete_task.py` (NEW)

**Create complete command module**:
```python
"""CLI command for marking tasks as complete."""

import argparse
import sys
from services.task_service import mark_complete

def complete_task_command(args: list[str]) -> None:
    """
    CLI command to mark a task as complete.

    Args:
        args: Command-line arguments (excluding 'complete')
    """
    parser = argparse.ArgumentParser(
        description="Mark a task as complete",
        prog="complete"
    )
    parser.add_argument(
        "task_id",
        help="The ID of the task to mark as complete"
    )

    try:
        parsed_args = parser.parse_args(args)
        task = mark_complete(parsed_args.task_id)

        # Display success message
        desc_display = task.description if task.description else "(none)"
        status_display = "Complete" if task.status == TaskStatus.COMPLETE else "Incomplete"
        print(f"Task marked as complete! ID: {task.id}, Title: {task.title}, Description: {desc_display}, Status: {status_display}")
        sys.exit(0)

    except KeyError as e:
        print(f"Error: Task not found with ID: {parsed_args.task_id}", file=sys.stderr)
        sys.exit(1)
```

---

#### Step 3: Update Main Router

**File**: `src/main.py`

**Update help text**:
```python
print("Commands: add, view, update, delete, complete, incomplete, toggle")
```

**Add complete command routing**:
```python
elif command == "complete":
    from cli.complete_task import complete_task_command
    complete_task_command(sys.argv[2:])
```

**Update error message**:
```python
print("Valid commands: add, view, update, delete, complete, incomplete, toggle", file=sys.stderr)
```

---

#### Checkpoint: Verify GREEN Phase

**Command**: `pytest tests/unit/test_task_service.py::test_mark_complete* -v`

**Expected**: All 4 unit tests PASS

**Command**: `pytest tests/integration/test_complete_task_integration.py -v`

**Expected**: All 4 integration tests PASS

**Command**: `pytest -v` (run all tests)

**Expected**: All existing tests PASS (no regressions)

**✅ Checkpoint PASS**: All tests pass, User Story 1 complete

---

### 🔵 REFACTOR Phase: Code Quality

#### Code Review Checklist

- [ ] No duplicate code (DRY principle)
- [ ] Function names are clear and descriptive
- [ ] Docstrings present for all public functions
- [ ] Type hints present for all parameters and return values
- [ ] Error messages match spec exactly
- [ ] Success messages match spec exactly
- [ ] Exit codes match spec (0, 1, 2)

#### Refactor if Needed

- Extract common patterns (if duplication found)
- Rename unclear variables/functions
- Add missing docstrings
- Simplify complex logic

#### Checkpoint: Verify No Regressions

**Command**: `pytest -v`

**Expected**: All tests still PASS (including existing features: Add, View, Update, Delete)

**✅ Checkpoint PASS**: Code is clean, all tests pass

---

## User Story 2: Mark Task as Incomplete (P2)

### 🔴 RED Phase: Write Tests First

#### Unit Tests (test_task_service.py)

**Test 1: Successfully mark complete task as incomplete**
```python
def test_mark_incomplete_returns_incomplete_task():
    """Test that mark_incomplete returns task with INCOMPLETE status."""
    # Setup: Create complete task
    task = create_task("Review document", "")
    task = mark_complete(task.id)

    # Execute: Mark as incomplete
    result = mark_incomplete(task.id)

    # Verify: Task status is INCOMPLETE
    assert result.status == TaskStatus.INCOMPLETE
    assert result.id == task.id
```

**Test 2: Verify task is updated in storage**
```python
def test_mark_incomplete_updates_storage():
    """Test that mark_incomplete updates task in storage dict."""
    # Setup: Create complete task
    task = create_task("Review document", "")
    task = mark_complete(task.id)

    # Execute: Mark as incomplete
    mark_incomplete(task.id)

    # Verify: Task in storage has INCOMPLETE status
    assert tasks[task.id].status == TaskStatus.INCOMPLETE
```

**Test 3: Raise error for non-existent task ID**
```python
def test_mark_incomplete_nonexistent_id_raises_keyerror():
    """Test that mark_incomplete raises KeyError for non-existent ID."""
    with pytest.raises(KeyError):
        mark_incomplete("non-existent-id")
```

**Test 4: Idempotent behavior**
```python
def test_mark_incomplete_idempotent():
    """Test that marking incomplete task as incomplete is idempotent."""
    # Setup: Create incomplete task
    task = create_task("Review document", "")
    assert task.status == TaskStatus.INCOMPLETE

    # Execute: Mark as incomplete again
    result = mark_incomplete(task.id)

    # Verify: Still INCOMPLETE, no error
    assert result.status == TaskStatus.INCOMPLETE
```

#### Integration Tests (test_incomplete_task_integration.py)

Similar structure to complete tests (4 tests: success, help, non-existent, missing arg)

#### Checkpoint: Verify RED Phase

All 8 tests (4 unit + 4 integration) should FAIL

---

### 🟢 GREEN Phase: Implement to Pass Tests

#### Step 1: Implement Service Layer

**Add mark_incomplete function** to `src/services/task_service.py` (similar to mark_complete)

#### Step 2: Implement CLI Layer

**Create** `src/cli/incomplete_task.py` (similar to complete_task.py)

#### Step 3: Update Main Router

**Add** incomplete command routing to `src/main.py`

#### Checkpoint: Verify GREEN Phase

All 8 tests should PASS

---

### 🔵 REFACTOR Phase: Code Quality

Review for common patterns between mark_complete and mark_incomplete (may extract helper if needed)

---

## User Story 3: Toggle Task Status (P3)

### 🔴 RED Phase: Write Tests First

#### Unit Tests (test_task_service.py)

**Test 1: Toggle incomplete to complete**
```python
def test_toggle_status_incomplete_to_complete():
    """Test that toggle flips INCOMPLETE to COMPLETE."""
    # Setup: Create incomplete task
    task = create_task("Buy milk", "")
    assert task.status == TaskStatus.INCOMPLETE

    # Execute: Toggle status
    result = toggle_status(task.id)

    # Verify: Status is now COMPLETE
    assert result.status == TaskStatus.COMPLETE
```

**Test 2: Toggle complete to incomplete**
```python
def test_toggle_status_complete_to_incomplete():
    """Test that toggle flips COMPLETE to INCOMPLETE."""
    # Setup: Create complete task
    task = create_task("Buy milk", "")
    task = mark_complete(task.id)
    assert task.status == TaskStatus.COMPLETE

    # Execute: Toggle status
    result = toggle_status(task.id)

    # Verify: Status is now INCOMPLETE
    assert result.status == TaskStatus.INCOMPLETE
```

**Test 3: Raise error for non-existent task ID**
```python
def test_toggle_status_nonexistent_id_raises_keyerror():
    """Test that toggle_status raises KeyError for non-existent ID."""
    with pytest.raises(KeyError):
        toggle_status("non-existent-id")
```

#### Integration Tests (test_toggle_task_integration.py)

Similar structure (4 tests: success, help, non-existent, missing arg)

#### Checkpoint: Verify RED Phase

All 7 tests (3 unit + 4 integration) should FAIL

---

### 🟢 GREEN Phase: Implement to Pass Tests

#### Step 1: Implement Service Layer

**Add toggle_status function** with flip logic

#### Step 2: Implement CLI Layer

**Create** `src/cli/toggle_task.py`

#### Step 3: Update Main Router

**Add** toggle command routing to `src/main.py`

#### Checkpoint: Verify GREEN Phase

All 7 tests should PASS

---

### 🔵 REFACTOR Phase: Code Quality

Final review of all three commands, extract any common patterns

---

## Polish Phase

### Manual Testing

Test all three commands with:
- Success scenarios (with and without description)
- Help text display
- Error scenarios (non-existent ID)
- Unicode characters in task data

### Coverage Report

**Command**:
```bash
pytest --cov=src --cov-report=term-missing
```

**Target**:
- Service layer: ≥90% coverage
- CLI layer: ≥80% coverage

### Success Criteria Validation

Verify all 8 success criteria from spec.md:
- SC-001: Single command status change ✓
- SC-002: Immediate appearance in views ✓
- SC-003: Clear confirmation messages ✓
- SC-004: Clear error messages ✓
- SC-005: < 1 second operation time ✓
- SC-006: Unicode display ✓
- SC-007: Help documentation ✓
- SC-008: Toggle without knowing state ✓

---

## Summary

**Total Tests**: 23 tests
- Unit tests: 11 (4 complete + 4 incomplete + 3 toggle)
- Integration tests: 12 (4 per command × 3 commands)

**TDD Cycle**: RED-GREEN-REFACTOR strictly followed for each user story

**Coverage Target**: ≥90% service layer, ≥80% CLI layer

**Deliverables**:
- 3 service functions (mark_complete, mark_incomplete, toggle_status)
- 3 CLI command modules (complete_task.py, incomplete_task.py, toggle_task.py)
- Updated main router (3 new elif blocks)
- 23 passing tests (no regressions)
