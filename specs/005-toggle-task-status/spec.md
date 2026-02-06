# Feature Specification: Toggle Task Status

**Feature Branch**: `005-toggle-task-status`
**Created**: 2026-01-01
**Status**: Draft
**Input**: User description: "Mark Complete / Incomplete Task feature for an in-memory Python CLI Todo application. Allow the user to toggle the completion status of an existing todo task using its unique task ID via a command-line interface."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Mark Task as Complete (Priority: P1) 🎯 MVP

A user needs to mark an incomplete task as complete when they finish working on it, using the task's unique identifier.

**Why this priority**: Core productivity functionality - allows users to track progress by marking tasks complete. This is essential for task list management and provides immediate value by letting users see what they've accomplished.

**Independent Test**: Create an incomplete task, mark it as complete using its task ID, verify task status changes from incomplete to complete and persists in storage.

**Acceptance Scenarios**:

1. **Given** an incomplete task exists with ID "abc-123" and title "Buy milk"
   **When** user runs `complete abc-123`
   **Then** task status changes to complete and success message displays "Task marked as complete! ID: abc-123, Title: Buy milk, Status: Complete"

2. **Given** multiple incomplete tasks exist with IDs "abc-123", "xyz-789", "def-456"
   **When** user runs `complete xyz-789`
   **Then** only task "xyz-789" status changes to complete and tasks "abc-123" and "def-456" remain incomplete

3. **Given** an incomplete task exists with ID "abc-123", title "Complete report", and description "Q4 financial summary"
   **When** user runs `complete abc-123`
   **Then** task status changes to complete and success message displays task ID, title, description, and new status

---

### User Story 2 - Mark Task as Incomplete (Priority: P2)

A user needs to mark a complete task as incomplete when they realize it needs more work or was marked complete by mistake.

**Why this priority**: Error correction and workflow flexibility - allows users to reverse completion status when tasks need rework. This is important for maintaining accurate task lists but less critical than the initial completion capability.

**Independent Test**: Create a complete task, mark it as incomplete using its task ID, verify task status changes from complete to incomplete.

**Acceptance Scenarios**:

1. **Given** a complete task exists with ID "abc-123" and title "Review document"
   **When** user runs `incomplete abc-123`
   **Then** task status changes to incomplete and success message displays "Task marked as incomplete! ID: abc-123, Title: Review document, Status: Incomplete"

2. **Given** multiple complete tasks exist with IDs "abc-123", "xyz-789", "def-456"
   **When** user runs `incomplete abc-123`
   **Then** only task "abc-123" status changes to incomplete and tasks "xyz-789" and "def-456" remain complete

---

### User Story 3 - Toggle Task Status (Priority: P3)

A user needs to quickly toggle a task's status (complete ↔ incomplete) without needing to know its current state.

**Why this priority**: Convenience feature - provides a single command to flip status regardless of current state. This is nice-to-have for power users but not essential since P1 and P2 cover all use cases.

**Independent Test**: Create a task (any status), toggle its status, verify it switches to the opposite state.

**Acceptance Scenarios**:

1. **Given** an incomplete task exists with ID "abc-123"
   **When** user runs `toggle abc-123`
   **Then** task status changes to complete and success message displays new status

2. **Given** a complete task exists with ID "xyz-789"
   **When** user runs `toggle xyz-789`
   **Then** task status changes to incomplete and success message displays new status

---

### Edge Cases

- **Task Already in Target State**: What happens when user runs `complete` on an already complete task? → System displays success message showing task is complete (idempotent operation - no error, just confirmation of current state)

- **Task Already in Target State (Incomplete)**: What happens when user runs `incomplete` on an already incomplete task? → System displays success message showing task is incomplete (idempotent operation)

- **Non-existent Task ID**: What happens when user provides an ID that doesn't exist? → System displays error message "Error: Task not found with ID: [id]" and exits with non-zero code (exit code 1)

- **Invalid ID Format**: What happens when user provides malformed ID? → System displays error "Error: Task not found with ID: [id]" (ID validation is lenient - if not found, show error regardless of format)

- **Empty Task List**: What happens when user tries to mark complete/incomplete from an empty task list? → System displays error "Error: Task not found with ID: [id]" (same error as non-existent ID)

- **No Task ID Provided**: What happens when user runs `complete`/`incomplete`/`toggle` without providing a task ID? → System displays error and shows usage help with exit code 2 (argparse validation error)

- **Unicode in Task Data**: What happens when marking complete/incomplete a task with Unicode characters in title/description? → Task status is updated normally and success message displays Unicode characters correctly

- **Status Change Persistence**: Does the status change persist in memory? → Yes, status change persists in in-memory storage for the current session (follows Phase I constraints)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST identify tasks by their unique deterministic task ID (UUID5 format)
- **FR-002**: System MUST accept task ID as a required positional argument via CLI for all status change commands
- **FR-003**: System MUST provide three commands: `complete` (mark as complete), `incomplete` (mark as incomplete), `toggle` (switch status)
- **FR-004**: System MUST update task status to complete when `complete` command is executed
- **FR-005**: System MUST update task status to incomplete when `incomplete` command is executed
- **FR-006**: System MUST toggle task status (incomplete → complete, complete → incomplete) when `toggle` command is executed
- **FR-007**: System MUST persist status changes in in-memory storage for the current session
- **FR-008**: System MUST display success message showing task ID, title, description (if present), and new status after successful status change
- **FR-009**: System MUST display error message "Task not found with ID: [id]" when task ID doesn't exist
- **FR-010**: System MUST exit with code 0 on successful status change
- **FR-011**: System MUST exit with code 1 when task ID is not found
- **FR-012**: System MUST exit with code 2 when task ID argument is missing (argparse validation)
- **FR-013**: System MUST support idempotent operations (marking complete task as complete is valid, shows current status)
- **FR-014**: System MUST correctly display Unicode characters in status change confirmation message
- **FR-015**: System MUST provide `--help` flag for each command to display usage information
- **FR-016**: Status changes MUST be reflected immediately in subsequent view commands

### Key Entities

- **Task**: The task object whose status is being changed, identified by unique ID with attributes (id, title, description, status, created timestamp)
- **TaskStatus**: Enum representing task completion state with two values: INCOMPLETE and COMPLETE

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can change a task's status in a single command using the task ID
- **SC-002**: Status changes immediately appear in task list views (verifiable by running view command)
- **SC-003**: System provides clear confirmation message showing what changed (ID, title, description, new status)
- **SC-004**: System provides clear error messages for all failure scenarios (non-existent ID, missing ID)
- **SC-005**: Status change operation completes in under 1 second for typical use cases
- **SC-006**: Unicode characters in task data are correctly displayed in status change confirmation message
- **SC-007**: Command help documentation clearly explains usage and provides examples for all three commands
- **SC-008**: Users can toggle task status without needing to know current state (using toggle command)

## Assumptions

- **A-001**: Task IDs are visible to users (from View Task List feature output)
- **A-002**: Users will copy-paste task IDs from view command output to status change commands
- **A-003**: In-memory storage (Phase I constraint) means status changes are lost when process ends
- **A-004**: Status change commands follow standard CLI conventions (positional args, error handling, help text)
- **A-005**: Idempotent operations are acceptable (marking complete task as complete shows success, not error)
- **A-006**: No undo/redo functionality required (not specified, Phase I scope)
- **A-007**: No audit trail of status changes required (Phase I constraint: in-memory only)
- **A-008**: Only one task can be updated per command invocation (bulk status change not required)
- **A-009**: Status changes do not require special permissions (single-user CLI application)
- **A-010**: Task entity already exists with status field (TaskStatus enum) from previous features
- **A-011**: All three commands (complete, incomplete, toggle) have equal implementation priority within the feature

## Dependencies

- **Add Task feature** (001-add-task): Must exist to create tasks whose status can be changed
- **View Task List feature** (002-view-task-list): Recommended for users to discover task IDs and verify status changes
- **Task Model** (src/models/task.py): Must have TaskStatus enum with INCOMPLETE and COMPLETE values

## Out of Scope

- Bulk status changes (updating multiple tasks at once)
- Status history tracking (recording when tasks were marked complete/incomplete)
- Scheduled or automated status changes
- Status change notifications
- Custom status values beyond complete/incomplete
- Filtering tasks by status (belongs to View Task List enhancements)
- Undo/redo functionality for status changes
- Persistence beyond current session (Phase I constraint)
