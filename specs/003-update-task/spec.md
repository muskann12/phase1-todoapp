# Feature Specification: Update Task

**Feature Branch**: `003-update-task`
**Created**: 2025-12-31
**Status**: Draft
**Input**: User description: "Update Task feature for an in-memory Python CLI Todo application. Allow the user to update an existing todo task's title and/or description using its unique task ID via a command-line interface."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Update Task Title (Priority: P1) 🎯 MVP

A user needs to correct a typo or refine the wording of a task's title without changing the description.

**Why this priority**: Core update functionality - allows users to fix errors and improve task clarity. This is the most common update scenario and provides immediate value.

**Independent Test**: Create a task with title "Buy mlk", update title to "Buy milk" using task ID, verify title changed and description unchanged.

**Acceptance Scenarios**:

1. **Given** a task exists with ID "abc-123" and title "Review docuemnt"
   **When** user runs `update abc-123 --title "Review document"`
   **Then** task ID "abc-123" has title "Review document" and description remains unchanged

2. **Given** a task exists with ID "xyz-789" and title "Call John" and description "Discuss project timeline"
   **When** user runs `update xyz-789 --title "Call Sarah"`
   **Then** task has title "Call Sarah" and description "Discuss project timeline" remains unchanged

3. **Given** a task exists with ID "def-456" and empty description
   **When** user runs `update def-456 --title "New title"`
   **Then** task has title "New title" and description remains empty

---

### User Story 2 - Update Task Description (Priority: P2)

A user needs to add context or update the details of a task without changing its title.

**Why this priority**: Common enhancement scenario - users often start with just a title and add details later. Supports evolving task requirements.

**Independent Test**: Create a task with empty description, update description to "Details here" using task ID, verify description changed and title unchanged.

**Acceptance Scenarios**:

1. **Given** a task exists with ID "abc-123" and title "Buy milk" and empty description
   **When** user runs `update abc-123 --description "Get organic whole milk from Trader Joe's"`
   **Then** task has description "Get organic whole milk from Trader Joe's" and title "Buy milk" remains unchanged

2. **Given** a task exists with ID "xyz-789" and title "Review code" and description "Check PR #42"
   **When** user runs `update xyz-789 --description "Review PR #45 for security fixes"`
   **Then** task has description "Review PR #45 for security fixes" and title "Review code" remains unchanged

3. **Given** a task exists with ID "def-456" and description "Old context"
   **When** user runs `update def-456 --description ""`
   **Then** task has empty description (description can be cleared)

---

### User Story 3 - Update Both Title and Description (Priority: P3)

A user needs to completely revise a task by updating both title and description simultaneously.

**Why this priority**: Convenience feature - allows atomic updates for task rewrites. Less common than individual field updates but reduces command count for complete changes.

**Independent Test**: Create a task, update both title and description in one command using task ID, verify both fields changed.

**Acceptance Scenarios**:

1. **Given** a task exists with ID "abc-123", title "Old title", and description "Old description"
   **When** user runs `update abc-123 --title "New title" --description "New description"`
   **Then** task has title "New title" and description "New description"

2. **Given** a task exists with ID "xyz-789", title "Task A", and empty description
   **When** user runs `update xyz-789 --title "Task B" --description "Details for Task B"`
   **Then** task has title "Task B" and description "Details for Task B"

---

### Edge Cases

- **Non-existent Task ID**: What happens when user provides an ID that doesn't exist? → System displays error message "Task not found with ID: [id]" and exits with non-zero code
- **Empty Title Update**: What happens when user tries to update title to empty string? → System rejects update with error "Title cannot be empty" (title is required)
- **Invalid ID Format**: What happens when user provides malformed ID? → System displays error "Task not found with ID: [id]" (ID validation is lenient - if not found, show error)
- **No Update Flags Provided**: What happens when user runs `update abc-123` with no `--title` or `--description`? → System displays error "No updates provided. Use --title and/or --description" and shows usage help
- **Unicode in Title/Description**: What happens when updating with Unicode characters (emoji, accented characters)? → System accepts and stores Unicode correctly (Python 3.13+ native Unicode support)
- **Very Long Title**: What happens when title exceeds maximum length (500 chars)? → System rejects update with error "Title cannot exceed 500 characters"
- **Very Long Description**: What happens when description exceeds maximum length (2000 chars)? → System rejects update with error "Description cannot exceed 2000 characters"
- **Task Status Preservation**: When updating task fields, is the status preserved? → Yes, status (complete/incomplete) remains unchanged

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST identify tasks by their unique deterministic task ID (UUID5 format)
- **FR-002**: System MUST support updating task title via `--title` flag
- **FR-003**: System MUST support updating task description via `--description` flag
- **FR-004**: System MUST support updating both title and description simultaneously
- **FR-005**: System MUST preserve task status (complete/incomplete) when updating title or description
- **FR-006**: System MUST preserve task ID and creation timestamp when updating fields
- **FR-007**: System MUST reject updates with empty title (title is required, minimum 1 character)
- **FR-008**: System MUST accept empty description (description is optional, can be empty string)
- **FR-009**: System MUST validate title length does not exceed 500 characters
- **FR-010**: System MUST validate description length does not exceed 2000 characters
- **FR-011**: System MUST display error message "Task not found with ID: [id]" when task ID doesn't exist
- **FR-012**: System MUST display error message "No updates provided" when neither `--title` nor `--description` are provided
- **FR-013**: System MUST support Unicode characters (UTF-8) in title and description fields
- **FR-014**: System MUST display success confirmation showing updated task details after successful update
- **FR-015**: System MUST provide `--help` flag showing usage and examples
- **FR-016**: System MUST exit with code 0 on success, non-zero on error

### Key Entities *(include if feature involves data)*

- **Task**: Represents a todo item with:
  - `id` (string, UUID5, unique, immutable): Deterministic identifier
  - `title` (string, 1-500 chars, required): Task summary
  - `description` (string, 0-2000 chars, optional): Task details
  - `status` (enum: INCOMPLETE/COMPLETE): Task completion state
  - `created_at` (datetime, immutable): Creation timestamp

**Field Mutability Matrix**:
- ✏️ Mutable: `title`, `description` (via Update Task feature)
- 🔒 Immutable: `id`, `created_at`
- ⚙️ Status-Dependent: `status` (via Mark Complete/Incomplete feature, not Update Task)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can update a task's title in a single command using the task ID
- **SC-002**: Users can update a task's description in a single command using the task ID
- **SC-003**: Users can update both title and description simultaneously in one command
- **SC-004**: System provides clear error messages for all failure scenarios (non-existent ID, validation errors, missing flags)
- **SC-005**: Task status and creation timestamp remain unchanged after title/description updates
- **SC-006**: Updated task information is immediately reflected in task list views
- **SC-007**: Users can clear task description by updating to empty string
- **SC-008**: Unicode characters in title and description are correctly stored and displayed
- **SC-009**: Command help documentation clearly explains usage and provides examples

## Assumptions

- **A-001**: Task IDs are visible to users (from View Task List feature output)
- **A-002**: Users will copy-paste task IDs from view command output to update command
- **A-003**: In-memory storage (Phase I constraint) means updates are lost when process ends
- **A-004**: Update command follows standard CLI conventions (flags with `--`, error handling, help text)
- **A-005**: No undo/redo functionality required (not specified, Phase I scope)
- **A-006**: No update history/audit trail required (Phase I constraint: in-memory only)
- **A-007**: Only one task can be updated per command invocation (bulk update not required)
- **A-008**: Task validation rules (title length, description length) match Add Task feature for consistency

## Dependencies

- **Add Task feature** (001-add-task): Must exist to create tasks that can be updated
- **View Task List feature** (002-view-task-list): Recommended for users to discover task IDs before updating

## Out of Scope (Phase I)

- Bulk updates (updating multiple tasks at once)
- Update history or change tracking
- Undo/redo functionality
- Task field versioning
- Update permissions or access control
- Updating task status (handled by Mark Complete/Incomplete feature)
- Updating task creation timestamp
- Updating task ID (immutable by design)
- Natural language task identification (e.g., "update task about milk")

## CLI Interface Examples

**Command Format**:
```bash
python -m src.main update <TASK_ID> [--title "New Title"] [--description "New Description"]
```

**Example 1 - Update Title Only**:
```bash
$ python -m src.main update abc-123-def-456 --title "Buy organic milk"
Task updated successfully!
ID: abc-123-def-456
Title: Buy organic milk
Description: (unchanged)
Status: Incomplete
```

**Example 2 - Update Description Only**:
```bash
$ python -m src.main update xyz-789 --description "Get whole milk from Trader Joe's"
Task updated successfully!
ID: xyz-789
Title: (unchanged)
Description: Get whole milk from Trader Joe's
Status: Incomplete
```

**Example 3 - Update Both**:
```bash
$ python -m src.main update def-456 --title "Call Sarah" --description "Discuss Q1 roadmap"
Task updated successfully!
ID: def-456
Title: Call Sarah
Description: Discuss Q1 roadmap
Status: Incomplete
```

**Example 4 - Error: Task Not Found**:
```bash
$ python -m src.main update nonexistent-id --title "New Title"
Error: Task not found with ID: nonexistent-id
```

**Example 5 - Error: No Updates Provided**:
```bash
$ python -m src.main update abc-123
Error: No updates provided. Use --title and/or --description
Usage: python -m src.main update <TASK_ID> [--title "TITLE"] [--description "DESC"]
```

**Example 6 - Help**:
```bash
$ python -m src.main update --help
usage: todo update [-h] [--title TITLE] [--description DESCRIPTION] task_id

Update an existing task's title and/or description

positional arguments:
  task_id              Unique task identifier (UUID)

options:
  -h, --help           show this help message and exit
  --title TITLE        New task title (1-500 characters)
  --description DESCRIPTION
                       New task description (0-2000 characters, optional)

Examples:
  python -m src.main update abc-123 --title "New Title"
  python -m src.main update abc-123 --description "New Description"
  python -m src.main update abc-123 --title "New Title" --description "New Desc"
```

## Notes

- This specification focuses on WHAT the feature does, not HOW it's implemented
- Technical implementation details (service layer, CLI parsing, storage) will be defined in plan.md
- All CLI examples show expected behavior, not implementation code
