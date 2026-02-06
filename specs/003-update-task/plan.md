# Implementation Plan: Update Task

**Branch**: `003-update-task` | **Date**: 2025-12-31 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/003-update-task/spec.md`

## Summary

The Update Task feature allows users to modify an existing task's title and/or description using the task's unique ID via command-line interface. This feature supports partial updates (title-only, description-only, or both simultaneously) while preserving immutable fields (id, created_at, status). Implementation follows the existing architecture pattern established by Add Task (001) and View Task List (002) features, using in-memory storage, argparse CLI framework, and Test-First Development methodology.

**Technical Approach**: Add `update_task()` function to service layer for business logic, create `update_task.py` CLI module for user interaction, update main router for command routing. Reuse existing Task model validation (no schema changes required). Implement partial update pattern using Python optional parameters (None defaults).

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: argparse (stdlib), dataclasses (stdlib), uuid (stdlib), datetime (stdlib), pytest (testing)
**Storage**: In-memory dictionary (`_tasks: Dict[str, Task]` in `src/services/task_service.py`)
**Testing**: pytest with coverage (pytest-cov)
**Target Platform**: CLI application (Python interpreter on any OS)
**Project Type**: Single project (src/ and tests/ at repository root)
**Performance Goals**: Instant response for update operations (< 10ms for in-memory dict lookup and update)
**Constraints**: In-memory only (no persistence), CLI-only interface, Python 3.13+ required (Phase I Constitution)
**Scale/Scope**: Small-scale (5 features total in Phase I, in-memory storage limits scale to process lifetime)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ I. Specifications as Single Source of Truth
- **Status**: PASS
- **Evidence**: spec.md approved, all requirements explicit, no ambiguity
- **Action**: None required

### ✅ II. AI-Generated Code Only
- **Status**: PASS
- **Evidence**: Implementation via `/sp.implement` command (Claude Code only)
- **Action**: None required

### ✅ III. Reusable Intelligence Encouraged
- **Status**: PASS
- **Evidence**: Reuses existing Task model, service layer pattern, CLI pattern from Add Task and View Task List features
- **Action**: None required

### ✅ IV. Mandatory Five-Step Workflow
- **Status**: PASS
- **Evidence**: Following spec → plan → tasks → implement → validate workflow
- **Current Step**: 2/5 (Planning phase)
- **Action**: Proceed to task decomposition after plan approval

### ✅ V. Test-First Development (NON-NEGOTIABLE)
- **Status**: PASS
- **Evidence**: Plan includes RED-GREEN-REFACTOR cycle in quickstart.md
- **Action**: Ensure tests written before implementation code in tasks.md

### ✅ VI. Modularity and Clean Code
- **Status**: PASS
- **Evidence**: Separation of concerns - service layer (business logic), CLI layer (presentation), Task model (data)
- **Action**: None required

### ✅ VII. Explicit Over Implicit
- **Status**: PASS
- **Evidence**: All edge cases defined in spec.md, validation rules explicit in data-model.md, error messages specified in contracts/cli-interface.md
- **Action**: None required

### ✅ VIII. Small, Testable Changes
- **Status**: PASS
- **Evidence**: Minimal diff - adds 1 service function, 1 CLI file, updates main.py routing. All independently testable.
- **Action**: None required

**Constitution Check Result**: ✅ **ALL GATES PASS** - Proceed to implementation

## Project Structure

### Documentation (this feature)

```text
specs/003-update-task/
├── spec.md                # Feature specification (/sp.specify output)
├── plan.md                # This file (/sp.plan output)
├── research.md            # Technical decisions and rationale (/sp.plan Phase 0)
├── data-model.md          # Task entity description (/sp.plan Phase 1)
├── quickstart.md          # Implementation guide (/sp.plan Phase 1)
├── contracts/
│   └── cli-interface.md   # CLI contract specification (/sp.plan Phase 1)
├── checklists/
│   └── requirements.md    # Spec quality validation (/sp.specify output)
└── tasks.md               # Task decomposition (/sp.tasks output - NOT YET CREATED)
```

### Source Code (repository root)

```text
src/
├── models/
│   ├── __init__.py        # Existing (no changes)
│   └── task.py            # Existing Task dataclass (no changes)
├── services/
│   ├── __init__.py        # Existing (no changes)
│   └── task_service.py    # UPDATE: add update_task() function
├── cli/
│   ├── __init__.py        # Existing (no changes)
│   ├── add_task.py        # Existing (no changes)
│   ├── view_tasks.py      # Existing (no changes)
│   └── update_task.py     # NEW: CLI command for update
├── main.py                # UPDATE: add "update" command routing
└── __init__.py            # Existing (no changes)

tests/
├── unit/
│   └── test_task_service.py    # UPDATE: add ~10 tests for update_task()
└── integration/
    └── test_update_task_integration.py  # NEW: ~6 integration tests for CLI
```

**Structure Decision**: Single project layout (Option 1 from template) - consistent with existing Phase I architecture. All source code in `src/`, all tests in `tests/`. No web frontend, no mobile app, no separate backend (Phase I constraint: CLI-only).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**No violations detected.** All Constitution principles followed. No complexity justification required.

---

## Implementation Strategy

### Phase 0: Research ✅ COMPLETE

**Artifact**: `research.md`

**Key Decisions**:
1. **Update Task Service Function**: Add `update_task(task_id, title=None, description=None)` to `src/services/task_service.py`
   - **Rationale**: Follows existing service layer pattern, enables partial updates via Python optional parameters
   - **Alternatives**: Separate functions (update_title, update_description) - rejected due to duplication

2. **CLI Argument Parsing**: Use argparse with `--title` and `--description` optional flags + required `task_id` positional argument
   - **Rationale**: Consistent with Add Task and View Task List, standard CLI pattern for optional updates
   - **Alternatives**: Interactive prompts - rejected (violates Phase I CLI-only constraint)

3. **Error Handling**: Mirror Add Task pattern - service layer raises exceptions, CLI layer translates to user messages and exit codes
   - **Rationale**: Maintains clean architecture separation (domain logic vs presentation)
   - **Error scenarios**: 5 edge cases defined (task not found, empty title, title too long, description too long, no updates)

4. **Success Confirmation**: Display updated task details in same format as Add Task success message
   - **Rationale**: User expectation, consistency, helps verify update applied correctly

**Technology Stack**: No new dependencies - all functionality in stdlib + existing codebase (argparse, dataclasses, uuid, datetime, pytest)

---

### Phase 1: Design & Contracts ✅ COMPLETE

**Artifacts**: `data-model.md`, `contracts/cli-interface.md`, `quickstart.md`

#### Data Model

**Entity**: Task (existing, no changes)

**Mutable Fields** (updated by this feature):
- ✏️ `title` (string, 1-500 chars, required)
- ✏️ `description` (string, 0-2000 chars, optional)

**Immutable Fields** (preserved by this feature):
- 🔒 `id` (string, UUID5, unique)
- 🔒 `created` (datetime, creation timestamp)
- ⚙️ `status` (enum, INCOMPLETE/COMPLETE - updated by Mark Complete feature, not Update Task)

**Validation**: Reuses Task dataclass `__post_init__` validation (no new validation logic required)

#### CLI Interface Contract

**Command Signature**:
```bash
python -m src.main update <TASK_ID> [--title TITLE] [--description DESCRIPTION]
```

**Positional Arguments**:
- `task_id` (required): Unique task identifier (UUID5 format)

**Optional Flags**:
- `--title` (optional): New task title (1-500 chars after trim, non-empty)
- `--description` (optional): New task description (0-2000 chars, can be empty string)
- `--help` / `-h` (optional): Display usage help

**Constraints**:
- At least one update required (--title OR --description OR both)
- Empty description allowed ("" clears description)
- Empty title rejected (title is required field)

**Exit Codes**:
- `0`: Success (task updated or help displayed)
- `1`: Application error (task not found, validation failed, no updates)
- `2`: Usage error (argparse validation failed)

**Error Messages** (8 scenarios):
1. Task not found → "Error: Task not found with ID: {id}"
2. No updates → "Error: No updates provided. Use --title and/or --description"
3. Empty title → "Error: Title cannot be empty"
4. Title too long → "Error: Title cannot exceed 500 characters"
5. Description too long → "Error: Description cannot exceed 2000 characters"
6. Missing task_id → argparse error (exit code 2)
7. Invalid flag → argparse error (exit code 2)
8. Unicode support → native Python 3.13+ UTF-8 handling

**Success Output Format**:
```
Task updated successfully!
ID: <task_id>
Title: <title>
Description: <description or "(none)">
Status: <status>
```

#### Implementation Guide

**Quickstart.md** provides step-by-step roadmap:
1. Add `update_task()` to service layer
2. Write unit tests (RED phase - 10 tests)
3. Implement service function (GREEN phase)
4. Create `src/cli/update_task.py` CLI command file
5. Update `src/main.py` router with "update" command
6. Write integration tests (6 tests)
7. Manual validation (CLI testing)
8. Run full test suite with coverage

---

## Architecture Details

### Service Layer (`src/services/task_service.py`)

**New Function**: `update_task(task_id: str, title: str | None = None, description: str | None = None) -> Task`

**Responsibilities**:
- Validate task exists (KeyError if not found)
- Validate at least one update provided (ValueError if both None)
- Retrieve existing task from _tasks dict
- Determine new values (use provided or preserve existing)
- Create updated Task instance (triggers validation)
- Replace task in _tasks dict
- Return updated Task object

**Validation Strategy**:
- Reuse Task dataclass `__post_init__` validation
- Create new Task instance with updated fields → validation runs automatically
- No duplication of validation logic

**Immutability Enforcement**:
- Pass existing `id`, `created`, `status` to new Task instance
- These fields never modified by Update Task feature

**Error Handling**:
- Raise KeyError for non-existent task_id
- Raise ValueError for no updates provided
- Let Task.__post_init__ raise ValueError for validation failures (empty title, length exceeded)

---

### CLI Layer (`src/cli/update_task.py`)

**New File**: `src/cli/update_task.py`

**Function**: `update_task_command(args: list[str] = None)`

**Responsibilities**:
- Parse command-line arguments with argparse
- Validate at least one update flag provided (before calling service)
- Call `update_task()` service function
- Handle exceptions → translate to user-friendly error messages
- Print success confirmation with updated task details
- Exit with appropriate code (0=success, 1=error)

**Argparse Configuration**:
```python
parser = argparse.ArgumentParser(description='...', prog='todo update')
parser.add_argument('task_id', type=str, help='...')
parser.add_argument('--title', type=str, default=None, help='...')
parser.add_argument('--description', type=str, default=None, help='...')
```

**Error Handling Pattern**:
```python
try:
    updated_task = update_task(args.task_id, args.title, args.description)
    # Print success
    sys.exit(0)
except KeyError:
    print(f"Error: Task not found with ID: {args.task_id}", file=sys.stderr)
    sys.exit(1)
except ValueError as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
```

---

### Main Router Update (`src/main.py`)

**Changes**:
1. Add "update" to command list in usage message
2. Add elif block for "update" command routing
3. Import and call `update_task_command` from `src.cli.update_task`

**Pattern** (consistent with add, view commands):
```python
elif command == 'update':
    from src.cli.update_task import update_task_command
    update_task_command(sys.argv[2:])
```

---

## Testing Strategy

### Unit Tests (`tests/unit/test_task_service.py`)

**Test Coverage** (10 tests for `update_task()` function):

1. ✅ Update title only (preserve description)
2. ✅ Update description only (preserve title)
3. ✅ Update both title and description
4. ✅ Clear description with empty string
5. ✅ Non-existent task ID raises KeyError
6. ✅ No updates provided raises ValueError
7. ✅ Empty title raises ValueError
8. ✅ Title > 500 chars raises ValueError
9. ✅ Description > 2000 chars raises ValueError
10. ✅ Status preserved after update (immutability)

**RED-GREEN-REFACTOR Workflow**:
- **RED**: Write tests first, run pytest → verify FAIL (update_task doesn't exist)
- **GREEN**: Implement update_task(), run pytest → verify PASS (all tests pass)
- **REFACTOR**: Review code for improvements (DRY, clarity, performance)

---

### Integration Tests (`tests/integration/test_update_task_integration.py`)

**Test Coverage** (6 tests for CLI command):

1. ✅ Help text display (--help)
2. ✅ Update title in-process (service layer test)
3. ✅ Update description in-process
4. ✅ Update both fields in-process
5. ✅ Unicode character handling (UTF-8 support)
6. ✅ Immutable fields preserved (ID, created, status)

**In-Process Testing Pattern**:
- Phase I constraint: in-memory storage doesn't persist between subprocess calls
- Solution: Test service layer directly (import and call functions), not via subprocess
- Subprocess tests only for CLI-specific behavior (help text, argparse)

---

### Coverage Goals

- **Service Layer**: 100% coverage for `update_task()` function
- **CLI Layer**: Tested via integration tests (subprocess/in-process)
- **Overall**: > 90% coverage for src/services/task_service.py

---

## File Changes Summary

### New Files (2)

1. **`src/cli/update_task.py`** (~60 lines)
   - CLI command implementation
   - argparse setup, error handling, output formatting

2. **`tests/integration/test_update_task_integration.py`** (~80 lines)
   - Integration tests for CLI behavior
   - In-process testing pattern for Phase I constraints

### Modified Files (2)

1. **`src/services/task_service.py`** (add ~35 lines)
   - Add `update_task()` function after `get_all_tasks()`
   - Follows existing function structure and patterns

2. **`src/main.py`** (modify ~10 lines)
   - Add "update" to command list in usage messages (2 locations)
   - Add elif block for "update" command routing (4 lines)
   - Update "Available commands" error message (1 line)

3. **`tests/unit/test_task_service.py`** (add ~120 lines)
   - Add 10 unit tests for `update_task()` function
   - Follows existing test structure and patterns

**Total LOC**: ~295 lines of new/modified code (not counting comments/docstrings)

---

## Dependencies

### Internal Dependencies (existing features)

1. **Add Task (001-add-task)** - REQUIRED
   - Provides: Task model (src/models/task.py)
   - Provides: create_task() function for test setup
   - Provides: _tasks storage dict
   - Provides: generate_task_id() function
   - Provides: Task validation logic in `__post_init__`

2. **View Task List (002-view-task-list)** - RECOMMENDED
   - Provides: Visual confirmation of updates (SC-006 requirement)
   - Provides: get_all_tasks() for integration testing
   - Not strictly required for Update Task functionality, but enhances user experience

### External Dependencies (no new additions)

All dependencies already in stdlib or existing project:
- ✅ `argparse` (stdlib) - CLI argument parsing
- ✅ `sys` (stdlib) - exit codes, stderr output
- ✅ `uuid` (stdlib) - UUID5 generation (existing)
- ✅ `datetime` (stdlib) - timestamps (existing)
- ✅ `dataclasses` (stdlib) - Task model (existing)
- ✅ `pytest` (dev dependency) - testing framework (existing)
- ✅ `pytest-cov` (dev dependency) - coverage reporting (existing)

**No new pip installs required.**

---

## Risk Analysis

### Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| In-memory storage isolation in tests | ✅ Known | Medium | Use in-process testing pattern (established in View Task List feature) |
| Unicode character handling | Low | Low | Python 3.13+ native UTF-8 support (no action needed) |
| Validation logic duplication | Low | Low | Reuse Task.__post_init__ validation (design pattern enforced) |
| Argparse help text clarity | Low | Low | Provide examples in help text (spec requirement FR-015) |

**All risks mitigated** through existing patterns or stdlib features.

### Implementation Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Forgetting to preserve immutable fields | Medium | High | Explicit tests for id/created/status preservation (test coverage requirement) |
| Missing "no updates provided" validation | Low | Medium | Validation check in CLI layer before service call |
| Incorrect exit codes | Low | Low | Follow Add Task exit code pattern (0=success, 1=error, 2=usage) |

**All risks addressable** through Test-First Development and code review.

---

## Success Criteria Validation

After implementation, verify all 9 success criteria from spec.md:

- ✅ **SC-001**: Users can update task title in single command using task ID
  - **Test**: `python -m src.main update <ID> --title "New Title"`

- ✅ **SC-002**: Users can update task description in single command using task ID
  - **Test**: `python -m src.main update <ID> --description "New Description"`

- ✅ **SC-003**: Users can update both title and description simultaneously
  - **Test**: `python -m src.main update <ID> --title "A" --description "B"`

- ✅ **SC-004**: System provides clear error messages for all failure scenarios
  - **Test**: Verify 8 error messages (task not found, empty title, etc.)

- ✅ **SC-005**: Task status and created timestamp remain unchanged after updates
  - **Test**: Unit test `test_update_task_preserves_status()`

- ✅ **SC-006**: Updated task information immediately reflected in View Task List
  - **Test**: Update task, run view command, verify changes visible

- ✅ **SC-007**: Users can clear task description by updating to empty string
  - **Test**: `python -m src.main update <ID> --description ""`

- ✅ **SC-008**: Unicode characters correctly stored and displayed
  - **Test**: Integration test `test_update_task_unicode_in_process()`

- ✅ **SC-009**: Command help documentation clearly explains usage
  - **Test**: `python -m src.main update --help` shows usage and examples

---

## Next Steps

After plan approval:

1. **Run `/sp.tasks`** to generate detailed task decomposition
   - Input: This plan.md + spec.md
   - Output: tasks.md with RED-GREEN-REFACTOR workflow

2. **Run `/sp.implement`** to execute implementation via Claude Code
   - Input: tasks.md
   - Output: Fully implemented Update Task feature with tests

3. **Manual validation** against success criteria
   - Test all 9 success criteria from spec.md
   - Verify error messages, Unicode support, help text

4. **Code review** (human approval)
   - Verify Constitution compliance
   - Check code quality, test coverage, documentation

5. **Commit and PR**
   - Create commit with descriptive message
   - Create pull request for feature review

---

## References

- **Specification**: [specs/003-update-task/spec.md](spec.md)
- **Research**: [specs/003-update-task/research.md](research.md)
- **Data Model**: [specs/003-update-task/data-model.md](data-model.md)
- **CLI Contract**: [specs/003-update-task/contracts/cli-interface.md](contracts/cli-interface.md)
- **Quickstart**: [specs/003-update-task/quickstart.md](quickstart.md)
- **Constitution**: [.specify/memory/constitution.md](../../.specify/memory/constitution.md)
- **Add Task Feature**: [specs/001-add-task/](../001-add-task/)
- **View Task List Feature**: [specs/002-view-task-list/](../002-view-task-list/)
