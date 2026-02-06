# Data Model: Toggle Task Status

**Feature**: 005-toggle-task-status
**Date**: 2026-01-01
**Phase**: 1 (Design)

## Overview

This document defines the data model for the Toggle Task Status feature. The feature reuses the existing Task entity and TaskStatus enum without modifications. The focus is on documenting status transitions and storage mutation patterns.

## Entities

### Task (Existing - No Changes)

**Source**: `src/models/task.py`

**Definition**:
```python
@dataclass
class Task:
    id: str
    title: str
    description: str
    status: TaskStatus
    created: str

    def __post_init__(self):
        # Validation logic (already exists)
        pass
```

**Fields**:
- `id` (str): UUID5 deterministic identifier (format: `xxxxxxxx-xxxx-5xxx-xxxx-xxxxxxxxxxxx`)
- `title` (str): Required task title (1-200 characters)
- `description` (str): Optional task description (empty string if not provided)
- `status` (TaskStatus): Task completion state (INCOMPLETE or COMPLETE)
- `created` (str): ISO 8601 timestamp (format: `YYYY-MM-DDTHH:MM:SS`)

**Validation** (in `__post_init__`):
- All fields are required (no None values)
- `status` must be a TaskStatus enum member

**Immutability Pattern**:
- Task instances are treated as immutable
- Status changes create new Task instance with updated status field
- All other fields copied from original task

---

### TaskStatus (Existing - No Changes)

**Source**: `src/models/task.py`

**Definition**:
```python
class TaskStatus(Enum):
    INCOMPLETE = "incomplete"
    COMPLETE = "complete"
```

**Values**:
- `INCOMPLETE`: Task is not yet finished (default state for new tasks)
- `COMPLETE`: Task is finished

**Usage**:
- Stored in Task.status field
- Used in status transition logic
- Displayed in CLI messages (capitalized: "Incomplete", "Complete")

---

## Status Transitions

### State Diagram

```
┌─────────────┐
│ INCOMPLETE  │◄─────────┐
└──────┬──────┘          │
       │                 │
       │ mark_complete() │ mark_incomplete()
       │ toggle()        │ toggle()
       │                 │
       ▼                 │
┌─────────────┐          │
│  COMPLETE   │──────────┘
└─────────────┘
```

### Transition Rules

#### 1. Mark Complete (mark_complete)

**Precondition**: Task exists in storage
**Postcondition**: Task status is COMPLETE

**Transitions**:
- INCOMPLETE → COMPLETE (state change)
- COMPLETE → COMPLETE (idempotent - no state change)

**Implementation**:
```python
def mark_complete(task_id: str) -> Task:
    # Get task (raises KeyError if not found)
    task = tasks[task_id]

    # Create new task with COMPLETE status
    updated_task = Task(
        id=task.id,
        title=task.title,
        description=task.description,
        status=TaskStatus.COMPLETE,  # Always COMPLETE
        created=task.created
    )

    # Update storage
    tasks[task_id] = updated_task
    return updated_task
```

**Idempotent Behavior**: If task is already COMPLETE, return task with COMPLETE status (no error)

---

#### 2. Mark Incomplete (mark_incomplete)

**Precondition**: Task exists in storage
**Postcondition**: Task status is INCOMPLETE

**Transitions**:
- COMPLETE → INCOMPLETE (state change)
- INCOMPLETE → INCOMPLETE (idempotent - no state change)

**Implementation**:
```python
def mark_incomplete(task_id: str) -> Task:
    # Get task (raises KeyError if not found)
    task = tasks[task_id]

    # Create new task with INCOMPLETE status
    updated_task = Task(
        id=task.id,
        title=task.title,
        description=task.description,
        status=TaskStatus.INCOMPLETE,  # Always INCOMPLETE
        created=task.created
    )

    # Update storage
    tasks[task_id] = updated_task
    return updated_task
```

**Idempotent Behavior**: If task is already INCOMPLETE, return task with INCOMPLETE status (no error)

---

#### 3. Toggle Status (toggle_status)

**Precondition**: Task exists in storage
**Postcondition**: Task status is opposite of original status

**Transitions**:
- INCOMPLETE → COMPLETE (flip)
- COMPLETE → INCOMPLETE (flip)

**Implementation**:
```python
def toggle_status(task_id: str) -> Task:
    # Get task (raises KeyError if not found)
    task = tasks[task_id]

    # Determine new status (flip current status)
    new_status = (
        TaskStatus.COMPLETE
        if task.status == TaskStatus.INCOMPLETE
        else TaskStatus.INCOMPLETE
    )

    # Create new task with flipped status
    updated_task = Task(
        id=task.id,
        title=task.title,
        description=task.description,
        status=new_status,  # Flipped status
        created=task.created
    )

    # Update storage
    tasks[task_id] = updated_task
    return updated_task
```

**Toggle Logic**: Uses simple conditional (if INCOMPLETE then COMPLETE, else INCOMPLETE)

---

## Storage Model

### Storage Structure

**Type**: `Dict[str, Task]`
**Module**: `src/services/task_service.py`

**Structure**:
```python
tasks: Dict[str, Task] = {}

# Example state:
{
    "abc-123": Task(id="abc-123", title="Buy milk", ..., status=TaskStatus.INCOMPLETE),
    "xyz-789": Task(id="xyz-789", title="Write report", ..., status=TaskStatus.COMPLETE),
}
```

**Key**: Task ID (UUID5 string)
**Value**: Task instance

---

### Storage Mutation Pattern

**Pattern**: Replace-in-place (consistent with Update Task)

**Steps**:
1. Retrieve task from storage (raises KeyError if not found)
2. Create new Task instance with updated status
3. Replace task in storage dict using same key
4. Return new task instance

**Code Pattern**:
```python
def mark_complete(task_id: str) -> Task:
    # Step 1: Retrieve
    if task_id not in tasks:
        raise KeyError(f"Task not found with ID: {task_id}")
    task = tasks[task_id]

    # Step 2: Create new instance
    updated_task = Task(
        id=task.id,
        title=task.title,
        description=task.description,
        status=TaskStatus.COMPLETE,
        created=task.created
    )

    # Step 3: Replace
    tasks[task_id] = updated_task

    # Step 4: Return
    return updated_task
```

**Rationale**:
- Maintains Task immutability (no in-place modification)
- Triggers Task validation in `__post_init__()`
- Consistent with existing `update_task()` pattern
- Dict replacement is O(1) operation

---

## Validation Rules

### Task ID Validation

**Where**: Service layer (all three functions)

**Rule**: Task ID must exist in storage
**Error**: Raise `KeyError` if task ID not found
**Message**: `"Task not found with ID: {task_id}"`

**Implementation**:
```python
if task_id not in tasks:
    raise KeyError(f"Task not found with ID: {task_id}")
```

---

### Status Validation

**Where**: Task dataclass `__post_init__()`

**Rule**: Status must be a TaskStatus enum member
**Error**: Raise `ValueError` if status is invalid (handled by dataclass)

**Note**: Service layer creates Task instances with valid TaskStatus values (INCOMPLETE or COMPLETE) - no additional validation needed.

---

## Invariants

1. **Task ID Uniqueness**: Each task has a unique ID (UUID5)
2. **Status Validity**: Task status is always INCOMPLETE or COMPLETE (enforced by TaskStatus enum)
3. **Field Completeness**: All Task fields are required (no None values)
4. **Storage Consistency**: Task ID in storage dict matches Task.id field
5. **Immutability**: Task instances are never modified in-place (replaced in storage)

---

## Edge Cases

### 1. Idempotent State Assignment

**Scenario**: Mark complete task as complete
**Behavior**:
- Service returns task with COMPLETE status
- CLI displays success message
- Exit code 0

**Data Flow**:
```python
# Before: task.status = TaskStatus.COMPLETE
task = mark_complete(task_id)
# After: task.status = TaskStatus.COMPLETE (no change)
```

---

### 2. Non-Existent Task ID

**Scenario**: Attempt to change status of task that doesn't exist
**Behavior**:
- Service raises KeyError
- CLI catches exception
- CLI displays error message: "Error: Task not found with ID: {task_id}"
- Exit code 1

**Data Flow**:
```python
try:
    task = mark_complete("non-existent-id")
except KeyError:
    # CLI handles error
    print(f"Error: Task not found with ID: non-existent-id", file=sys.stderr)
    sys.exit(1)
```

---

### 3. Empty Task List

**Scenario**: Attempt to change status when no tasks exist
**Behavior**: Same as non-existent task ID (KeyError → error message)

**Data Flow**:
```python
tasks = {}  # Empty storage
try:
    task = mark_complete("any-id")
except KeyError:
    # CLI handles error
    print(f"Error: Task not found with ID: any-id", file=sys.stderr)
    sys.exit(1)
```

---

## Summary

- **No model changes required**: Reuse existing Task and TaskStatus
- **Three service functions**: `mark_complete()`, `mark_incomplete()`, `toggle_status()`
- **Immutability pattern**: Create new Task instance for status changes
- **Idempotent operations**: Always return task with desired status (no error)
- **Storage mutation**: Replace task in dict (O(1) operation)
- **Validation**: Task ID existence check only (status validation via Task dataclass)
