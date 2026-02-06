# Implementation Plan: Toggle Task Status

**Branch**: `005-toggle-task-status` | **Date**: 2026-01-01 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/005-toggle-task-status/spec.md`

## Summary

The Toggle Task Status feature enables users to change task completion status via three CLI commands: `complete`, `incomplete`, and `toggle`. This builds upon the existing Task model (TaskStatus enum with INCOMPLETE and COMPLETE values) and follows established patterns from Update Task (003) and Delete Task (004). Implementation adds three service layer functions and three CLI command modules plus main router updates. Total estimated LOC: ~476 lines.

**Key Technical Approach**: Create three service functions (`mark_complete()`, `mark_incomplete()`, `toggle_status()`) for clear separation of concerns, three separate CLI command files for modularity, and leverage existing Task dataclass mutation pattern from Update Task. All operations are idempotent per spec requirements.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: argparse (stdlib), pytest (testing)
**Storage**: In-memory dictionary `Dict[str, Task]` (Phase I constraint)
**Testing**: pytest with Test-First Development (RED-GREEN-REFACTOR cycle)
**Target Platform**: CLI (Windows/Linux/macOS)
**Project Type**: Single Python CLI project
**Performance Goals**: Status change operation completes in <1 second (O(1) dict operations)
**Constraints**: In-memory only, no persistence, session-scoped changes
**Scale/Scope**: MVP scope - three commands, ~476 LOC total, ~23 tests (11 unit + 12 integration)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ I. Specifications as Single Source of Truth
- **Status**: PASS
- **Evidence**: All behavior documented in spec.md (three user stories, 16 FRs, 8 success criteria)
- **Action**: Proceed - spec complete and unambiguous

### ✅ II. AI-Generated Code Only
- **Status**: PASS
- **Evidence**: Implementation will be via `/sp.implement` command (Claude Code only)
- **Action**: Ensure manual coding remains prohibited

### ✅ III. Reusable Intelligence Encouraged
- **Status**: PASS
- **Evidence**: Reuses Task model, service pattern, CLI pattern from existing features (Add/Update/Delete)
- **Action**: Follow established patterns from specs/003-update-task and specs/004-delete-task

### ✅ IV. Mandatory Five-Step Workflow
- **Status**: PASS (Step 2/5)
- **Evidence**: Spec complete (step 1), this is planning (step 2), tasks next (step 3), implement (step 4), validate (step 5)
- **Action**: Generate tasks.md after plan complete

### ✅ V. Test-First Development (NON-NEGOTIABLE)
- **Status**: PASS
- **Evidence**: Plan mandates RED-GREEN-REFACTOR cycle in quickstart.md
- **Action**: Ensure tests written BEFORE implementation in tasks.md

### ✅ VI. Modularity and Clean Code
- **Status**: PASS
- **Evidence**: Service/CLI separation, three focused functions, clear naming
- **Action**: Follow existing separation pattern

### ✅ VII. Explicit Over Implicit
- **Status**: PASS
- **Evidence**: All edge cases defined, idempotent behavior explicit, error formats specified
- **Action**: No clarifications needed - implementation can proceed

### ✅ VIII. Small, Testable Changes
- **Status**: PASS
- **Evidence**: Three independently testable user stories, minimal diff per command
- **Action**: Each command implementation is independently testable

**Constitution Check Result**: ✅ **ALL 8 GATES PASS** - Proceed to implementation

## Project Structure

### Documentation (this feature)

```text
specs/005-toggle-task-status/
├── plan.md              # This file
├── research.md          # Phase 0: Technical decisions
├── data-model.md        # Phase 1: Status transition model
├── quickstart.md        # Phase 1: TDD workflow guide
├── contracts/
│   └── cli-interface.md # Phase 1: CLI command contracts
└── tasks.md             # Phase 2: /sp.tasks command output (NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── models/
│   └── task.py          # Existing - Task dataclass, TaskStatus enum (NO CHANGES)
├── services/
│   └── task_service.py  # MODIFY - Add mark_complete(), mark_incomplete(), toggle_status()
├── cli/
│   ├── complete_task.py    # NEW - Complete command
│   ├── incomplete_task.py  # NEW - Incomplete command
│   └── toggle_task.py      # NEW - Toggle command
└── main.py              # MODIFY - Add three command routes

tests/
├── integration/
│   ├── test_complete_task_integration.py    # NEW - 4 tests
│   ├── test_incomplete_task_integration.py  # NEW - 4 tests
│   └── test_toggle_task_integration.py      # NEW - 4 tests
└── unit/
    └── test_task_service.py  # MODIFY - Add 11 unit tests
```

**Structure Decision**: Single Python CLI project (Option 1). Reuses existing src/ and tests/ structure from Add/Update/Delete Task features.

## File Changes Summary

### New Files (6 total)

**CLI Layer** (3 files):
1. `src/cli/complete_task.py` (~55 lines)
2. `src/cli/incomplete_task.py` (~55 lines)
3. `src/cli/toggle_task.py` (~55 lines)

**Integration Tests** (3 files):
4. `tests/integration/test_complete_task_integration.py` (~40 lines)
5. `tests/integration/test_incomplete_task_integration.py` (~40 lines)
6. `tests/integration/test_toggle_task_integration.py` (~45 lines)

### Modified Files (3 total)

1. **`src/services/task_service.py`** (+~65 lines)
   - Add `mark_complete(task_id: str) -> Task` (~20 lines)
   - Add `mark_incomplete(task_id: str) -> Task` (~20 lines)
   - Add `toggle_status(task_id: str) -> Task` (~25 lines)

2. **`tests/unit/test_task_service.py`** (+~110 lines)
   - Add 11 unit tests for status change functions

3. **`src/main.py`** (+~11 lines)
   - Add three command routing blocks (~9 lines)
   - Update help text (~2 lines)

### Total LOC Estimate: ~476 lines

- Service layer: ~65 lines
- CLI layer: ~165 lines
- Main routing: ~11 lines
- Unit tests: ~110 lines
- Integration tests: ~125 lines

**Comparison**:
- Add Task: ~250 LOC
- Update Task: ~295 LOC
- Delete Task: ~183 LOC
- **Toggle Task Status: ~476 LOC** (three commands = more code, but follows same patterns)

## Implementation Strategy

**Approach**: Test-First Development with three independent user stories

**Phase 1 - User Story 1 (P1 - MVP)**: Mark Task as Complete
- Service: `mark_complete()` function
- CLI: `complete_task.py` command
- Tests: 4 unit tests + 4 integration tests
- Independent delivery: Complete command works standalone

**Phase 2 - User Story 2 (P2)**: Mark Task as Incomplete
- Service: `mark_incomplete()` function
- CLI: `incomplete_task.py` command
- Tests: 4 unit tests + 4 integration tests
- Independent delivery: Incomplete command works standalone

**Phase 3 - User Story 3 (P3)**: Toggle Task Status
- Service: `toggle_status()` function
- CLI: `toggle_task.py` command
- Tests: 3 unit tests + 4 integration tests
- Independent delivery: Toggle command works standalone

**Total Tests**: 11 unit + 12 integration = 23 tests

**Coverage Target**: >90% service layer, >80% CLI layer

## Risk Analysis

### Technical Risks

**1. Three Commands = More Code** (Medium Risk)
- **Mitigation**: Follow DRY - extract common patterns if needed
- **Impact**: Managed via refactor phase

**2. Idempotent Behavior Clarity** (Low Risk)
- **Mitigation**: Clear messages, help text documents behavior
- **Impact**: Minimal - spec explicitly defines idempotent operations

**3. Message Format Consistency** (Low Risk)
- **Mitigation**: Integration tests validate exact message format
- **Impact**: Minimal - follow existing pattern

## Dependencies

- **Add Task (001)**: REQUIRED - create tasks before changing status
- **View Task List (002)**: RECOMMENDED - verify status changes
- **Update Task (003)**: REFERENCE - Task mutation pattern
- **Delete Task (004)**: REFERENCE - CLI argument parsing pattern

## Next Steps

1. ✅ Phase 0 Complete: Research decisions documented (research.md)
2. ✅ Phase 1 Complete: Design artifacts created (data-model.md, contracts/, quickstart.md)
3. ⏭️ Phase 2 Next: Execute `/sp.tasks` to generate tasks.md
4. ⏭️ Phase 3 Next: Execute `/sp.implement` for Test-First Development

**Plan Status**: ✅ **READY FOR TASK DECOMPOSITION** (`/sp.tasks`)
