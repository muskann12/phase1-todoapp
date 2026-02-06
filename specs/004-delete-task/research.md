# Technical Research: Delete Task

**Feature**: Delete Task (004-delete-task)
**Date**: 2025-12-31
**Status**: Complete

## Overview

This document captures technical decisions and research findings for implementing the Delete Task feature in the Evolution of Todo Phase I CLI application.

## Research Questions & Decisions

### 1. Delete Function Return Value

**Question**: Should `delete_task()` return the deleted Task object or return nothing (void)?

**Options Considered**:
- **Option A**: Return deleted Task object before removal
- **Option B**: Void function (no return value)
- **Option C**: Return boolean (True if deleted, False if not found)

**Decision**: **Option A** - Return deleted Task object

**Rationale**:
- Enables confirmation message to show user what was deleted (SC-003: "System provides clear confirmation message showing what was deleted")
- Follows spec requirement FR-004: "System MUST display success message showing deleted task's ID, title, and description"
- Consistent with pattern from other features (Add Task returns created Task, Update Task returns updated Task)
- No additional storage lookup needed - capture Task before deletion and return it

**Alternatives Rejected**:
- Option B rejected: Cannot display deleted task details without separate storage lookup before deletion
- Option C rejected: Boolean doesn't provide task details needed for confirmation message

---

### 2. Deletion Confirmation Strategy

**Question**: Should users be prompted to confirm deletion before it happens?

**Options Considered**:
- **Option A**: No confirmation prompt (user must be intentional)
- **Option B**: Interactive prompt "Are you sure? (y/n)"
- **Option C**: Require `--force` flag for actual deletion

**Decision**: **Option A** - No confirmation prompt

**Rationale**:
- Spec assumption A-005 explicitly states: "No confirmation prompt required before deletion (user must be intentional with command)"
- Phase I constraint: CLI-only interface, no interactive prompts
- Follows standard Unix/Linux tool behavior (rm, git branch -d, etc.) - user types command intentionally
- User gets confirmation AFTER deletion showing what was removed (prevention of accidental confusion, not accidental execution)

**Alternatives Rejected**:
- Option B rejected: Violates Phase I CLI-only constraint, adds interactive complexity
- Option C rejected: Not specified in requirements, adds unnecessary friction for simple operation

---

### 3. Storage Deletion Method

**Question**: What Python dict operation should be used to remove tasks from `_tasks` storage?

**Options Considered**:
- **Option A**: `deleted_task = _tasks.pop(task_id)` (returns deleted value)
- **Option B**: `del _tasks[task_id]` (no return value)
- **Option C**: `_tasks.pop(task_id, None)` (returns None if not found)

**Decision**: **Option A** - Use `dict.pop(task_id)`

**Rationale**:
- Returns deleted Task object in one operation (O(1) time complexity)
- Raises KeyError if task doesn't exist (matches existing error handling pattern from `get_task()`)
- Atomic operation - no race conditions in single-process CLI
- Cleaner than separate lookup + delete operations

**Alternatives Rejected**:
- Option B rejected: Requires separate Task lookup before deletion to get return value
- Option C rejected: Suppresses KeyError, contradicts spec requirement FR-005 (MUST display error when ID doesn't exist)

**Implementation Pattern**:
```python
def delete_task(task_id: str) -> Task:
    """Delete a task and return the deleted Task object."""
    if task_id not in _tasks:
        raise KeyError(f"Task not found with ID: {task_id}")

    deleted_task = _tasks.pop(task_id)
    return deleted_task
```

---

### 4. Error Message Format

**Question**: What error message format should be used for non-existent task IDs?

**Options Considered**:
- **Option A**: "Error: Task not found with ID: {task_id}"
- **Option B**: "Task {task_id} does not exist"
- **Option C**: "Cannot delete task {task_id}: not found"

**Decision**: **Option A** - "Error: Task not found with ID: {task_id}"

**Rationale**:
- Matches exact format specified in spec.md edge cases and FR-005
- Consistent with Update Task error messages (same error for non-existent ID)
- Clear prefix "Error:" distinguishes from success messages
- Includes task ID in error for user verification (prevents confusion about which ID was used)

**Alternatives Rejected**:
- Option B rejected: Doesn't match spec format, no "Error:" prefix
- Option C rejected: Unnecessarily verbose, not specified in requirements

---

### 5. CLI Argument Structure

**Question**: Should task ID be a positional argument or a flag (e.g., `--id`)?

**Options Considered**:
- **Option A**: Positional argument: `delete <task_id>`
- **Option B**: Flag argument: `delete --id <task_id>`
- **Option C**: Both supported (positional or flag)

**Decision**: **Option A** - Required positional argument

**Rationale**:
- Spec requirement FR-002: "System MUST accept task ID as a required positional argument via CLI"
- Simpler user experience (fewer characters to type)
- Consistent with Update Task command structure (`update <task_id> [flags]`)
- Standard CLI pattern for simple operations (e.g., `rm file.txt`, `git branch -d branch-name`)

**Alternatives Rejected**:
- Option B rejected: More verbose, not specified in requirements
- Option C rejected: Adds complexity for no benefit, spec explicitly states positional argument

---

### 6. Success Message Format

**Question**: What information should be included in the deletion success message?

**Options Considered**:
- **Option A**: Show all task fields (ID, title, description, status)
- **Option B**: Show only ID and title
- **Option C**: Simple "Task deleted successfully" with no details

**Decision**: **Option A** - Show all task fields

**Rationale**:
- Spec requirement FR-004: "System MUST display success message showing deleted task's ID, title, and description (if present)"
- SC-003: "System provides clear confirmation message showing what was deleted (ID, title, description)"
- Matches Add Task and Update Task success message format (consistency)
- Helps user verify correct task was deleted (especially important for permanent deletion)

**Format**:
```text
Task deleted successfully!
ID: <task_id>
Title: <title>
Description: <description or "(none)">
Status: <Complete|Incomplete>
```

**Alternatives Rejected**:
- Option B rejected: Doesn't meet FR-004 requirement (must show description)
- Option C rejected: No verification for user, violates SC-003

---

### 7. Exit Codes

**Question**: What exit codes should be used for different scenarios?

**Options Considered**:
- **Option A**: 0 (success), 1 (not found), 2 (argparse error)
- **Option B**: 0 (success), 1 (any error)
- **Option C**: 0 (success), 1 (not found), 2 (validation), 3 (system error)

**Decision**: **Option A** - Three exit codes (0, 1, 2)

**Rationale**:
- Matches spec requirements FR-006, FR-007, FR-008
- Consistent with Add Task and Update Task exit code patterns
- Exit code 0: Success (standard Unix convention)
- Exit code 1: Task not found (business logic error)
- Exit code 2: Missing argument (argparse validation error)

**Alternatives Rejected**:
- Option B rejected: Less granular, can't distinguish between error types
- Option C rejected: Over-engineered for simple CLI, not specified in requirements

---

### 8. Unicode Character Handling

**Question**: How should Unicode characters in task data be handled during deletion?

**Options Considered**:
- **Option A**: Display Unicode characters natively (UTF-8)
- **Option B**: Escape Unicode characters (e.g., \u1234)
- **Option C**: Strip/replace Unicode with ASCII

**Decision**: **Option A** - Display Unicode characters natively

**Rationale**:
- Python 3.13+ has native Unicode support (UTF-8 encoding)
- Spec requirement FR-010: "System MUST correctly display Unicode characters in deleted task confirmation message"
- SC-006: "Unicode characters in task data are correctly displayed in deletion confirmation message"
- Consistent with existing Add Task, View Task List, and Update Task features

**Alternatives Rejected**:
- Option B rejected: Makes output harder to read, not user-friendly
- Option C rejected: Data loss, violates spec requirement

---

## Technology Stack Summary

**No new dependencies required.** All functionality implemented using:

1. **Python 3.13+ Standard Library**:
   - `argparse` - CLI argument parsing
   - `sys` - Exit codes and stderr
   - `dataclasses` - Task model (existing, no changes)
   - `uuid` - Task ID format (existing, no changes)
   - `datetime` - Timestamp handling (existing, no changes)

2. **Testing**:
   - `pytest` - Test framework (existing)
   - `subprocess` - CLI integration testing (existing pattern)

3. **Storage**:
   - In-memory `Dict[str, Task]` in `src/services/task_service.py` (existing)

---

## Best Practices Applied

1. **Service Layer Separation**: Business logic in `delete_task()` service function, CLI concerns in `delete_task.py` CLI module
2. **Error Handling Pattern**: Service raises KeyError, CLI catches and translates to user-friendly message
3. **Return Deleted Object**: Enables confirmation message without additional lookup
4. **Test-First Development**: Unit tests → Integration tests → Implementation → Validation
5. **Consistency**: Follows exact patterns from Add Task, View Task List, and Update Task features

---

## Open Questions

**None.** All technical decisions resolved.

---

## References

- Spec: `specs/004-delete-task/spec.md`
- Constitution: `.specify/memory/constitution.md`
- Existing Patterns:
  - `specs/001-add-task/plan.md`
  - `specs/002-view-task-list/plan.md`
  - `specs/003-update-task/plan.md`
