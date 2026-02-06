# Feature Specification: Delete Task

**Feature Branch**: `004-delete-task`
**Created**: 2025-12-31
**Status**: Draft
**Input**: User description: "Delete Task feature for an in-memory Python CLI Todo application. Allow the user to delete an existing todo task using its unique task ID via a command-line interface."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Delete Task by ID (Priority: P1) 🎯 MVP

A user needs to remove a completed or obsolete task from their todo list using the task's unique identifier.

**Why this priority**: Core deletion functionality - allows users to maintain a clean, relevant task list by removing unwanted tasks. This is essential for task list hygiene and provides immediate value.

**Independent Test**: Create a task, delete it using its task ID, verify task is removed from storage and no longer appears in task list.

**Acceptance Scenarios**:

1. **Given** a task exists with ID "abc-123" and title "Buy milk"
   **When** user runs `delete abc-123`
   **Then** task with ID "abc-123" is removed from storage and success message displays "Task deleted successfully! ID: abc-123, Title: Buy milk"

2. **Given** multiple tasks exist with IDs "abc-123", "xyz-789", "def-456"
   **When** user runs `delete xyz-789`
   **Then** only task "xyz-789" is removed and tasks "abc-123" and "def-456" remain in storage

3. **Given** a task exists with ID "abc-123", title "Complete report", and description "Q4 financial summary"
   **When** user runs `delete abc-123`
   **Then** task is removed and success message displays task ID, title, and description before deletion

---

### Edge Cases

- **Non-existent Task ID**: What happens when user provides an ID that doesn't exist? → System displays error message "Error: Task not found with ID: [id]" and exits with non-zero code (exit code 1)

- **Invalid ID Format**: What happens when user provides malformed ID? → System displays error "Error: Task not found with ID: [id]" (ID validation is lenient - if not found, show error regardless of format)

- **Empty Task List**: What happens when user tries to delete from an empty task list? → System displays error "Error: Task not found with ID: [id]" (same error as non-existent ID)

- **Delete Same Task Twice**: What happens when user tries to delete a task that was already deleted in the current session? → System displays error "Error: Task not found with ID: [id]" (task no longer exists in storage)

- **No Task ID Provided**: What happens when user runs `delete` without providing a task ID? → System displays error "Error: Task ID is required" and shows usage help with exit code 2 (argparse validation error)

- **Deletion is Permanent**: Once deleted, can the task be recovered? → No, deletion is permanent for the current session (no undo/recovery mechanism in Phase I)

- **Task Status Independence**: Can tasks with any status (complete/incomplete) be deleted? → Yes, both completed and incomplete tasks can be deleted (status doesn't affect deletion)

- **Unicode in Task Data**: What happens when deleting a task with Unicode characters in title/description? → Task is deleted normally and success message displays Unicode characters correctly

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST identify tasks by their unique deterministic task ID (UUID5 format)
- **FR-002**: System MUST accept task ID as a required positional argument via CLI
- **FR-003**: System MUST remove the specified task from in-memory storage when deletion succeeds
- **FR-004**: System MUST display success message showing deleted task's ID, title, and description (if present)
- **FR-005**: System MUST display error message "Task not found with ID: [id]" when task ID doesn't exist
- **FR-006**: System MUST exit with code 0 on successful deletion
- **FR-007**: System MUST exit with code 1 when task ID is not found
- **FR-008**: System MUST exit with code 2 when task ID argument is missing (argparse validation)
- **FR-009**: System MUST support deletion of tasks with any status (complete or incomplete)
- **FR-010**: System MUST correctly display Unicode characters in deleted task confirmation message
- **FR-011**: System MUST provide `--help` flag to display usage information
- **FR-012**: Deletion MUST be permanent for the current session (no recovery mechanism)

### Key Entities

- **Task**: The task object being deleted, identified by unique ID with attributes (id, title, description, status, created timestamp)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can delete a task in a single command using the task ID
- **SC-002**: Deleted task immediately disappears from task list views (verifiable by running view command)
- **SC-003**: System provides clear confirmation message showing what was deleted (ID, title, description)
- **SC-004**: System provides clear error messages for all failure scenarios (non-existent ID, missing ID)
- **SC-005**: Deletion operation completes in under 1 second for typical use cases
- **SC-006**: Unicode characters in task data are correctly displayed in deletion confirmation message
- **SC-007**: Command help documentation clearly explains usage and provides examples

## Assumptions

- **A-001**: Task IDs are visible to users (from View Task List feature output)
- **A-002**: Users will copy-paste task IDs from view command output to delete command
- **A-003**: In-memory storage (Phase I constraint) means deletions are lost when process ends
- **A-004**: Delete command follows standard CLI conventions (positional args, error handling, help text)
- **A-005**: No confirmation prompt required before deletion (user must be intentional with command)
- **A-006**: No undo/recovery functionality required (not specified, Phase I scope)
- **A-007**: No audit trail of deleted tasks required (Phase I constraint: in-memory only)
- **A-008**: Only one task can be deleted per command invocation (bulk delete not required)
- **A-009**: Deletion does not require special permissions (single-user CLI application)

## Dependencies

- **Add Task feature** (001-add-task): Must exist to create tasks that can be deleted
- **View Task List feature** (002-view-task-list): Recommended for users to discover task IDs before deletion

## Out of Scope (Phase I)

- Bulk deletion (deleting multiple tasks at once)
- Deletion confirmation prompt ("Are you sure?" dialogue)
- Undo/recovery functionality
- Soft delete with trash/archive
- Deletion history or audit trail
- Delete by criteria (e.g., "delete all completed tasks")
- Natural language task identification (e.g., "delete task about milk")
- Deletion permissions or access control
- Cascading deletions (no related entities in Phase I)

## CLI Interface Examples

**Command Format**:
```bash
python -m src.main delete <TASK_ID>
```

**Example 1 - Delete Existing Task**:
```bash
$ python -m src.main delete abc-123-def-456
Task deleted successfully!
ID: abc-123-def-456
Title: Buy milk
Description: Get organic whole milk
Status: Incomplete
```

**Example 2 - Delete Task with No Description**:
```bash
$ python -m src.main delete xyz-789
Task deleted successfully!
ID: xyz-789
Title: Call John
Description: (none)
Status: Complete
```

**Example 3 - Task Not Found**:
```bash
$ python -m src.main delete nonexistent-id
Error: Task not found with ID: nonexistent-id
```

**Example 4 - Missing Task ID**:
```bash
$ python -m src.main delete
Error: Task ID is required
Usage: python -m src.main delete <TASK_ID>
```

**Example 5 - Help Text**:
```bash
$ python -m src.main delete --help
usage: todo delete [-h] task_id

Delete an existing task by its unique ID

positional arguments:
  task_id     Unique task identifier (UUID)

options:
  -h, --help  show this help message and exit
```

## Related Features

- **Add Task** (001-add-task): Creates tasks that can later be deleted
- **View Task List** (002-view-task-list): Displays task IDs needed for deletion
- **Update Task** (003-update-task): Alternative to deletion for modifying tasks
