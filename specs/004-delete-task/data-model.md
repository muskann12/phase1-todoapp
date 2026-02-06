# Data Model: Delete Task

**Feature**: Delete Task (004-delete-task)
**Date**: 2025-12-31
**Status**: Complete

## Overview

This document describes the data model and storage operations for the Delete Task feature. The Delete Task feature reuses the existing Task entity and storage structure with no schema modifications required.

## Entity: Task

**Source**: `src/models/task.py` (existing, no changes)

The Task dataclass represents a single todo item with the following attributes:

```python
@dataclass
class Task:
    """Represents a single todo item"""
    id: str                      # Unique identifier (UUID5 format)
    title: str                   # Task title (1-500 characters, required)
    description: str = ""        # Task description (0-5000 characters, optional)
    status: TaskStatus = TaskStatus.INCOMPLETE  # Task completion status
    created: datetime = field(default_factory=datetime.now)  # Creation timestamp
```

### Task Status Enum

```python
class TaskStatus(Enum):
    """Task completion status"""
    INCOMPLETE = "incomplete"
    COMPLETE = "complete"
```

## Storage Structure

**Location**: `src/services/task_service.py`

**Storage Type**: In-memory dictionary

```python
_tasks: Dict[str, Task] = {}
```

**Key**: Task ID (str) - UUID5 formatted string
**Value**: Task object - Complete Task dataclass instance

## Delete Operation

### Function Signature

```python
def delete_task(task_id: str) -> Task:
    """
    Delete a task from in-memory storage.

    Args:
        task_id: Unique task identifier (UUID5 format)

    Returns:
        Task: The deleted task object (captured before removal)

    Raises:
        KeyError: If task ID not found in storage
    """
```

### Storage Mutation

**Before deletion**:
```python
_tasks = {
    "task-123-abc": Task(id="task-123-abc", title="Buy milk", ...),
    "task-456-def": Task(id="task-456-def", title="Walk dog", ...),
    "task-789-ghi": Task(id="task-789-ghi", title="Call John", ...)
}
```

**Delete operation**: `delete_task("task-456-def")`

**After deletion**:
```python
_tasks = {
    "task-123-abc": Task(id="task-123-abc", title="Buy milk", ...),
    "task-789-ghi": Task(id="task-789-ghi", title="Call John", ...)
}
```

**Returned object**: Task(id="task-456-def", title="Walk dog", ...)

### Implementation Details

**Lookup & Delete**:
```python
# Check if task exists
if task_id not in _tasks:
    raise KeyError(f"Task not found with ID: {task_id}")

# Remove from storage and capture deleted task
deleted_task = _tasks.pop(task_id)

# Return deleted task for confirmation message
return deleted_task
```

**Time Complexity**: O(1) - Dictionary lookup and deletion
**Space Complexity**: O(1) - No additional storage, removes one entry

## Validation Rules

**Task ID Validation**:
- **Format**: Any string accepted (lenient validation)
- **Existence Check**: Task ID MUST exist in `_tasks` dictionary
- **Error Handling**: Raise KeyError if task ID not found

**No Schema Validation Required**:
- Task object is already validated (retrieved from storage, not modified)
- No field updates or validations needed (unlike Add Task or Update Task)

## Immutability Considerations

**Task Fields**: All task fields remain unchanged during deletion operation
- ID remains the same (used for lookup)
- Title, description, status, created timestamp all unchanged
- Task object is returned as-is before removal from storage

**Storage Immutability**: Dictionary mutation is permanent
- Once removed, task is not recoverable (no undo mechanism in Phase I)
- No soft delete, no archive, no trash (spec assumption A-006)

## Data Flow

### Successful Deletion Flow

```text
1. CLI receives task_id from user
   ↓
2. CLI calls delete_task(task_id) service function
   ↓
3. Service checks if task_id exists in _tasks
   ↓
4. Service calls _tasks.pop(task_id) to remove and capture task
   ↓
5. Service returns deleted Task object to CLI
   ↓
6. CLI displays task details in confirmation message
   ↓
7. CLI exits with code 0 (success)
```

### Error Flow (Task Not Found)

```text
1. CLI receives task_id from user
   ↓
2. CLI calls delete_task(task_id) service function
   ↓
3. Service checks if task_id exists in _tasks
   ↓
4. Task not found → Service raises KeyError
   ↓
5. CLI catches KeyError
   ↓
6. CLI displays error message to stderr
   ↓
7. CLI exits with code 1 (not found)
```

## State Transitions

**Task State**: No state transitions (task is removed entirely)

**Storage State Transitions**:
- **Before**: Task exists in `_tasks` dictionary
- **After**: Task removed from `_tasks` dictionary (not recoverable)

## Relationship to Other Features

### Add Task (001-add-task)
- **Relationship**: Creates tasks that can later be deleted
- **Dependency**: Must have tasks in storage before deletion is possible
- **Data Flow**: Add Task populates `_tasks` → Delete Task removes from `_tasks`

### View Task List (002-view-task-list)
- **Relationship**: Displays task IDs that users need for deletion
- **Dependency**: Users discover task IDs via View Task List
- **Data Flow**: View Task List reads `_tasks` → User copies ID → Delete Task removes from `_tasks`

### Update Task (003-update-task)
- **Relationship**: Alternative to deletion (modify instead of remove)
- **Dependency**: No dependency (orthogonal operations)
- **Data Flow**: Both operate on `_tasks`, but different operations (update vs remove)

## Edge Cases

### 1. Non-Existent Task ID
**Scenario**: User provides task ID that doesn't exist in storage
**Behavior**: `delete_task()` raises KeyError
**CLI Response**: Display error "Error: Task not found with ID: {task_id}" and exit with code 1

### 2. Empty Storage
**Scenario**: User tries to delete from empty task list (`_tasks = {}`)
**Behavior**: Same as non-existent task ID (KeyError)
**CLI Response**: Display error "Error: Task not found with ID: {task_id}" and exit with code 1

### 3. Delete Same Task Twice
**Scenario**: User deletes task, then tries to delete same ID again in same session
**Behavior**: Second deletion raises KeyError (task already removed)
**CLI Response**: Display error "Error: Task not found with ID: {task_id}" and exit with code 1

### 4. Task with Unicode Characters
**Scenario**: Delete task that has Unicode characters in title/description
**Behavior**: Task deleted normally, Unicode characters displayed in confirmation
**CLI Response**: Display deleted task details with Unicode characters correctly rendered

### 5. Delete Task with Any Status
**Scenario**: Delete task that is marked complete or incomplete
**Behavior**: Status doesn't affect deletion (FR-009)
**CLI Response**: Display deleted task with status field shown correctly

## Testing Scenarios

### Unit Tests (Service Layer)
1. Delete existing task → Returns Task object with correct fields
2. Delete task → Verify task removed from `_tasks` storage
3. Delete non-existent task → Raises KeyError
4. Delete completed task → Works same as incomplete task
5. Delete task with Unicode → Returns task with Unicode intact
6. Delete from storage with multiple tasks → Only deletes specified task

### Integration Tests (CLI Layer)
1. Delete command success → Displays correct confirmation message format
2. Delete non-existent ID → Displays correct error message
3. Delete --help → Displays correct usage information
4. Delete without task ID → Displays missing argument error

## Schema Changes

**None required.** Delete Task feature reuses existing Task entity and storage structure with no modifications.

## Future Considerations (Out of Scope for Phase I)

### Soft Delete Pattern (Phase II)
- Add `deleted: bool` field to Task dataclass
- Add `deleted_at: datetime` field to capture deletion timestamp
- Modify View Task List to filter out deleted tasks by default
- Add "undo delete" or "restore" functionality

### Deletion History (Phase II)
- Add separate `_deleted_tasks` dictionary for audit trail
- Track who deleted (multi-user support)
- Track when deleted (timestamp)
- Enable deletion history queries

### Bulk Delete (Phase II)
- Accept multiple task IDs as arguments
- Delete by criteria (e.g., all completed tasks)
- Delete by date range

**Note**: All future considerations require persistence layer (database) and are out of scope for Phase I in-memory implementation.
