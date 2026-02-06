# Feature Specification: View Task List

**Feature Branch**: `002-view-task-list`
**Created**: 2025-12-31
**Status**: Draft
**Input**: User description: "View Task List"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - View All Tasks (Priority: P1) 🎯 MVP

Users need to see what tasks they have created to review their todo list and plan their work. This is the core read functionality that complements the Add Task feature.

**Why this priority**: This is the minimum viable read functionality. Without the ability to view tasks, the Add Task feature has limited value. Users must be able to see what they've added.

**Independent Test**: Run the view command after creating 3 tasks with different titles and statuses. Verify all 3 tasks are displayed with their ID, title, description, and status in ascending ID order.

**Acceptance Scenarios**:

1. **Given** no tasks exist in the system, **When** user runs the view command, **Then** system displays "No tasks found. Add your first task with: python -m src.main add \"<title>\""
2. **Given** 5 tasks exist (3 incomplete, 2 complete), **When** user runs the view command, **Then** system displays all 5 tasks in ascending ID order with status indicators ([ ] for incomplete, [✓] for complete)
3. **Given** tasks exist with both title and description, **When** user runs the view command, **Then** system displays each task's ID, title, description (or "(none)" if empty), and status
4. **Given** a task with a very long title (500 chars), **When** user runs the view command, **Then** system displays the full title without truncation
5. **Given** tasks with Unicode characters (e.g., "Café ☕"), **When** user runs the view command, **Then** system displays Unicode characters correctly

---

### User Story 2 - View Task Count Summary (Priority: P2)

Users want to quickly see how many tasks they have and how many are complete vs incomplete to understand their progress.

**Why this priority**: Provides valuable context about task list size and progress, but viewing the tasks themselves (P1) is more critical.

**Independent Test**: Create 10 tasks (7 incomplete, 3 complete), run the view command, and verify the summary line shows "Total: 10 | Incomplete: 7 | Complete: 3"

**Acceptance Scenarios**:

1. **Given** 10 tasks exist (7 incomplete, 3 complete), **When** user runs the view command, **Then** system displays a summary line at the top showing "Total: 10 | Incomplete: 7 | Complete: 3"
2. **Given** no tasks exist, **When** user runs the view command, **Then** no summary is displayed (only the empty-state message)

---

### Edge Cases

- What happens when there are 0 tasks in the system? (Display empty-state message)
- How does the system handle 1000+ tasks? (Display all without pagination in Phase I)
- What if a task has an empty description? (Display "(none)" instead of empty string)
- What if a task title contains special characters or line breaks? (Display exactly as stored, preserving special characters)
- What if the terminal width is narrow? (Allow text wrapping, no forced truncation)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a CLI command to view all tasks stored in memory
- **FR-002**: System MUST display tasks in ascending order by task ID (deterministic sort order)
- **FR-003**: System MUST display each task's ID, title, description, and status
- **FR-004**: System MUST use `[ ]` indicator for incomplete tasks and `[✓]` indicator for complete tasks
- **FR-005**: System MUST display "(none)" for tasks with empty descriptions
- **FR-006**: System MUST display a helpful empty-state message when no tasks exist
- **FR-007**: System MUST retrieve tasks from the in-memory storage without mutation
- **FR-008**: System MUST handle Unicode characters in task titles and descriptions correctly
- **FR-009**: System MUST display a count summary showing total, incomplete, and complete tasks (User Story 2)
- **FR-010**: System MUST exit with code 0 on successful display

### Key Entities *(include if feature involves data)*

- **Task**: Existing entity from Add Task feature (id, title, description, status, created). No new entities required.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can view their entire task list in under 2 seconds
- **SC-002**: System displays tasks in consistent, deterministic order (ascending by ID) 100% of the time
- **SC-003**: Empty task list displays helpful guidance message 100% of the time
- **SC-004**: System correctly displays tasks with Unicode characters (emojis, accented characters) without corruption
- **SC-005**: Task count summary accurately reflects the number of incomplete and complete tasks 100% of the time
- **SC-006**: View operation completes without modifying any task data (read-only guarantee)

## Assumptions *(optional)*

1. Tasks already exist in memory (created via Add Task feature)
2. In-memory storage structure (_tasks dict) is accessible to the view functionality
3. No filtering or search required in Phase I (view ALL tasks only)
4. No pagination required in Phase I (display all tasks regardless of count)
5. Task sorting is by ID in ascending order (matches insertion order for UUID5 sequential IDs)
6. Terminal supports UTF-8 for Unicode display
7. The view command does not modify task status, title, description, or any other field (read-only)

## Out of Scope *(optional)*

- Filtering tasks by status (incomplete/complete)
- Searching tasks by title or description keywords
- Sorting by fields other than ID (e.g., by created date, by title)
- Pagination or limiting number of tasks displayed
- Exporting task list to file
- Displaying tasks in table format with columns
- Color-coding output (e.g., green for complete, red for incomplete)

## Dependencies *(optional)*

- **Internal**: Requires `src/services/task_service.py` to provide task retrieval function (`get_all_tasks()`)
- **Internal**: Requires `src/models/task.py` for Task entity definition and TaskStatus enum
- **External**: None (uses Python standard library only)

## Constraints *(optional)*

- **Storage**: In-memory only (no persistence to file or database)
- **Interface**: CLI only (no GUI or web interface)
- **Runtime**: Python 3.13+ required
- **Performance**: Must handle at least 1000 tasks without noticeable delay (< 2 seconds)

## Notes *(optional)*

- The view command is read-only and must never modify task data
- Empty-state message should guide users to the Add Task command for first-time users
- Task IDs are UUID5 strings (e.g., "550e8400-e29b-41d4-a716-446655440000")
- Description field was introduced in Add Task feature and may be empty for title-only tasks
- Status indicators `[ ]` and `[✓]` provide quick visual scan for task completion
- The count summary (User Story 2) provides at-a-glance progress tracking
