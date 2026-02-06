# Implementation Plan: Delete Task

**Branch**: `004-delete-task` | **Date**: 2025-12-31 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/004-delete-task/spec.md`

## Summary

The Delete Task feature allows users to permanently remove an existing task from their todo list using the task's unique ID via command-line interface. This feature enables task list hygiene by removing completed or obsolete tasks. Implementation follows the existing architecture pattern established by Add Task (001), View Task List (002), and Update Task (003) features, using in-memory storage, argparse CLI framework, and Test-First Development methodology.

**Technical Approach**: Add `delete_task()` function to service layer for business logic, create `delete_task.py` CLI module for user interaction, update main router for command routing. Reuse existing Task model (no schema changes required). Implement deletion with confirmation message showing deleted task details before removal from storage.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: argparse (stdlib), dataclasses (stdlib), uuid (stdlib), datetime (stdlib), pytest (testing)
**Storage**: In-memory dictionary (`_tasks: Dict[str, Task]` in `src/services/task_service.py`)
**Testing**: pytest with coverage (pytest-cov)
**Target Platform**: CLI application (Python interpreter on any OS)
**Project Type**: Single project (src/ and tests/ at repository root)
**Performance Goals**: Instant response for delete operations (< 10ms for in-memory dict lookup and removal)
**Constraints**: In-memory only (no persistence), CLI-only interface, Python 3.13+ required, no undo/recovery (Phase I Constitution)
**Scale/Scope**: Small-scale (5 features total in Phase I, in-memory storage limits scale to process lifetime)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ I. Specifications as Single Source of Truth
- **Status**: PASS
- **Evidence**: spec.md approved, all requirements explicit, no ambiguity, all edge cases defined
- **Action**: None required

### ✅ II. AI-Generated Code Only
- **Status**: PASS
- **Evidence**: Implementation via `/sp.implement` command (Claude Code only)
- **Action**: None required

### ✅ III. Reusable Intelligence Encouraged
- **Status**: PASS
- **Evidence**: Reuses existing Task model, service layer pattern, CLI pattern, error handling pattern from Add Task, View Task List, and Update Task features
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
- **Evidence**: All edge cases defined in spec.md, validation rules explicit, error messages specified in contracts/cli-interface.md
- **Action**: None required

### ✅ VIII. Small, Testable Changes
- **Status**: PASS
- **Evidence**: Minimal diff - adds 1 service function, 1 CLI file, updates main.py routing. All independently testable.
- **Action**: None required

**Constitution Check Result**: ✅ **ALL GATES PASS** - Proceed to implementation

## Project Structure

### Documentation (this feature)

```text
specs/004-delete-task/
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
│   └── task_service.py    # UPDATE: add delete_task() function
├── cli/
│   ├── __init__.py        # Existing (no changes)
│   ├── add_task.py        # Existing (no changes)
│   ├── view_tasks.py      # Existing (no changes)
│   ├── update_task.py     # Existing (no changes)
│   └── delete_task.py     # NEW: CLI command for delete
├── main.py                # UPDATE: add "delete" command routing
└── __init__.py            # Existing (no changes)

tests/
├── unit/
│   ├── __init__.py        # Existing (no changes)
│   └── test_task_service.py    # UPDATE: add ~6 tests for delete_task()
└── integration/
    ├── __init__.py        # Existing (no changes)
    └── test_delete_task_integration.py  # NEW: ~4 integration tests for CLI
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
1. **Delete Task Service Function**: Add `delete_task(task_id)` to `src/services/task_service.py`
   - **Rationale**: Follows existing service layer pattern, returns deleted Task before removal for confirmation message
   - **Alternatives**: Void function with no return - rejected (user needs confirmation of what was deleted)

2. **CLI Argument Parsing**: Use argparse with required `task_id` positional argument
   - **Rationale**: Consistent with existing CLI pattern, simpler than Update Task (no optional flags)
   - **Alternatives**: Interactive confirmation prompt - rejected (violates Phase I CLI-only constraint and spec assumption A-005)

3. **Error Handling**: Mirror Add Task/Update Task pattern - service layer raises KeyError for non-existent ID, CLI layer translates to user messages and exit codes
   - **Rationale**: Maintains clean architecture separation (domain logic vs presentation)
   - **Error scenarios**: 3 main cases (task not found, missing ID argument, general errors)

4. **Success Confirmation**: Display deleted task details (ID, title, description, status) before removing from storage
   - **Rationale**: User verification, prevents accidental deletion confusion, follows SC-003 (show what was deleted)

5. **Permanent Deletion**: No soft delete, no undo mechanism (FR-012, assumption A-006)
   - **Rationale**: Phase I constraint (in-memory only), simpler implementation, spec explicitly states permanent deletion

**Technology Stack**: No new dependencies - all functionality in stdlib + existing codebase (argparse, dataclasses, uuid, datetime, pytest)

---

### Phase 1: Design & Contracts ✅ COMPLETE

**Artifacts**: `data-model.md`, `contracts/cli-interface.md`, `quickstart.md`

#### Data Model (data-model.md)

**Entity**: Task (existing - no changes required)
- Reuses existing Task dataclass from `src/models/task.py`
- No schema modifications needed for deletion
- Deletion removes entire Task object from storage

**Storage Operation**: Dictionary deletion using `del _tasks[task_id]`
- **Rationale**: Python dict.pop() or del operator for in-memory removal, O(1) complexity

#### Contracts (contracts/cli-interface.md)

**CLI Command**: `delete <task_id>`

**Input Contract**:
```python
# Positional argument (required)
task_id: str  # Unique task identifier (UUID5 format)
```

**Output Contract**:

*Success Response* (exit code 0):
```text
Task deleted successfully!
ID: <task_id>
Title: <title>
Description: <description or "(none)">
Status: <Complete|Incomplete>
```

*Error Responses*:

Exit code 1 (Task not found):
```text
Error: Task not found with ID: <task_id>
```

Exit code 2 (Missing argument - argparse):
```text
usage: todo delete [-h] task_id
todo delete: error: the following arguments are required: task_id
```

**Help Text**:
```text
usage: todo delete [-h] task_id

Delete an existing task by its unique ID

positional arguments:
  task_id     Unique task identifier (UUID)

options:
  -h, --help  show this help message and exit
```

#### Implementation Guide (quickstart.md)

**Test-First Workflow** (RED-GREEN-REFACTOR):

1. **RED Phase**: Write tests that fail
   - Unit tests for `delete_task()` function (6 tests)
   - Integration tests for CLI command (4 tests)
   - Run tests → Verify all FAIL

2. **GREEN Phase**: Implement minimal code to pass tests
   - Implement `delete_task()` in service layer
   - Implement `delete_task.py` CLI command
   - Update `main.py` routing
   - Run tests → Verify all PASS

3. **REFACTOR Phase**: Clean up code (if needed)
   - Review for DRY violations
   - Ensure consistency with existing patterns
   - Run tests → Verify still PASS

---

### Phase 2: Task Decomposition

**Status**: ⏳ PENDING - Execute via `/sp.tasks` command

**Expected Output**: `tasks.md` with:
- Setup tasks (if any project structure changes needed)
- Unit test tasks (RED phase)
- Integration test tasks (RED phase)
- Implementation tasks (GREEN phase)
- Validation tasks (REFACTOR phase)
- Manual testing tasks

**Estimated Task Count**: ~20-25 tasks total
- Similar scope to Add Task feature (single user story, simpler than Update Task)

---

## File Changes Summary

### New Files (2)
1. `src/cli/delete_task.py` (~60 lines) - CLI command implementation
2. `tests/integration/test_delete_task_integration.py` (~40 lines) - Integration tests

### Modified Files (2)
1. `src/services/task_service.py` - Add `delete_task()` function (~20 lines)
2. `tests/unit/test_task_service.py` - Add 6 unit tests (~60 lines)
3. `src/main.py` - Add "delete" command routing (~3 lines)

### Total LOC Estimate: ~183 lines
- Service layer: ~20 lines
- CLI layer: ~60 lines
- Main routing: ~3 lines
- Unit tests: ~60 lines
- Integration tests: ~40 lines

**Comparison with related features**:
- Add Task: ~250 LOC
- Update Task: ~295 LOC
- **Delete Task: ~183 LOC** (simplest CRUD operation)

---

## Risk Analysis

### Technical Risks

1. **Accidental Deletion** (Medium Risk)
   - **Mitigation**: Clear confirmation message showing what was deleted, no auto-deletion features
   - **Assumption**: User is intentional with delete command (spec assumption A-005)

2. **No Undo Mechanism** (Low Risk)
   - **Mitigation**: Spec explicitly states permanent deletion (FR-012), user must be careful
   - **Phase II Consideration**: Could add soft delete or trash/archive feature if needed

### Implementation Risks

1. **Storage Consistency** (Low Risk)
   - **Mitigation**: Python dict operations are atomic in CPython (GIL), no race conditions in single-process CLI

2. **Error Message Consistency** (Low Risk)
   - **Mitigation**: Follow exact error format from spec.md and contracts/cli-interface.md

---

## Dependencies

### Feature Dependencies
- **Add Task** (001-add-task): REQUIRED - Must be able to create tasks before deleting them
- **View Task List** (002-view-task-list): RECOMMENDED - Users need to see task IDs for deletion

### Code Dependencies
- `src/models/task.py` (Task dataclass) - No changes required
- `src/services/task_service.py` (_tasks storage) - Add delete_task() function
- `src/main.py` (command router) - Add "delete" command

---

## Testing Strategy

### Unit Tests (~6 tests)

**Service Layer** (`test_task_service.py`):
1. Test successful deletion returns deleted Task
2. Test task is removed from storage after deletion
3. Test delete raises KeyError for non-existent task ID
4. Test delete works regardless of task status (complete/incomplete)
5. Test delete with Unicode characters in task data
6. Test delete from storage with multiple tasks (only deletes specified task)

### Integration Tests (~4 tests)

**CLI Layer** (`test_delete_task_integration.py`):
1. Test delete command success message format (in-process test)
2. Test delete command error message for non-existent ID (subprocess)
3. Test delete --help displays correct usage (subprocess)
4. Test delete with no task ID argument shows error (subprocess)

**Test Coverage Goal**: >90% for service layer, >80% for CLI layer

---

## Validation Checklist

Before marking feature complete, verify:

- [ ] All 7 success criteria met (SC-001 through SC-007)
- [ ] All 12 functional requirements implemented (FR-001 through FR-012)
- [ ] All 8 edge cases handled correctly
- [ ] Test coverage >90% for service layer
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Manual testing confirms CLI behavior
- [ ] Error messages match specification exactly
- [ ] Unicode characters display correctly
- [ ] Help text matches contract specification
- [ ] Constitution compliance verified (all 8 principles)
- [ ] Code follows existing patterns (modularity, clean code)
- [ ] No manual coding used (AI-generated only via Claude Code)

---

## Appendix: Comparison with Existing Features

| Feature | User Stories | FRs | Tests | LOC | Complexity |
|---------|-------------|-----|-------|-----|------------|
| Add Task | 2 | 11 | 16 | ~250 | Medium |
| View Task List | 3 | 9 | 15 | ~200 | Medium |
| Update Task | 3 | 16 | 17 | ~295 | High |
| **Delete Task** | **1** | **12** | **~10** | **~183** | **Low** |

**Analysis**: Delete Task is the simplest CRUD operation. Single user story, straightforward logic (lookup + delete), minimal edge cases compared to Update Task's partial update complexity.

---

**Plan Status**: ✅ READY FOR TASK DECOMPOSITION

**Next Step**: Execute `/sp.tasks` to generate task breakdown with Test-First Development workflow
