# Data Model: View Task List Feature

**Feature**: View Task List
**Date**: 2025-12-31
**Purpose**: Phase 1 data model specification (reuses existing Add Task entities)

## Entity Overview

**View Task List is a read-only feature** - it does NOT introduce new entities. All data structures are reused from the Add Task feature implementation.

---

## Existing Entities (Reference Only)

### Task Entity

**Defined in**: `src/models/task.py` (from Add Task feature)

**Purpose**: Represents a single todo item with title, description, status, and metadata

**Fields**:

| Field | Type | Required | Default | Validation | Description |
|-------|------|----------|---------|------------|-------------|
| `id` | `str` | Yes | (generated) | UUID5 format | Unique deterministic task identifier |
| `title` | `str` | Yes | - | 1-500 chars, non-empty after strip | Task title (primary identifier for users) |
| `description` | `str` | No | `""` | Max 5000 chars | Optional task details |
| `status` | `TaskStatus` | Yes | `TaskStatus.INCOMPLETE` | Enum value | Completion status (incomplete/complete) |
| `created` | `datetime` | Yes | `datetime.now()` | ISO 8601 format | Creation timestamp |

**Constraints**:
- Title MUST NOT be empty or whitespace-only after stripping
- Title MUST NOT exceed 500 characters
- Description MUST NOT exceed 5000 characters
- ID is immutable after creation
- Status can only be `INCOMPLETE` or `COMPLETE`

**Validation Logic** (in `Task.__post_init__`):
```python
def __post_init__(self):
    self.title = self.title.strip()
    if not self.title:
        raise ValueError("Title cannot be empty")
    if len(self.title) > 500:
        raise ValueError(f"Title cannot exceed 500 characters (provided: {len(self.title)})")
    if len(self.description) > 5000:
        raise ValueError(f"Description cannot exceed 5000 characters (provided: {len(self.description)})")
```

---

### TaskStatus Enum

**Defined in**: `src/models/task.py` (from Add Task feature)

**Purpose**: Type-safe representation of task completion status

**Values**:
```python
class TaskStatus(Enum):
    INCOMPLETE = "incomplete"
    COMPLETE = "complete"
```

**Usage in View Task List**:
- Read status to determine display icon: `[ ]` for INCOMPLETE, `[✓]` for COMPLETE
- Count incomplete vs complete tasks for summary (User Story 2)
- Display status text: `task.status.value.capitalize()` → "Incomplete" or "Complete"

---

## Storage Structure (Reference Only)

### In-Memory Task Dictionary

**Defined in**: `src/services/task_service.py` (from Add Task feature)

**Structure**:
```python
_tasks: Dict[str, Task] = {}
```

**Access Pattern for View Task List**:
- **Read-only access**: `_tasks.values()` returns all Task objects
- **No mutations**: View feature MUST NOT modify `_tasks` dict
- **Sorted access**: `sorted(_tasks.values(), key=lambda t: t.id)`

**Guarantee**: View operation does not add, remove, or modify any tasks (read-only)

---

## Data Flow for View Task List

```text
User runs CLI command
        ↓
view_tasks_command() in src/cli/view_tasks.py
        ↓
get_all_tasks() in src/services/task_service.py
        ↓
sorted(_tasks.values(), key=lambda t: t.id)  [Read-only - no mutation]
        ↓
Return list[Task] sorted by ID ascending
        ↓
Format and display each task in CLI
        ↓
Display summary counts (total, incomplete, complete)
        ↓
Exit with code 0
```

**Key Principle**: Data flows ONE-WAY (storage → service → CLI → user). No write-back to storage.

---

## No New Entities Required

**Why no new entities?**
- View Task List is purely a read operation
- All necessary data (Task objects) already exists from Add Task feature
- Summary counts are computed on-the-fly (not persisted)
- Display formatting is presentation logic (not data model)

**Future Considerations** (Out of Scope for Phase I):
- Filter criteria entities (e.g., TaskFilter with status/date range) - Phase II or later
- Sort preference entity - Phase II or later
- View configuration (e.g., show/hide fields) - Phase II or later

---

## Data Consistency Requirements

### Read-Only Guarantees

**Pre-condition**: Tasks exist in `_tasks` dict (created via Add Task)

**During View Operation**:
- `_tasks` dict MUST NOT be modified (no add, update, delete)
- Task objects MUST NOT be mutated (no field changes)
- Sort operation creates new list (temporary), does not modify original dict

**Post-condition**:
- `_tasks` dict unchanged (same keys, same Task object references)
- Task count unchanged
- Individual task fields unchanged

**Testing Verification**:
```python
def test_view_does_not_modify_storage():
    # Pre-condition: Create 3 tasks
    task1 = create_task("Task 1")
    task2 = create_task("Task 2")
    task3 = create_task("Task 3")

    # Capture state before view
    tasks_before = get_all_tasks()
    count_before = len(tasks_before)

    # Execute view operation
    view_tasks_command()

    # Verify no changes
    tasks_after = get_all_tasks()
    count_after = len(tasks_after)

    assert count_before == count_after
    assert tasks_before == tasks_after  # Same task objects
```

---

## Summary

**Reused from Add Task**:
- ✅ Task entity (id, title, description, status, created)
- ✅ TaskStatus enum (INCOMPLETE, COMPLETE)
- ✅ In-memory storage dict (_tasks)

**New for View Task List**:
- ❌ No new entities
- ❌ No new data structures
- ✅ New service function: `get_all_tasks()` (returns sorted list)
- ✅ New CLI module: `view_tasks.py` (display logic only, no data model)

**Read-Only Principle**: View Task List operates entirely in read mode - zero data modifications.
