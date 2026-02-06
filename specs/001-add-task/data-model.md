# Data Model: Add Task Feature

**Feature**: Add Task
**Date**: 2025-12-31
**Version**: 1.0
**Source**: Derived from spec.md requirements and research.md decisions

## Overview

This document defines the data structures and their relationships for the Add Task feature. The model is technology-agnostic in design but includes Python-specific implementation notes based on research findings.

## Entities

### Task

**Purpose**: Represents a single todo item in the system

**Attributes**:

| Attribute | Type | Required | Default | Constraints | Description |
|-----------|------|----------|---------|-------------|-------------|
| id | String (UUID) | Yes | Generated | Unique, deterministic, immutable | Task identifier generated using UUID5 |
| title | String | Yes | None | Non-empty, max 500 chars, trimmed | Short description of the task |
| description | String | No | Empty string | Max 5000 chars | Detailed context for the task |
| status | Enum | Yes | INCOMPLETE | One of: INCOMPLETE, COMPLETE | Current completion state |
| created | DateTime | Yes | Now | ISO 8601 format, immutable | Timestamp when task was created |

**Validation Rules**:

1. **Title Validation**:
   - MUST NOT be empty string after trimming whitespace
   - MUST NOT exceed 500 characters
   - MUST preserve exact user input (capitalization, internal spacing)
   - Example valid: "  Buy groceries  " → stored as "Buy groceries" (trimmed) OR preserved exactly per FR-009
   - Example invalid: "", "   ", null

2. **Description Validation**:
   - MAY be empty (optional field)
   - MUST NOT exceed 5000 characters
   - MUST preserve exact user input (capitalization, spacing, newlines)

3. **ID Validation**:
   - MUST be unique across all tasks in current session
   - MUST be deterministic (same inputs → same ID for testing)
   - MUST NOT be user-editable

4. **Status Validation**:
   - MUST be one of the defined TaskStatus enum values
   - Defaults to INCOMPLETE on creation

5. **Created Timestamp Validation**:
   - MUST be set at task creation time
   - MUST NOT be user-editable
   - MUST be in ISO 8601 format for display

**Invariants**:
- Once created, `id` and `created` fields are immutable
- `title` can be modified later (Update Task feature) but never empty
- `status` transitions only between INCOMPLETE ↔ COMPLETE (no other states in Phase I)

---

### TaskStatus (Enumeration)

**Purpose**: Represents the completion state of a task

**Values**:

| Value | Display Name | Description | Transitions |
|-------|--------------|-------------|-------------|
| INCOMPLETE | Incomplete | Task not yet completed (default state) | → COMPLETE (via Mark Complete) |
| COMPLETE | Complete | Task has been completed | → INCOMPLETE (via Mark Incomplete) |

**Rules**:
- New tasks always start in INCOMPLETE state
- State transitions handled by Mark Complete/Incomplete feature (not Add Task)
- No intermediate states in Phase I (e.g., no "IN_PROGRESS", "BLOCKED")

---

## Relationships

**Phase I Scope**: No relationships between entities (Task is the only entity)

**Future Considerations** (not implemented in Phase I):
- Task → User (owner relationship for multi-user support)
- Task → Tags (many-to-many for categorization)
- Task → Subtasks (hierarchical relationship)
- Task → Project (grouping relationship)

---

## Storage Structure

**In-Memory Storage**: Dictionary mapping task IDs to Task objects

```
TaskStorage = {
    "task-uuid-1": Task(id="task-uuid-1", title="Buy groceries", ...),
    "task-uuid-2": Task(id="task-uuid-2", title="Call dentist", ...),
    ...
}
```

**Storage Characteristics**:
- **Type**: Python `dict[str, Task]`
- **Scope**: Module-level variable in `task_service.py`
- **Lifetime**: Application session (cleared on exit, not persisted)
- **Concurrency**: Single-threaded (no locking needed in Phase I)
- **Capacity**: Tested up to 10,000 tasks (SC-002 performance goal)

**Access Patterns**:
1. **Add Task**: `storage[new_task.id] = new_task` - O(1)
2. **Get by ID**: `storage[task_id]` - O(1)
3. **List all**: `storage.values()` - O(n)
4. **Delete**: `del storage[task_id]` - O(1)

---

## Data Flow

### Task Creation Flow

```
User Input (CLI)
    ↓
1. Parse arguments (argparse)
    title: str (required)
    description: str (optional, default="")
    ↓
2. Validate title
    - Strip whitespace
    - Check non-empty
    - Check length ≤ 500
    ↓
3. Validate description (if provided)
    - Check length ≤ 5000
    ↓
4. Generate task ID
    - UUID5(namespace, f"task-{timestamp}-{counter}")
    ↓
5. Create Task object
    - id: generated UUID
    - title: validated title
    - description: validated description (or "")
    - status: TaskStatus.INCOMPLETE
    - created: datetime.now()
    ↓
6. Store in memory
    - tasks[task.id] = task
    ↓
7. Return confirmation
    - Display: "Task created: {task.id}"
```

**Error Paths**:
- Empty title → Validation error → Display error message → Exit code 1
- Title too long → Validation error → Display error message → Exit code 1
- Description too long → Validation error → Display error message → Exit code 1

---

## Implementation Notes (Python-Specific)

### Task Dataclass

```python
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import uuid

class TaskStatus(Enum):
    INCOMPLETE = "incomplete"
    COMPLETE = "complete"

@dataclass
class Task:
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
            raise ValueError("Title cannot exceed 500 characters")

        # Description validation
        if len(self.description) > 5000:
            raise ValueError("Description cannot exceed 5000 characters")
```

**Dataclass Benefits**:
- Auto-generates `__init__`, `__repr__`, `__eq__`
- Type hints for all fields
- Default values for optional fields
- `__post_init__` for validation logic

---

## Validation Summary

| Field | Validation | Error Message | Exit Code |
|-------|------------|---------------|-----------|
| title (empty) | `if not title.strip()` | "Error: Title cannot be empty" | 1 |
| title (too long) | `if len(title) > 500` | "Error: Title cannot exceed 500 characters" | 1 |
| description (too long) | `if len(description) > 5000` | "Error: Description cannot exceed 5000 characters" | 1 |
| id (duplicate) | `if id in tasks` | "Error: Task ID collision (internal error)" | 2 |

**Validation Strategy**:
- **Early validation**: Check inputs before creating Task object
- **Defensive validation**: Task dataclass re-validates in `__post_init__`
- **Clear errors**: User-friendly messages, specific to the problem

---

## Testing Considerations

### Unit Test Cases (Task Model)

1. **Valid task creation**:
   - Title only: `Task(id="123", title="Buy milk")` → Success
   - Title + description: `Task(id="123", title="Buy milk", description="From store")` → Success

2. **Edge cases**:
   - Whitespace title: `Task(id="123", title="   ")` → ValueError
   - Max length title: `Task(id="123", title="a"*500)` → Success
   - Over-length title: `Task(id="123", title="a"*501)` → ValueError
   - Max length description: `Task(..., description="a"*5000)` → Success
   - Over-length description: `Task(..., description="a"*5001)` → ValueError

3. **Special characters**:
   - Unicode: `Task(id="123", title="Café ☕")` → Success
   - Newlines in description: `Task(..., description="Line1\nLine2")` → Success
   - Quotes: `Task(id="123", title='She said "hi"')` → Success

4. **Default values**:
   - No description: `Task(id="123", title="Test")` → description=""
   - Default status: `Task(id="123", title="Test")` → status=INCOMPLETE
   - Auto timestamp: `Task(id="123", title="Test")` → created=datetime.now()

### Integration Test Cases

1. **CLI to model**:
   - `todo add "Buy milk"` → Task created with title="Buy milk"
   - `todo add "Buy milk" -d "From store"` → Task with both fields

2. **ID uniqueness**:
   - Add 1000 tasks → Verify 1000 unique IDs

3. **Persistence boundary**:
   - Add task → Verify in storage → Exit app → Restart → Verify storage empty

---

## Acceptance Mapping

This data model satisfies the following spec requirements:

- **FR-001**: Task accepts title (required field in dataclass)
- **FR-002**: Unique ID generation (UUID5 deterministic approach)
- **FR-003**: Default status INCOMPLETE (dataclass default)
- **FR-004**: In-memory storage (dict structure)
- **FR-005**: Optional description (dataclass default="")
- **FR-006**: Title validation (non-empty check in `__post_init__`)
- **FR-007**: Confirmation with ID (return Task object from service)
- **FR-008**: Validation error handling (ValueError with clear messages)
- **FR-009**: Text preservation (no transformation except title trim)

---

## Future Evolution (Not in Phase I)

**Phase II Considerations** (when adding persistence):
- Add `updated: datetime` field for modification tracking
- Add `version: int` field for optimistic locking
- Add `deleted: bool` field for soft deletes

**Multi-User Considerations** (future):
- Add `owner_id: str` field for user ownership
- Add `shared_with: list[str]` for collaboration

**Advanced Features** (future):
- Add `priority: enum` (LOW, MEDIUM, HIGH)
- Add `due_date: datetime` for deadlines
- Add `tags: list[str]` for categorization
- Add `parent_id: str` for subtask hierarchy
