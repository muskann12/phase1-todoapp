# Implementation Plan: View Task List

**Branch**: `002-view-task-list` | **Date**: 2025-12-31 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-view-task-list/spec.md`

## Summary

View Task List is a read-only CLI feature that displays all tasks stored in memory with their ID, title, description, and status. Users can see a summary of total, incomplete, and complete tasks, followed by individual task entries sorted by ID in ascending order. The feature reuses the existing Add Task infrastructure (Task entity, in-memory storage, service layer) and requires only CLI display logic and a new `get_all_tasks()` service function.

**Technical Approach**: Retrieve all tasks from the existing `_tasks` dict, sort by ID for deterministic output, format with status indicators (`[ ]` / `[✓]`), and display with summary counts. Empty lists show onboarding message. Implementation follows Test-First Development with 8 tests (3 unit, 5 integration).

---

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Standard library only (argparse, dataclasses, enum - already used in Add Task)
**Storage**: In-memory dict[str, Task] (reused from Add Task feature)
**Testing**: pytest (already configured)
**Target Platform**: CLI (Windows/Linux/Mac with UTF-8 terminal)
**Project Type**: Single project (src/ and tests/ at repository root)
**Performance Goals**: Display all tasks in under 2 seconds (even for 1000+ tasks)
**Constraints**: In-memory only (no persistence), CLI only (no GUI), read-only (no data modification)
**Scale/Scope**: Support 1000+ tasks without pagination; no filtering/search in Phase I

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Pre-Phase 0 Check (Before Research)

| Principle | Requirement | Status | Notes |
|-----------|-------------|--------|-------|
| I. Specifications as SSoT | Feature spec exists and complete | ✅ PASS | spec.md created with 2 user stories, 10 FRs, 6 SCs |
| II. AI-Generated Code Only | No manual coding permitted | ✅ PASS | Implementation via Claude Code only |
| III. Reusable Intelligence | Reuse existing patterns | ✅ PASS | Reuses Task entity, in-memory storage, service layer from Add Task |
| IV. Five-Step Workflow | Spec → Plan → Tasks → Implement → Validate | ✅ PASS | Currently in Step 2 (Plan phase) |
| V. Test-First Development | Tests before implementation, RED-GREEN-REFACTOR | ✅ PASS | 8 tests planned (3 unit, 5 integration); RED-GREEN-REFACTOR enforced |
| VI. Modularity and Clean Code | Separation of concerns, clean code | ✅ PASS | Service layer (`get_all_tasks`), CLI layer (`view_tasks.py`), main routing |
| VII. Explicit Over Implicit | No ambiguities | ✅ PASS | All requirements explicit; no [NEEDS CLARIFICATION] markers |
| VIII. Small, Testable Changes | Minimal diff, independently testable | ✅ PASS | ~150 LOC total; each user story independently testable |

**Phase I Constraints Check**:
- ✅ In-memory storage only (no file I/O, no database)
- ✅ Python CLI only (no GUI, no web interface)
- ✅ Python 3.13+ required
- ✅ Feature #2 of 5 planned features (Add Task, **View Task List**, Delete Task, Update Task, Mark Complete/Incomplete)

**Gate Result**: ✅ PASS - Proceed to Phase 0 (Research)

---

### Post-Phase 1 Check (After Design)

| Principle | Requirement | Status | Notes |
|-----------|-------------|--------|-------|
| I. Specifications as SSoT | Design matches spec | ✅ PASS | research.md, data-model.md, contracts/cli-interface.md, quickstart.md all align with spec.md |
| II. AI-Generated Code Only | Design for AI implementation | ✅ PASS | Quickstart provides complete code templates for Claude Code |
| III. Reusable Intelligence | Leverages existing infrastructure | ✅ PASS | Reuses Task, TaskStatus, _tasks dict, argparse pattern from Add Task |
| IV. Five-Step Workflow | Plan complete before tasks | ✅ PASS | Plan phase complete; ready for Step 3 (Tasks) |
| V. Test-First Development | Test strategy defined | ✅ PASS | 8 tests specified; RED-GREEN-REFACTOR workflow documented in quickstart |
| VI. Modularity and Clean Code | Clean architecture | ✅ PASS | Service (`get_all_tasks`), CLI (`view_tasks.py`), Main (routing) - clear separation |
| VII. Explicit Over Implicit | All decisions documented | ✅ PASS | 5 research decisions, CLI contract, test cases all explicit |
| VIII. Small, Testable Changes | Minimal implementation | ✅ PASS | 2 new files, 2 modified files, ~150 LOC total |

**Constitution Compliance**: ✅ VERIFIED - Ready for Phase 2 (Task Decomposition)

---

## Project Structure

### Documentation (this feature)

```text
specs/002-view-task-list/
├── spec.md                      # Feature specification (User Stories, FRs, SCs)
├── plan.md                      # This file (/sp.plan output)
├── research.md                  # Phase 0: Technical decisions (5 decisions)
├── data-model.md                # Phase 1: Data model (reuses Task entity)
├── quickstart.md                # Phase 1: Implementation guide with code templates
├── contracts/
│   └── cli-interface.md         # Phase 1: CLI contract specification
├── checklists/
│   └── requirements.md          # Specification quality checklist (14 items, all passed)
└── tasks.md                     # Phase 2: Task decomposition (NOT created yet - awaits /sp.tasks)
```

---

### Source Code (repository root)

```text
src/
├── models/
│   └── task.py                  # Task entity, TaskStatus enum (REUSED from Add Task)
├── services/
│   └── task_service.py          # ADD: get_all_tasks() function
├── cli/
│   ├── add_task.py              # Existing (Add Task feature)
│   └── view_tasks.py            # NEW: View Task List CLI command
└── main.py                      # UPDATE: Add "view" command routing

tests/
├── unit/
│   ├── test_task_model.py       # Existing (Add Task tests)
│   └── test_task_service.py     # ADD: 3 tests for get_all_tasks()
└── integration/
    ├── test_add_task_integration.py      # Existing (Add Task tests)
    └── test_view_tasks_integration.py    # NEW: 5 CLI integration tests
```

**Structure Decision**: Single project layout (default). View Task List reuses existing src/models and src/services structure from Add Task feature. Only adds new CLI module and tests.

---

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**No violations** - Constitution fully compliant. No complexity justifications needed.

---

## Phase 0: Research (COMPLETED)

**Input**: Feature specification with unknowns marked as "NEEDS CLARIFICATION"

**Output**: `research.md` with all technical decisions resolved

**Status**: ✅ COMPLETE

### Research Decisions Made

1. **Task Retrieval and Sorting**
   - Decision: Use `get_all_tasks()` returning sorted list by ID (ascending)
   - Rationale: Deterministic order for testing, reuses existing infrastructure
   - Alternatives rejected: Sort by timestamp (less deterministic), no sorting (not explicit)

2. **CLI Output Formatting**
   - Decision: Multi-line format with status indicators and summary
   - Rationale: Readability, scannability, matches spec display rules
   - Alternatives rejected: Table format (out of scope), JSON (not user-friendly), single-line (hard to read)

3. **Empty-State Handling**
   - Decision: Display onboarding message with Add Task example
   - Rationale: User guidance, spec requirement, prevents confusion
   - Alternative: Empty output rejected (looks like error)

4. **Task Count Summary Display**
   - Decision: Summary as first line before task entries (User Story 2)
   - Rationale: At-a-glance visibility, spec FR-009 requirement
   - Conditional: Only show when tasks exist

5. **Unicode and Special Character Handling**
   - Decision: Display exactly as stored with UTF-8 support
   - Rationale: Spec FR-008 requirement, Python 3 native UTF-8, no sanitization needed for CLI
   - Terminal assumption: UTF-8 support (spec Assumption #6)

**Artifacts**: [research.md](research.md)

---

## Phase 1: Design & Contracts (COMPLETED)

**Input**: Research decisions from Phase 0

**Output**: Data model, API contracts, implementation quickstart

**Status**: ✅ COMPLETE

### 1. Data Model Design

**File**: `data-model.md`

**Summary**: View Task List is read-only and reuses all entities from Add Task feature. No new entities required.

**Reused Entities**:
- Task (id, title, description, status, created)
- TaskStatus enum (INCOMPLETE, COMPLETE)
- In-memory storage dict (_tasks)

**New Service Function**:
- `get_all_tasks() -> list[Task]` (returns sorted tasks)

**Read-Only Guarantee**: View operation does not add, remove, or modify tasks. Pre/post-condition verification in tests.

**Artifacts**: [data-model.md](data-model.md)

---

### 2. CLI Contract Specification

**File**: `contracts/cli-interface.md`

**Command**: `python -m src.main view`

**Arguments**: None (displays all tasks)

**Success Scenarios**:
1. View tasks with mixed statuses (display all with summary)
2. View empty list (onboarding message)
3. View single task (summary + task entry)
4. View tasks with Unicode (correct display)
5. View large list (1000+ tasks, no pagination)

**Output Format**:
```text
Total: {count} | Incomplete: {incomplete} | Complete: {complete}

[ ] ID: {uuid}
    Title: {title}
    Description: {description or "(none)"}
    Status: {status}
```

**Exit Codes**: Always 0 (success, including empty list)

**Performance**: Under 2 seconds for 1000+ tasks (SC-001)

**Artifacts**: [contracts/cli-interface.md](contracts/cli-interface.md)

---

### 3. Implementation Quickstart

**File**: `quickstart.md`

**Implementation Steps**:
1. Extend service layer: Add `get_all_tasks()` to `task_service.py`
2. Create CLI module: `src/cli/view_tasks.py` with `view_tasks_command()`
3. Update main entry: Add "view" command routing to `main.py`

**Test-First Workflow**:
- **RED Phase**: Write 8 tests first (3 unit, 5 integration), verify they FAIL
- **GREEN Phase**: Implement code, verify all tests PASS
- **REFACTOR Phase**: Review for improvements (expected: clean from start)

**Files Created**: 2 new files (~140 LOC)
**Files Modified**: 2 existing files (~10 LOC added)
**Tests**: 8 tests (3 unit, 5 integration)

**Artifacts**: [quickstart.md](quickstart.md)

---

## Phase 2: Task Decomposition (NOT STARTED)

**Status**: ⏳ PENDING - Awaiting `/sp.tasks` command

**Expected Output**: `tasks.md` with discrete, testable tasks organized by user story

**Estimated Tasks**:
- Phase 1: Setup (pytest configuration - already done)
- Phase 2: Foundational (service layer - add `get_all_tasks()`)
- Phase 3: User Story 1 - View All Tasks (tests → RED → implementation → GREEN → refactor)
- Phase 4: User Story 2 - View Task Count Summary (tests → RED → implementation → GREEN → refactor)
- Phase 5: Polish & Validation (coverage, manual testing, success criteria verification)

**Next Command**: `/sp.tasks` to generate task breakdown

---

## Ready for Implementation

**Prerequisites Met**:
- ✅ Specification complete and validated (14 checklist items passed)
- ✅ Constitution check passed (all 8 principles compliant)
- ✅ Research complete (5 technical decisions resolved)
- ✅ Data model defined (reuses existing Task entity)
- ✅ CLI contract specified (complete input/output spec)
- ✅ Quickstart guide created (step-by-step implementation)
- ✅ Test strategy defined (8 tests, RED-GREEN-REFACTOR workflow)

**Next Steps**:
1. Run `/sp.tasks` to generate task decomposition
2. Review and approve task breakdown
3. Run `/sp.implement` to execute Test-First Development
4. Validate against 6 success criteria (SC-001 through SC-006)

**Estimated Effort**:
- Implementation: ~150 lines of code + tests
- Test-First cycles: 2 cycles (US1 + US2)
- Validation: Manual testing + coverage report

---

## Risk Analysis

### Low Risk Items

- ✅ **Code reuse**: Leverages proven Add Task infrastructure (Task, storage, service layer)
- ✅ **No new dependencies**: Uses standard library only
- ✅ **Simple logic**: Read-only operation, no complex algorithms
- ✅ **Well-defined spec**: No ambiguities, all requirements explicit

### Mitigation Strategies

**Risk**: Unicode display issues on Windows terminals
- **Mitigation**: Document UTF-8 terminal setup in troubleshooting; test on Windows/Linux/Mac

**Risk**: Performance degradation with 10,000+ tasks
- **Mitigation**: Performance test with 1000 tasks; verify under 2-second limit (SC-001)

**Risk**: Regression in Add Task feature
- **Mitigation**: Run full test suite (Add Task + View Task List) after implementation

---

## Success Criteria Validation Plan

After implementation, verify:

- **SC-001**: View completes in under 2 seconds
  - Test: Create 1000 tasks, measure view execution time
  - Expected: < 2 seconds

- **SC-002**: Deterministic sort order (ascending by ID) 100% of time
  - Test: Run view 10 times, verify ID order identical each time
  - Expected: Same order every run

- **SC-003**: Empty-state message displays 100% of time
  - Test: View with 0 tasks, verify onboarding message
  - Expected: "No tasks found. Add your first task..."

- **SC-004**: Unicode displayed correctly (emoji, accents)
  - Test: Create task with "Café ☕", view and verify exact display
  - Expected: Characters displayed without corruption

- **SC-005**: Summary counts accurate 100% of time
  - Test: Create 10 tasks (7 incomplete, 3 complete), verify summary
  - Expected: "Total: 10 | Incomplete: 7 | Complete: 3"

- **SC-006**: Read-only guarantee (no data mutation)
  - Test: Count tasks before/after view, verify unchanged
  - Expected: Task count and task fields identical

---

## Appendix: Files Generated by /sp.plan

1. ✅ `research.md` - 5 technical decisions with rationale
2. ✅ `data-model.md` - Entity reference (reuses Task)
3. ✅ `contracts/cli-interface.md` - Complete CLI specification
4. ✅ `quickstart.md` - Step-by-step implementation guide
5. ✅ `plan.md` - This file (technical context, phase summaries, constitution check)

**Total Documentation**: ~2500 lines across 5 files

**Ready for**: `/sp.tasks` command
