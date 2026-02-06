# Research: Update Task Feature

**Feature**: 003-update-task
**Date**: 2025-12-31
**Status**: Complete

## Executive Summary

Update Task feature requires minimal new technical decisions - it reuses existing architecture from Add Task (001) and View Task List (002) features. All technical context is constrained by Phase I requirements (Python 3.13+, in-memory storage, CLI interface). No unknowns require resolution.

## Technical Decisions

### Decision 1: Update Task Service Function

**Chosen**: Add `update_task(task_id, title=None, description=None)` function to `src/services/task_service.py`

**Rationale**:
- Follows existing service layer pattern (create_task, get_task, get_all_tasks)
- Modular separation: business logic in services, presentation in CLI
- Reuses existing validation logic from Task model (title/description length constraints)
- Python optional parameters (None defaults) enable partial updates cleanly

**Alternatives Considered**:
- **Separate functions** (update_title, update_description): Rejected - increases API surface, duplicates validation logic
- **Immutable pattern** (create new task, delete old): Rejected - loses task ID and created_at timestamp (spec requires preservation)
- **Direct dict mutation** (modify _tasks[id] in CLI): Rejected - violates separation of concerns, duplicates validation

**Implementation Notes**:
- Check if task_id exists in _tasks dict → raise KeyError if not found
- Validate at least one field provided (title or description) → raise ValueError if both None
- Reuse Task dataclass validation by creating updated Task instance with modified fields
- Preserve immutable fields: id, created_at, status (per spec FR-005, FR-006)

---

### Decision 2: CLI Argument Parsing Strategy

**Chosen**: Use argparse with optional `--title` and `--description` flags + required positional `task_id` argument

**Rationale**:
- Consistent with existing CLI architecture (add_task.py, view_tasks.py use argparse)
- Standard CLI pattern for optional updates (e.g., `git commit --amend --message "new"`)
- argparse handles help text generation automatically (FR-015 requirement)
- Optional flags clearly communicate partial update support

**Alternatives Considered**:
- **Interactive prompts**: Rejected - violates Phase I CLI-only constraint, not scriptable
- **Positional arguments** (task_id, title, description): Rejected - can't distinguish between "update title only" vs "clear description"
- **JSON input**: Rejected - over-engineering for Phase I, reduces usability for simple updates

**Implementation Notes**:
- `parser.add_argument('task_id', type=str, help='Unique task identifier')`
- `parser.add_argument('--title', type=str, help='New task title (1-500 characters)')`
- `parser.add_argument('--description', type=str, help='New task description (0-2000 characters, optional)')`
- Validate at least one flag provided in CLI command function

---

### Decision 3: Error Handling Strategy

**Chosen**: Mirror Add Task error handling pattern - catch service layer exceptions, display user-friendly messages, exit with non-zero codes

**Rationale**:
- Consistency with existing features (add_task.py pattern established)
- Service layer raises domain exceptions (ValueError, KeyError)
- CLI layer translates to user messages and exit codes
- Follows Clean Architecture: services know domain rules, CLI knows presentation

**Alternatives Considered**:
- **Return error codes from service**: Rejected - exceptions are Pythonic, clearer than magic numbers
- **Try-catch in service layer**: Rejected - service shouldn't know about exit codes (CLI concern)

**Error Scenarios** (from spec edge cases):
1. Task not found → catch KeyError → "Error: Task not found with ID: {id}" + exit(1)
2. Empty title → catch ValueError → "Error: Title cannot be empty" + exit(1)
3. Title too long → catch ValueError → "Error: Title cannot exceed 500 characters" + exit(1)
4. Description too long → catch ValueError → "Error: Description cannot exceed 2000 characters" + exit(1)
5. No updates provided → check before service call → "Error: No updates provided..." + exit(1)

---

### Decision 4: Success Confirmation Output

**Chosen**: Display updated task details in same format as Add Task success message

**Rationale**:
- User expectation: confirmation shows what changed
- Consistency: Add Task shows "Task created successfully!" + details
- Spec FR-014: "display success confirmation showing updated task details"
- Helps users verify update was applied correctly

**Output Format**:
```
Task updated successfully!
ID: {task.id}
Title: {task.title}
Description: {task.description or "(none)"}
Status: {task.status.value.capitalize()}
```

**Note**: Shows ALL current values (not just changed fields) to provide complete context after update.

---

## Technology Stack (Phase I Constraints)

| Component | Technology | Constraint Source |
|-----------|------------|-------------------|
| Language | Python 3.13+ | Phase I Constitution |
| Storage | In-memory dict (no persistence) | Phase I Constitution |
| CLI Framework | argparse (stdlib) | Existing architecture (Add Task, View Task List) |
| Testing | pytest | Existing architecture (Add Task tests) |
| Validation | dataclass __post_init__ | Existing Task model pattern |
| ID Generation | UUID5 (deterministic) | Existing task_service pattern |

**No new dependencies required** - all functionality available in stdlib + existing codebase.

---

## Architecture Consistency Check

### Existing Patterns to Follow

1. **Service Layer** (`src/services/task_service.py`):
   - Functions operate on _tasks dict
   - Raise domain exceptions (ValueError, KeyError)
   - Return domain objects (Task instances)
   - No I/O or presentation logic

2. **CLI Layer** (`src/cli/*.py`):
   - Use argparse for command parsing
   - Import from services, call service functions
   - Handle exceptions → user-friendly messages
   - Print output, call sys.exit()

3. **Main Routing** (`src/main.py`):
   - Check command name
   - Import and call command function
   - Each command in separate file (add_task.py, view_tasks.py, update_task.py)

4. **Testing** (`tests/`):
   - Unit tests for service layer (tests/unit/test_task_service.py)
   - Integration tests for CLI (tests/integration/test_*_integration.py)
   - Test-First Development (RED-GREEN-REFACTOR)

### Update Task Conformance

✅ **Follows all existing patterns** - no architectural drift
✅ **Reuses existing Task model** - no new data structures
✅ **Consistent error handling** - same exception → message → exit pattern
✅ **Same CLI conventions** - argparse, flags, help text, exit codes

---

## Open Questions / Risks

**None identified.** All technical decisions are constrained by:
1. Phase I Constitution (in-memory, Python 3.13+, CLI-only)
2. Existing codebase architecture (service layer, CLI layer, Task model)
3. Specification requirements (16 functional requirements, all explicit)

No NEEDS CLARIFICATION items remain from Technical Context.

---

## References

- Specification: `specs/003-update-task/spec.md`
- Existing service layer: `src/services/task_service.py`
- Existing Task model: `src/models/task.py`
- Add Task CLI pattern: `src/cli/add_task.py`
- Constitution: `.specify/memory/constitution.md`
