---
description: "Task list for View Task List feature implementation"
---

# Tasks: View Task List

**Input**: Design documents from `/specs/002-view-task-list/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/cli-interface.md

**Tests**: Tests are included following Test-First Development (constitution principle V)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths use forward slashes for cross-platform compatibility

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure (already complete from Add Task feature)

**Status**: ✅ COMPLETE (no additional setup needed for View Task List)

**Rationale**: View Task List reuses existing project structure, pytest configuration, .gitignore, and __init__.py files from Add Task feature. No new setup tasks required.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T001 [P] Add get_all_tasks() function to src/services/task_service.py (returns list of all tasks sorted by ID ascending)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - View All Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to view all tasks with ID, title, description, and status in ascending ID order

**Independent Test**: Create 3 tasks with different titles and statuses, run view command, verify all 3 tasks displayed with ID, title, description, status in ascending ID order

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T002 [P] [US1] Write unit test for get_all_tasks() with empty storage in tests/unit/test_task_service.py
- [x] T003 [P] [US1] Write unit test for get_all_tasks() returns tasks sorted by ID ascending in tests/unit/test_task_service.py
- [x] T004 [P] [US1] Write unit test for get_all_tasks() read-only guarantee (no storage modification) in tests/unit/test_task_service.py
- [x] T005 [P] [US1] Write integration test for CLI view with empty task list in tests/integration/test_view_tasks_integration.py
- [x] T006 [P] [US1] Write integration test for CLI view with single task in tests/integration/test_view_tasks_integration.py
- [x] T007 [P] [US1] Write integration test for CLI view with multiple tasks (verify sorting) in tests/integration/test_view_tasks_integration.py
- [x] T008 [P] [US1] Write integration test for CLI view with Unicode characters in tests/integration/test_view_tasks_integration.py
- [x] T009 [P] [US1] Write integration test for CLI view --help display in tests/integration/test_view_tasks_integration.py

### Run Tests (Verify RED Phase)

- [x] T010 [US1] Run all User Story 1 tests with pytest → Verify all tests FAIL (Red phase)

### Implementation for User Story 1

- [x] T011 [US1] Create src/cli/view_tasks.py with view_tasks_command() function (empty-state handling, task display loop, status indicators)
- [x] T012 [US1] Add "view" command routing to src/main.py (import view_tasks_command, add elif block, update help text)

### Run Tests (Verify GREEN Phase)

- [x] T013 [US1] Run all User Story 1 tests with pytest → Verify all tests PASS (Green phase)

### Refactor (if needed)

- [x] T014 [US1] Review code for DRY violations and refactor if needed (preserve test passing)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View Task Count Summary (Priority: P2)

**Goal**: Display summary line with total, incomplete, and complete task counts for at-a-glance progress

**Independent Test**: Create 10 tasks (7 incomplete, 3 complete), run view command, verify summary line shows "Total: 10 | Incomplete: 7 | Complete: 3"

### Tests for User Story 2 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T015 [P] [US2] Write integration test for CLI view with task count summary in tests/integration/test_view_tasks_integration.py
- [x] T016 [P] [US2] Write integration test for CLI view empty list has no summary (only empty-state message) in tests/integration/test_view_tasks_integration.py

### Run Tests (Verify RED Phase)

- [x] T017 [US2] Run User Story 2 tests with pytest → Verify tests FAIL (Red phase)

### Implementation for User Story 2

- [x] T018 [US2] Add summary count calculation and display logic to src/cli/view_tasks.py (before task loop, conditional on non-empty list)

### Run Tests (Verify GREEN Phase)

- [x] T019 [US2] Run all tests (US1 + US2) with pytest → Verify all tests PASS (Green phase)

### Refactor (if needed)

- [x] T020 [US2] Review code for improvements and refactor if needed (preserve test passing)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T021 [P] Verify docstrings exist for all public functions in src/cli/view_tasks.py and src/services/task_service.py (get_all_tasks, view_tasks_command)
- [ ] T022 [P] Verify type hints exist for all function signatures in src/cli/view_tasks.py and src/services/task_service.py
- [ ] T023 Run full test suite with coverage report (pytest --cov=src tests/)
- [ ] T024 Verify coverage for src/services/task_service.py >90% (get_all_tasks function)
- [ ] T025 [P] Manual validation: Test empty list displays onboarding message
- [ ] T026 [P] Manual validation: Test 3 tasks display with correct status indicators ([ ] and [✓])
- [ ] T027 [P] Manual validation: Test Unicode characters display correctly (create task with "Café ☕", verify view output)
- [ ] T028 [P] Manual validation: Test empty descriptions show "(none)"
- [ ] T029 [P] Manual validation: Test summary counts are accurate (create 10 tasks: 7 incomplete, 3 complete)
- [ ] T030 Verify all 6 success criteria from spec.md (SC-001 through SC-006)
- [ ] T031 Final code review: Verify modularity, clean code principles, constitution compliance

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: ✅ COMPLETE (reused from Add Task feature)
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User Story 1 (P1): Can start after Foundational (Phase 2) - No dependencies on other stories
  - User Story 2 (P2): Can start after Foundational (Phase 2) - Extends US1 display but independently testable
- **Polish (Final Phase)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Builds on US1 implementation but independently testable (adds summary line)

### Within Each User Story

- Tests MUST be written and FAIL before implementation (Test-First Development)
- Within User Story 1:
  - T002-T009 (tests) before T010 (run tests - RED)
  - T010 (verify RED) before T011-T012 (implementation)
  - T011-T012 (implementation) before T013 (run tests - GREEN)
  - T013 (verify GREEN) before T014 (refactor)
- Within User Story 2:
  - T015-T016 (tests) before T017 (run tests - RED)
  - T017 (verify RED) before T018 (implementation)
  - T018 (implementation) before T019 (run tests - GREEN)
  - T019 (verify GREEN) before T020 (refactor)

### Parallel Opportunities

- Foundational phase: T001 is single task (no parallel opportunities)
- Within User Story 1:
  - T002-T009 (all test writing tasks) can run in parallel
  - T011-T012 (implementation tasks) can run in parallel if different developers
- Within User Story 2:
  - T015-T016 (test writing tasks) can run in parallel
- Polish phase: Most tasks marked [P] can run in parallel (T021-T029)

---

## Parallel Example: User Story 1 Tests

```bash
# Launch all test writing tasks for User Story 1 together:
Task: "Write unit test for get_all_tasks() with empty storage"
Task: "Write unit test for get_all_tasks() returns sorted tasks"
Task: "Write unit test for get_all_tasks() read-only guarantee"
Task: "Write integration test for CLI view with empty list"
Task: "Write integration test for CLI view with single task"
Task: "Write integration test for CLI view with multiple tasks"
Task: "Write integration test for CLI view with Unicode characters"
Task: "Write integration test for CLI view --help"

# Then verify RED phase before proceeding to implementation
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (✅ already done)
2. Complete Phase 2: Foundational (T001 - add get_all_tasks())
3. Complete Phase 3: User Story 1 (tests → RED → implementation → GREEN → refactor)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Validate (MVP!)
3. Add User Story 2 → Test independently → Validate
4. Polish & Cross-Cutting → Final validation
5. Each story adds value without breaking previous stories

### Sequential Execution Order

If implementing alone or in strict order:

1. T001 (Foundational - add get_all_tasks())
2. **User Story 1** (MVP):
   - T002-T009 (Write tests)
   - T010 (Verify RED)
   - T011-T012 (Implementation)
   - T013 (Verify GREEN)
   - T014 (Refactor)
3. **User Story 2**:
   - T015-T016 (Write tests)
   - T017 (Verify RED)
   - T018 (Implementation)
   - T019 (Verify GREEN)
   - T020 (Refactor)
4. T021-T031 (Polish & Validation)

---

## Test-First Development Checkpoints

**Constitution Principle V: Test-First Development (NON-NEGOTIABLE)**

Each user story follows Red-Green-Refactor cycle:

### User Story 1 Checkpoints:

1. ✅ **Tests Written**: T002-T009 complete
2. ✅ **Red Phase**: T010 confirms all tests FAIL
3. ✅ **Implementation**: T011-T012 complete
4. ✅ **Green Phase**: T013 confirms all tests PASS
5. ✅ **Refactor**: T014 improves code while keeping tests green

### User Story 2 Checkpoints:

1. ✅ **Tests Written**: T015-T016 complete
2. ✅ **Red Phase**: T017 confirms tests FAIL
3. ✅ **Implementation**: T018 complete
4. ✅ **Green Phase**: T019 confirms all tests PASS (including US1 regression)
5. ✅ **Refactor**: T020 improves code while keeping tests green

**Validation**: If any Green phase checkpoint fails, DO NOT proceed to next user story. Fix implementation until all tests pass.

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail (RED) before implementing
- Verify tests pass (GREEN) after implementing
- Commit after each checkpoint or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Task Summary

**Total Tasks**: 31 tasks

**Breakdown by Phase**:
- Phase 1 (Setup): 0 tasks (already complete from Add Task)
- Phase 2 (Foundational): 1 task (BLOCKING)
- Phase 3 (User Story 1 - P1): 13 tasks (8 tests + 1 verify RED + 2 implementation + 1 verify GREEN + 1 refactor)
- Phase 4 (User Story 2 - P2): 6 tasks (2 tests + 1 verify RED + 1 implementation + 1 verify GREEN + 1 refactor)
- Phase 5 (Polish): 11 tasks

**Parallel Opportunities**: 18 tasks marked [P] can run in parallel

**MVP Scope**: Phases 1, 2, 3 (User Story 1) = 14 tasks

**Constitution Compliance**:
- ✅ Test-First Development: RED-GREEN-REFACTOR cycle enforced per user story
- ✅ Small, Testable Changes: Each user story independently testable
- ✅ Modularity: Clear separation (service layer, CLI layer, main routing)
- ✅ Explicit: All file paths specified, all validation explicit

**Ready for**: `/sp.implement` command to execute tasks
