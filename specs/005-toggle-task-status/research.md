# Research: Toggle Task Status

**Feature**: 005-toggle-task-status
**Date**: 2026-01-01
**Phase**: 0 (Technical Research)

## Overview

This document captures technical decisions made during the research phase for the Toggle Task Status feature. All decisions follow the Constitution principles and leverage existing patterns from Add Task (001), View Task List (002), Update Task (003), and Delete Task (004) features.

## Technical Decisions

### Decision 1: Service Layer Function Design

**Question**: Should we implement three separate functions or one unified function for status changes?

**Options Considered**:

1. **Option A: Three Functions** (SELECTED)
   - `mark_complete(task_id: str) -> Task`
   - `mark_incomplete(task_id: str) -> Task`
   - `toggle_status(task_id: str) -> Task`

2. **Option B: Single Function with Status Parameter**
   - `update_status(task_id: str, new_status: TaskStatus) -> Task`

3. **Option C: Single Function with Action Parameter**
   - `change_status(task_id: str, action: Literal["complete", "incomplete", "toggle"]) -> Task`

**Decision**: Option A - Three Separate Functions

**Rationale**:
- Matches CLI command structure (three distinct commands)
- Clear, self-documenting function names
- Simpler function signatures (no enum/literal parameters)
- Easier to test (focused unit tests per operation)
- Follows single-responsibility principle
- Consistent with existing pattern (`create_task()`, `update_task()`, `delete_task()`)
- Each function has clear postcondition (complete, incomplete, or toggled)

**Impact**: Service layer grows by ~65 lines (3 functions × ~20 lines each)

---

### Decision 2: Idempotent Operation Behavior

**Question**: What happens when marking a complete task as complete (or incomplete task as incomplete)?

**Options Considered**:

1. **Option A: Show Success** (SELECTED)
   - Return task with current status
   - Display success message
   - Exit code 0

2. **Option B: Show Error**
   - Raise ValueError("Task is already complete")
   - Display error message
   - Exit code 1

**Decision**: Option A - Show Success Message

**Rationale**:
- Spec edge case explicitly states: "System displays success message showing task is complete (idempotent operation - no error, just confirmation of current state)"
- FR-013: "System MUST support idempotent operations"
- Follows HTTP PUT semantics (idempotent state assignment)
- User-friendly - no error for achieving desired state
- Simplifies scripting/automation (exit code 0 = desired state achieved)
- Consistent with "tell, don't ask" principle (user declares desired state, system confirms)

**Impact**: Service layer returns task regardless of current status, CLI always shows success

---

### Decision 3: Status Change Implementation Method

**Question**: How should we implement status changes internally?

**Options Considered**:

1. **Option A: Direct Mutation**
   - Modify `task.status` in-place
   - Update task in storage dict

2. **Option B: Create New Task Instance** (SELECTED)
   - Create new Task with updated status
   - Replace in storage dict

3. **Option C: Separate Mutable vs Immutable Fields**
   - Task dataclass with mutable status field
   - Immutable other fields

**Decision**: Option B - Create New Task Instance

**Rationale**:
- Consistent with existing `update_task()` pattern (creates new Task object)
- Maintains Task dataclass immutability principle
- Triggers validation in `Task.__post_init__()` (defense in depth)
- Safer for future refactoring (no side effects)
- Aligns with Constitution Principle VI (clean code, modularity)
- Pattern already proven in Update Task (003)

**Implementation**:
```python
def mark_complete(task_id: str) -> Task:
    if task_id not in tasks:
        raise KeyError(f"Task not found with ID: {task_id}")

    task = tasks[task_id]
    updated_task = Task(
        id=task.id,
        title=task.title,
        description=task.description,
        status=TaskStatus.COMPLETE,  # New status
        created=task.created
    )
    tasks[task_id] = updated_task
    return updated_task
```

**Impact**: Service layer code follows proven pattern from Update Task

---

### Decision 4: Toggle Status Logic

**Question**: How should `toggle_status()` determine the new status?

**Options Considered**:

1. **Option A: Check Current Status, Then Flip** (SELECTED)
   - If INCOMPLETE → mark as COMPLETE
   - If COMPLETE → mark as INCOMPLETE

2. **Option B: Use Status Enum Method**
   - Add `TaskStatus.opposite()` method
   - Call `task.status.opposite()`

3. **Option C: Cycle Through All Statuses**
   - Support future status values (e.g., IN_PROGRESS)
   - Use list rotation logic

**Decision**: Option A - Check and Flip

**Rationale**:
- Simple and explicit (Constitution Principle VII)
- No modification to Task model needed
- Only two states exist (INCOMPLETE, COMPLETE) - no need for cycling logic
- Clear what happens for each current state
- Easy to test (2 test cases: incomplete→complete, complete→incomplete)
- Matches spec: "toggle a task's status (complete ↔ incomplete)"

**Implementation**:
```python
def toggle_status(task_id: str) -> Task:
    if task_id not in tasks:
        raise KeyError(f"Task not found with ID: {task_id}")

    task = tasks[task_id]
    new_status = TaskStatus.COMPLETE if task.status == TaskStatus.INCOMPLETE else TaskStatus.INCOMPLETE

    updated_task = Task(
        id=task.id,
        title=task.title,
        description=task.description,
        status=new_status,
        created=task.created
    )
    tasks[task_id] = updated_task
    return updated_task
```

**Impact**: Toggle logic is clear and testable with 2 scenarios

---

### Decision 5: CLI Structure

**Question**: Should we create three separate CLI files or one file with subcommands?

**Options Considered**:

1. **Option A: Three Separate Files** (SELECTED)
   - `src/cli/complete_task.py`
   - `src/cli/incomplete_task.py`
   - `src/cli/toggle_task.py`

2. **Option B: Single File with Subcommands**
   - `src/cli/task_status.py`
   - Uses `argparse` subparsers for `complete`, `incomplete`, `toggle`

3. **Option C: Single File with Shared Logic**
   - `src/cli/change_status.py`
   - Single `change_status_command(action)` function

**Decision**: Option A - Three Separate Files

**Rationale**:
- Consistent with existing pattern (Add Task, Update Task, Delete Task all have separate files)
- Each command is independently testable
- Clear separation of concerns (one file = one command)
- Main router follows established pattern (elif blocks per command)
- Easier to maintain (changes to one command don't affect others)
- Follows Constitution Principle VI (modularity)
- No added complexity from subparser setup

**Impact**: CLI layer has 3 new files (~55 lines each), main.py gains 3 elif blocks

---

### Decision 6: Success Message Format

**Question**: What information should success messages display?

**Options Considered**:

1. **Option A: ID, Title, Description, Status** (SELECTED)
   - "Task marked as complete! ID: abc-123, Title: Buy milk, Description: (none), Status: Complete"

2. **Option B: ID and Status Only**
   - "Task abc-123 marked as complete"

3. **Option C: Full Task Details with Timestamps**
   - Include created timestamp and all fields

**Decision**: Option A - ID, Title, Description, Status

**Rationale**:
- Spec acceptance scenario explicitly defines this format (User Story 1, Scenario 1)
- FR-008: "System MUST display success message showing task ID, title, description (if present), and new status"
- Provides confirmation of what changed
- User can verify correct task was modified
- Shows "(none)" if description is empty (consistent with View Task List)
- Matches existing pattern from Update Task (shows all modified fields)

**Implementation**:
```python
desc_display = task.description if task.description else "(none)"
status_display = "Complete" if task.status == TaskStatus.COMPLETE else "Incomplete"
print(f"Task marked as {status_display.lower()}! ID: {task.id}, Title: {task.title}, Description: {desc_display}, Status: {status_display}")
```

**Impact**: CLI layer displays consistent message format across all three commands

---

### Decision 7: Error Handling Pattern

**Question**: How should service layer communicate errors to CLI layer?

**Options Considered**:

1. **Option A: Raise KeyError, CLI Translates** (SELECTED)
   - Service raises `KeyError(f"Task not found with ID: {task_id}")`
   - CLI catches and displays user-friendly message

2. **Option B: Custom Exception Class**
   - Create `TaskNotFoundException(task_id)`
   - CLI catches specific exception type

3. **Option C: Return Optional**
   - Service returns `Optional[Task]` (None if not found)
   - CLI checks for None and displays error

**Decision**: Option A - Raise KeyError, CLI Translates

**Rationale**:
- Consistent with existing pattern from Delete Task (004)
- KeyError is semantic (task ID is a key in storage dict)
- No new exception classes needed (keeps codebase simple)
- Service layer stays focused on business logic
- CLI layer owns user-facing error messages
- Follows Constitution Principle VI (separation of concerns)

**Implementation**:
```python
# Service layer
def mark_complete(task_id: str) -> Task:
    if task_id not in tasks:
        raise KeyError(f"Task not found with ID: {task_id}")
    # ... implementation

# CLI layer
try:
    task = mark_complete(task_id)
    # ... success message
except KeyError:
    print(f"Error: Task not found with ID: {task_id}", file=sys.stderr)
    sys.exit(1)
```

**Impact**: Service layer raises standard Python exceptions, CLI translates to spec-defined messages

---

### Decision 8: Exit Code Strategy for Idempotent Operations

**Question**: What exit code should idempotent operations return?

**Options Considered**:

1. **Option A: Exit Code 0 Always** (SELECTED)
   - Success exit code for all idempotent operations

2. **Option B: Exit Code 0 for Change, 2 for No-Op**
   - Exit code 0 if status changed
   - Exit code 2 if status was already in target state

3. **Option C: Different Codes per Scenario**
   - Exit code 0 for normal success
   - Exit code 3 for idempotent success

**Decision**: Option A - Exit Code 0 Always

**Rationale**:
- FR-010: "System MUST exit with code 0 on successful status change"
- FR-013: "System MUST support idempotent operations (marking complete task as complete is valid, shows current status)"
- Combining FR-010 and FR-013: Idempotent operation is "successful status change" (desired state achieved)
- Simplifies scripting (exit code 0 = task is now in desired state)
- Consistent with HTTP PUT semantics (idempotent = success)
- No need to check previous state in scripts

**Impact**: CLI always exits with code 0 for valid task IDs, regardless of previous status

---

### Decision 9: Unicode Character Handling

**Question**: How should we handle Unicode characters in task data?

**Options Considered**:

1. **Option A: Display Natively** (SELECTED)
   - Display Unicode characters as-is
   - Trust Python 3.13+ UTF-8 mode

2. **Option B: ASCII-Safe Encoding**
   - Replace Unicode with ASCII equivalents
   - Use `str.encode('ascii', errors='replace')`

3. **Option C: Escape Unicode**
   - Display Unicode escape sequences
   - Use `repr()` for display

**Decision**: Option A - Display Natively

**Rationale**:
- FR-014: "System MUST correctly display Unicode characters in status change confirmation message"
- SC-006: "Unicode characters in task data are correctly displayed"
- Consistent with existing features (Add Task, View Task List, Update Task all handle Unicode natively)
- Python 3.13+ has UTF-8 mode enabled by default
- No added complexity for Unicode handling
- Terminal encoding limitations are user's environment issue (not application issue)

**Implementation**: No special handling needed - use standard `print()` with f-strings

**Impact**: CLI layer handles Unicode same as existing features (no new code needed)

---

### Decision 10: Status Validation Strategy

**Question**: Should we validate TaskStatus values in service layer?

**Options Considered**:

1. **Option A: Trust Storage, No Extra Validation** (SELECTED)
   - Service layer assumes tasks in storage have valid status
   - Task dataclass `__post_init__()` validates on creation

2. **Option B: Explicit Runtime Validation**
   - Check `task.status in [TaskStatus.INCOMPLETE, TaskStatus.COMPLETE]` before toggling
   - Raise ValueError for invalid status

3. **Option C: Type Narrowing**
   - Use `assert isinstance(task.status, TaskStatus)` in service layer
   - Runtime type checking with asserts

**Decision**: Option A - Trust Storage, No Extra Validation

**Rationale**:
- Task dataclass validates in `__post_init__()` (defense at creation boundary)
- TaskStatus is an Enum - only valid values can exist
- Service layer creates new Task instances (triggers validation)
- No way to get invalid TaskStatus unless Task model is broken
- Follows Constitution Principle VII (explicit over implicit, but don't validate what can't be wrong)
- Keeps service layer code simple and focused

**Impact**: Service layer code has no defensive status validation checks

---

## Technology Stack Decisions

**Language**: Python 3.13+
**CLI Framework**: argparse (stdlib)
**Testing**: pytest
**Type Hints**: Native (PEP 604 union operator)
**Storage**: In-memory `Dict[str, Task]` (Phase I constraint)

**Rationale**: Reuse existing stack from Add Task (001), Update Task (003), Delete Task (004). No new dependencies required.

---

## Pattern Reuse

- **Task Model**: Reuse existing Task dataclass and TaskStatus enum (no changes)
- **Service Layer Pattern**: Follow Update Task (create new Task instance)
- **CLI Argument Parsing**: Follow Delete Task (positional argument)
- **Error Handling**: Follow Delete Task (KeyError → user message)
- **Success Messages**: Follow spec format (ID, Title, Description, Status)
- **Test Structure**: Follow existing pattern (unit tests in test_task_service.py, integration tests in separate files)

---

## Next Steps

1. ✅ Phase 0 Complete: All technical decisions documented
2. ⏭️ Phase 1 Next: Create data-model.md, contracts/, quickstart.md
3. ⏭️ Phase 2 Next: Execute `/sp.tasks` to generate tasks.md
