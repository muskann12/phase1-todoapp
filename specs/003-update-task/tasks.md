---
description: "Task list for Update Task feature implementation"
---

# Tasks: Update Task

**Input**: Design documents from `/specs/003-update-task/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/cli-interface.md

**Tests**: Tests are included following Test-First Development (Constitution Principle V - NON-NEGOTIABLE)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths use forward slashes for cross-platform compatibility

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure (already complete from Add Task and View Task List features)

**Status**: ✅ COMPLETE (no additional setup needed for Update Task)

**Rationale**: Update Task reuses existing project structure, pytest configuration, .gitignore, and __init__.py files from Add Task and View Task List features. No new setup tasks required.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T001 [P] Add update_task() function to src/services/task_service.py (takes task_id, optional title, optional description; returns updated Task; raises KeyError if not found, ValueError if no updates or validation fails)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Update Task Title (Priority: P1) 🎯 MVP

**Goal**: Enable users to update a task's title without changing description using task ID via CLI

**Independent Test**: Create task with title "Buy mlk", update title to "Buy milk" using task ID, verify title changed and description unchanged

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T002 [P] [US1] Write unit test for update_task() with title-only update in tests/unit/test_task_service.py
- [x] T003 [P] [US1] Write unit test for update_task() preserving description when updating title in tests/unit/test_task_service.py
- [x] T004 [P] [US1] Write unit test for update_task() raising KeyError for non-existent task ID in tests/unit/test_task_service.py
- [x] T005 [P] [US1] Write unit test for update_task() raising ValueError for empty title in tests/unit/test_task_service.py
- [x] T006 [P] [US1] Write unit test for update_task() raising ValueError for title > 500 chars in tests/unit/test_task_service.py
- [x] T007 [P] [US1] Write integration test for CLI update with --title flag in tests/integration/test_update_task_integration.py
- [x] T008 [P] [US1] Write integration test for CLI update --help display in tests/integration/test_update_task_integration.py

### Run Tests (Verify RED Phase)

- [x] T009 [US1] Run all User Story 1 tests with pytest → Verify all tests FAIL (Red phase)

### Implementation for User Story 1

- [x] T010 [US1] Create src/cli/update_task.py with update_task_command() function (argparse with task_id positional + --title optional flag, validate at least one flag provided, call update_task service, handle exceptions, print success/error)
- [x] T011 [US1] Add "update" command routing to src/main.py (import update_task_command, add elif block, update help text)

### Run Tests (Verify GREEN Phase)

- [x] T012 [US1] Run all User Story 1 tests with pytest → Verify all tests PASS (Green phase)

### Refactor (if needed)

- [x] T013 [US1] Review code for DRY violations and refactor if needed (preserve test passing)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Update Task Description (Priority: P2)

**Goal**: Enable users to update a task's description without changing title using task ID via CLI

**Independent Test**: Create task with empty description, update description to "Details here" using task ID, verify description changed and title unchanged

### Tests for User Story 2 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T014 [P] [US2] Write unit test for update_task() with description-only update in tests/unit/test_task_service.py
- [x] T015 [P] [US2] Write unit test for update_task() preserving title when updating description in tests/unit/test_task_service.py
- [x] T016 [P] [US2] Write unit test for update_task() allowing empty description (clearing) in tests/unit/test_task_service.py
- [x] T017 [P] [US2] Write unit test for update_task() raising ValueError for description > 2000 chars in tests/unit/test_task_service.py
- [x] T018 [P] [US2] Write integration test for CLI update with --description flag in tests/integration/test_update_task_integration.py

### Run Tests (Verify RED Phase)

- [x] T019 [US2] Run User Story 2 tests with pytest → Verify tests FAIL (Red phase)

### Implementation for User Story 2

- [x] T020 [US2] Add --description flag support to src/cli/update_task.py (argparse configuration, pass to update_task service, handle in success output)

### Run Tests (Verify GREEN Phase)

- [x] T021 [US2] Run all tests (US1 + US2) with pytest → Verify all tests PASS (Green phase)

### Refactor (if needed)

- [x] T022 [US2] Review code for improvements and refactor if needed (preserve test passing)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Both Title and Description (Priority: P3)

**Goal**: Enable users to update both title and description simultaneously in one command using task ID

**Independent Test**: Create task, update both title and description in one command, verify both fields changed

### Tests for User Story 3 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T023 [P] [US3] Write unit test for update_task() with both title and description updated in tests/unit/test_task_service.py
- [x] T024 [P] [US3] Write unit test for update_task() raising ValueError when neither title nor description provided in tests/unit/test_task_service.py
- [x] T025 [P] [US3] Write unit test for update_task() preserving immutable fields (id, created, status) in tests/unit/test_task_service.py
- [x] T026 [P] [US3] Write integration test for CLI update with both --title and --description flags in tests/integration/test_update_task_integration.py
- [x] T027 [P] [US3] Write integration test for CLI update with Unicode characters in tests/integration/test_update_task_integration.py

### Run Tests (Verify RED Phase)

- [x] T028 [US3] Run User Story 3 tests with pytest → Verify tests FAIL (Red phase)

### Implementation for User Story 3

- [x] T029 [US3] Verify src/cli/update_task.py handles both flags simultaneously (should already work from US1+US2, add validation)
- [x] T030 [US3] Add validation in src/cli/update_task.py for "no updates provided" error when neither flag given

### Run Tests (Verify GREEN Phase)

- [x] T031 [US3] Run all tests (US1 + US2 + US3) with pytest → Verify all tests PASS (Green phase)

### Refactor (if needed)

- [x] T032 [US3] Review code for final improvements and refactor if needed (preserve test passing)

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T033 [P] Verify docstrings exist for all public functions in src/cli/update_task.py and src/services/task_service.py (update_task, update_task_command)
- [x] T034 [P] Verify type hints exist for all function signatures in src/cli/update_task.py and src/services/task_service.py
- [x] T035 Run full test suite with coverage report (pytest --cov=src tests/)
- [x] T036 Verify coverage for src/services/task_service.py >90% (update_task function)
- [x] T037 [P] Manual validation: Test updating title only preserves description
- [x] T038 [P] Manual validation: Test updating description only preserves title
- [x] T039 [P] Manual validation: Test updating both title and description simultaneously
- [x] T040 [P] Manual validation: Test error message for non-existent task ID
- [x] T041 [P] Manual validation: Test error message for empty title
- [x] T042 [P] Manual validation: Test error message for no updates provided
- [x] T043 [P] Manual validation: Test Unicode characters display correctly (create task with "Café ☕", update with "日本語")
- [x] T044 [P] Manual validation: Test help text displays correctly (python -m src.main update --help)
- [x] T045 Verify all 9 success criteria from spec.md (SC-001 through SC-009)
- [x] T046 Final code review: Verify modularity, clean code principles, constitution compliance

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: ✅ COMPLETE (reused from Add Task and View Task List features)
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User Story 1 (P1): Can start after Foundational (Phase 2) - No dependencies on other stories
  - User Story 2 (P2): Can start after Foundational (Phase 2) - Extends US1 CLI but independently testable
  - User Story 3 (P3): Can start after Foundational (Phase 2) - Combines US1+US2 but independently testable
- **Polish (Final Phase)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Adds --description flag to existing CLI (builds on US1 implementation but independently testable)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Uses both flags from US1+US2 (validates combined usage but independently testable)

**Note**: While US2 and US3 build on US1's CLI implementation, each story is independently testable and can be validated in isolation.

### Within Each User Story

- Tests MUST be written and FAIL before implementation (Test-First Development)
- Within User Story 1:
  - T002-T008 (tests) before T009 (run tests - RED)
  - T009 (verify RED) before T010-T011 (implementation)
  - T010-T011 (implementation) before T012 (run tests - GREEN)
  - T012 (verify GREEN) before T013 (refactor)
- Within User Story 2:
  - T014-T018 (tests) before T019 (run tests - RED)
  - T019 (verify RED) before T020 (implementation)
  - T020 (implementation) before T021 (run tests - GREEN)
  - T021 (verify GREEN) before T022 (refactor)
- Within User Story 3:
  - T023-T027 (tests) before T028 (run tests - RED)
  - T028 (verify RED) before T029-T030 (implementation)
  - T029-T030 (implementation) before T031 (run tests - GREEN)
  - T031 (verify GREEN) before T032 (refactor)

### Parallel Opportunities

- Foundational phase: T001 is single task (no parallel opportunities)
- Within User Story 1:
  - T002-T008 (all test writing tasks) can run in parallel
  - T010-T011 (implementation tasks) can run in parallel if different developers
- Within User Story 2:
  - T014-T018 (test writing tasks) can run in parallel
- Within User Story 3:
  - T023-T027 (test writing tasks) can run in parallel
- Polish phase: Most tasks marked [P] can run in parallel (T033-T044)

---

## Parallel Example: User Story 1 Tests

```bash
# Launch all test writing tasks for User Story 1 together:
Task: "Write unit test for update_task() with title-only update"
Task: "Write unit test for update_task() preserving description"
Task: "Write unit test for update_task() raising KeyError for non-existent ID"
Task: "Write unit test for update_task() raising ValueError for empty title"
Task: "Write unit test for update_task() raising ValueError for title > 500 chars"
Task: "Write integration test for CLI update with --title flag"
Task: "Write integration test for CLI update --help display"

# Then verify RED phase before proceeding to implementation
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (✅ already done)
2. Complete Phase 2: Foundational (T001 - add update_task())
3. Complete Phase 3: User Story 1 (tests → RED → implementation → GREEN → refactor)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Validate (MVP!)
3. Add User Story 2 → Test independently → Validate
4. Add User Story 3 → Test independently → Validate
5. Polish & Cross-Cutting → Final validation
6. Each story adds value without breaking previous stories

### Sequential Execution Order

If implementing alone or in strict order:

1. T001 (Foundational - add update_task())
2. **User Story 1** (MVP):
   - T002-T008 (Write tests)
   - T009 (Verify RED)
   - T010-T011 (Implementation)
   - T012 (Verify GREEN)
   - T013 (Refactor)
3. **User Story 2**:
   - T014-T018 (Write tests)
   - T019 (Verify RED)
   - T020 (Implementation)
   - T021 (Verify GREEN)
   - T022 (Refactor)
4. **User Story 3**:
   - T023-T027 (Write tests)
   - T028 (Verify RED)
   - T029-T030 (Implementation)
   - T031 (Verify GREEN)
   - T032 (Refactor)
5. T033-T046 (Polish & Validation)

---

## Test-First Development Checkpoints

**Constitution Principle V: Test-First Development (NON-NEGOTIABLE)**

Each user story follows Red-Green-Refactor cycle:

### User Story 1 Checkpoints:

1. **Tests Written**: T002-T008 complete
2. **Red Phase**: T009 confirms all tests FAIL
3. **Implementation**: T010-T011 complete
4. **Green Phase**: T012 confirms all tests PASS
5. **Refactor**: T013 improves code while keeping tests green

### User Story 2 Checkpoints:

1. **Tests Written**: T014-T018 complete
2. **Red Phase**: T019 confirms tests FAIL
3. **Implementation**: T020 complete
4. **Green Phase**: T021 confirms all tests PASS (including US1 regression)
5. **Refactor**: T022 improves code while keeping tests green

### User Story 3 Checkpoints:

1. **Tests Written**: T023-T027 complete
2. **Red Phase**: T028 confirms tests FAIL
3. **Implementation**: T029-T030 complete
4. **Green Phase**: T031 confirms all tests PASS (including US1+US2 regression)
5. **Refactor**: T032 improves code while keeping tests green

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

**Total Tasks**: 46 tasks

**Breakdown by Phase**:
- Phase 1 (Setup): 0 tasks (already complete from Add Task and View Task List)
- Phase 2 (Foundational): 1 task (BLOCKING)
- Phase 3 (User Story 1 - P1): 12 tasks (7 tests + 1 verify RED + 2 implementation + 1 verify GREEN + 1 refactor)
- Phase 4 (User Story 2 - P2): 9 tasks (5 tests + 1 verify RED + 1 implementation + 1 verify GREEN + 1 refactor)
- Phase 5 (User Story 3 - P3): 10 tasks (5 tests + 1 verify RED + 2 implementation + 1 verify GREEN + 1 refactor)
- Phase 6 (Polish): 14 tasks

**Parallel Opportunities**: 24 tasks marked [P] can run in parallel

**MVP Scope**: Phases 1, 2, 3 (User Story 1) = 13 tasks

**Constitution Compliance**:
- ✅ Test-First Development: RED-GREEN-REFACTOR cycle enforced per user story
- ✅ Small, Testable Changes: Each user story independently testable
- ✅ Modularity: Clear separation (service layer, CLI layer, main routing)
- ✅ Explicit: All file paths specified, all validation explicit

**Ready for**: `/sp.implement` command to execute tasks
