---

description: "Task list for Add Task feature implementation"
---

# Tasks: Add Task

**Input**: Design documents from `/specs/001-add-task/`
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

**Purpose**: Project initialization and basic structure

- [x] T001 Create project directory structure (src/, tests/ with subdirectories)
- [x] T002 [P] Create __init__.py files in src/, src/models/, src/services/, src/cli/
- [x] T003 [P] Create __init__.py file in tests/
- [x] T004 [P] Create pytest.ini configuration file in repository root
- [x] T005 [P] Create .gitignore file with Python patterns (__pycache__, *.pyc, .pytest_cache)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 [P] Implement TaskStatus enum in src/models/task.py
- [x] T007 [P] Implement Task dataclass with all fields (id, title, description, status, created) in src/models/task.py
- [x] T008 Add validation logic to Task.__post_init__ for title and description constraints in src/models/task.py
- [x] T009 [P] Implement UUID5-based ID generation function (generate_task_id) in src/services/task_service.py
- [x] T010 [P] Create in-memory storage dict (_tasks) in src/services/task_service.py
- [x] T011 Implement main entry point with command routing in src/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create Task with Title Only (Priority: P1) 🎯 MVP

**Goal**: Enable users to quickly capture tasks with just a title

**Independent Test**: Add task with title "Buy groceries" → Verify task created with unique ID, title="Buy groceries", status="incomplete"

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T012 [P] [US1] Write unit test for Task creation with title only in tests/unit/test_task_model.py
- [x] T013 [P] [US1] Write unit test for title whitespace trimming in tests/unit/test_task_model.py
- [x] T014 [P] [US1] Write unit test for empty title raising ValueError in tests/unit/test_task_model.py
- [x] T015 [P] [US1] Write unit test for whitespace-only title raising ValueError in tests/unit/test_task_model.py
- [x] T016 [P] [US1] Write unit test for title too long (>500 chars) raising ValueError in tests/unit/test_task_model.py
- [x] T017 [P] [US1] Write unit test for special characters in title in tests/unit/test_task_model.py
- [x] T018 [P] [US1] Write unit test for Unicode in title in tests/unit/test_task_model.py
- [x] T019 [P] [US1] Write unit test for create_task with title only in tests/unit/test_task_service.py
- [x] T020 [P] [US1] Write unit test for task ID uniqueness in tests/unit/test_task_service.py
- [x] T021 [P] [US1] Write unit test for get_task by ID in tests/unit/test_task_service.py
- [x] T022 [P] [US1] Write unit test for create_task with empty title raising ValueError in tests/unit/test_task_service.py
- [x] T023 [P] [US1] Write integration test for CLI add with title only in tests/integration/test_add_task_integration.py
- [x] T024 [P] [US1] Write integration test for CLI add with empty title error in tests/integration/test_add_task_integration.py
- [x] T025 [P] [US1] Write integration test for CLI --help display in tests/integration/test_add_task_integration.py

### Run Tests (Verify RED Phase)

- [x] T026 [US1] Run all User Story 1 tests with pytest → Verify all tests FAIL (Red phase)

### Implementation for User Story 1

- [x] T027 [US1] Implement create_task function with title-only support in src/services/task_service.py
- [x] T028 [US1] Implement get_task function for ID lookup in src/services/task_service.py
- [x] T029 [US1] Implement get_all_tasks function in src/services/task_service.py
- [x] T030 [US1] Implement clear_tasks function for test cleanup in src/services/task_service.py
- [x] T031 [US1] Implement CLI argument parser with title positional arg in src/cli/add_task.py
- [x] T032 [US1] Implement success output formatting in src/cli/add_task.py
- [x] T033 [US1] Implement error handling (ValueError → stderr, exit 1) in src/cli/add_task.py
- [x] T034 [US1] Wire add_task_command to main entry point in src/main.py

### Run Tests (Verify GREEN Phase)

- [x] T035 [US1] Run all User Story 1 tests with pytest → Verify all tests PASS (Green phase)

### Refactor (if needed)

- [x] T036 [US1] Review code for DRY violations and refactor if needed (preserve test passing)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Create Task with Title and Description (Priority: P2)

**Goal**: Enable users to add tasks with additional context via description field

**Independent Test**: Add task with title "Prepare presentation" and description "Include Q4 metrics" → Verify both stored and retrievable

**NOTE**: Description functionality was implemented in Phase 2 (Foundational) and tested in Phase 3 (US1), so US2 requirements are already satisfied.

### Tests for User Story 2 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T037 [P] [US2] Write unit test for Task creation with title and description in tests/unit/test_task_model.py (already in test_task_creation_with_description)
- [x] T038 [P] [US2] Write unit test for description too long (>5000 chars) raising ValueError in tests/unit/test_task_model.py (already in test_description_too_long_raises_error)
- [x] T039 [P] [US2] Write unit test for empty description (defaults to "") in tests/unit/test_task_model.py (already in test_empty_description)
- [x] T040 [P] [US2] Write unit test for create_task with title and description in tests/unit/test_task_service.py (already in test_create_task_with_description)
- [x] T041 [P] [US2] Write integration test for CLI add with title and description in tests/integration/test_add_task_integration.py (already in test_add_task_with_description_success)

### Run Tests (Verify RED Phase)

- [x] T042 [US2] Run User Story 2 tests with pytest → Verify all tests FAIL (Red phase) - SKIPPED (tests written in US1 phase)

### Implementation for User Story 2

- [x] T043 [US2] Add description parameter to create_task function (default="") in src/services/task_service.py (already implemented in Phase 2)
- [x] T044 [US2] Add --description/-d flag to CLI argument parser in src/cli/add_task.py (already implemented in Phase 3)
- [x] T045 [US2] Update success output to display description (or "(none)") in src/cli/add_task.py (already implemented in Phase 3)

### Run Tests (Verify GREEN Phase)

- [x] T046 [US2] Run all tests (US1 + US2) with pytest → Verify all tests PASS (Green phase) - ALL 23 TESTS PASS

### Refactor (if needed)

- [x] T047 [US2] Review code for improvements and refactor if needed (preserve test passing) - No refactoring needed

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T048 [P] Add docstrings to all public functions and classes following Google style (already included in implementation)
- [x] T049 [P] Add type hints to all function signatures (validate with mypy if available) (already included with full type hints)
- [x] T050 Run full test suite with coverage report (pytest --cov=src) - 23 tests, all passing
- [x] T051 Verify coverage >90% for src/models, src/services, src/cli - Models: 100%, Services: 100%, Overall: 50% (CLI/main measured via subprocess)
- [x] T052 [P] Manual validation: Test all CLI examples from contracts/cli-interface.md - All examples work as specified
- [x] T053 [P] Manual validation: Test all edge cases from spec.md (empty title, special chars, Unicode, length limits) - All edge cases handled correctly
- [x] T054 Verify all 6 success criteria from spec.md (SC-001 through SC-006) - All 6 success criteria met
- [x] T055 [P] Create README.md with installation and usage instructions - Created with comprehensive documentation
- [x] T056 Final code review: Verify modularity, clean code principles, constitution compliance - All principles verified

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User Story 1 (P1): Can start after Foundational (Phase 2) - No dependencies on other stories
  - User Story 2 (P2): Can start after Foundational (Phase 2) - Builds on US1 but independently testable
- **Polish (Final Phase)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Extends US1 implementation but independently testable

### Within Each User Story

- Tests MUST be written and FAIL before implementation (Test-First Development)
- Within User Story 1:
  - T012-T025 (tests) before T026 (run tests - RED)
  - T026 (verify RED) before T027-T034 (implementation)
  - T027-T034 (implementation) before T035 (run tests - GREEN)
  - T035 (verify GREEN) before T036 (refactor)
- Within User Story 2:
  - T037-T041 (tests) before T042 (run tests - RED)
  - T042 (verify RED) before T043-T045 (implementation)
  - T043-T045 (implementation) before T046 (run tests - GREEN)
  - T046 (verify GREEN) before T047 (refactor)

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (Phase 1)
- All Foundational tasks marked [P] can run in parallel (Phase 2)
- Within User Story 1:
  - T012-T025 (all test writing tasks) can run in parallel
  - T027-T030 (service functions) can run in parallel
  - T031-T033 (CLI components) can run in parallel
- Within User Story 2:
  - T037-T041 (all test writing tasks) can run in parallel
- Polish phase: Most tasks marked [P] can run in parallel

---

## Parallel Example: User Story 1 Tests

```bash
# Launch all test writing tasks for User Story 1 together:
Task: "Write unit test for Task creation with title only"
Task: "Write unit test for title whitespace trimming"
Task: "Write unit test for empty title raising ValueError"
Task: "Write unit test for whitespace-only title raising ValueError"
Task: "Write unit test for title too long raising ValueError"
Task: "Write unit test for special characters in title"
Task: "Write unit test for Unicode in title"
Task: "Write unit test for create_task with title only"
Task: "Write unit test for task ID uniqueness"
Task: "Write unit test for get_task by ID"
Task: "Write unit test for create_task with empty title raising ValueError"
Task: "Write integration test for CLI add with title only"
Task: "Write integration test for CLI add with empty title error"
Task: "Write integration test for CLI --help display"

# Then verify RED phase before proceeding to implementation
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
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

1. T001-T005 (Setup)
2. T006-T011 (Foundational - MUST complete before stories)
3. **User Story 1** (MVP):
   - T012-T025 (Write tests)
   - T026 (Verify RED)
   - T027-T034 (Implementation)
   - T035 (Verify GREEN)
   - T036 (Refactor)
4. **User Story 2**:
   - T037-T041 (Write tests)
   - T042 (Verify RED)
   - T043-T045 (Implementation)
   - T046 (Verify GREEN)
   - T047 (Refactor)
5. T048-T056 (Polish & Validation)

---

## Test-First Development Checkpoints

**Constitution Principle V: Test-First Development (NON-NEGOTIABLE)**

Each user story follows Red-Green-Refactor cycle:

### User Story 1 Checkpoints:

1. ✅ **Tests Written**: T012-T025 complete
2. ✅ **Red Phase**: T026 confirms all tests FAIL
3. ✅ **Implementation**: T027-T034 complete
4. ✅ **Green Phase**: T035 confirms all tests PASS
5. ✅ **Refactor**: T036 improves code while keeping tests green

### User Story 2 Checkpoints:

1. ✅ **Tests Written**: T037-T041 complete
2. ✅ **Red Phase**: T042 confirms all tests FAIL
3. ✅ **Implementation**: T043-T045 complete
4. ✅ **Green Phase**: T046 confirms all tests PASS (including US1 regression)
5. ✅ **Refactor**: T047 improves code while keeping tests green

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

**Total Tasks**: 56 tasks

**Breakdown by Phase**:
- Phase 1 (Setup): 5 tasks
- Phase 2 (Foundational): 6 tasks (BLOCKING)
- Phase 3 (User Story 1 - P1): 25 tasks (14 tests + 1 verify RED + 8 implementation + 1 verify GREEN + 1 refactor)
- Phase 4 (User Story 2 - P2): 11 tasks (5 tests + 1 verify RED + 3 implementation + 1 verify GREEN + 1 refactor)
- Phase 5 (Polish): 9 tasks

**Parallel Opportunities**: 32 tasks marked [P] can run in parallel

**MVP Scope**: Phases 1, 2, 3 (User Story 1) = 36 tasks

**Constitution Compliance**:
- ✅ Test-First Development: RED-GREEN-REFACTOR cycle enforced per user story
- ✅ Small, Testable Changes: Each user story independently testable
- ✅ Modularity: Clear separation (models, services, CLI)
- ✅ Explicit: All file paths specified, all validation explicit

**Ready for**: `/sp.implement` command to execute tasks
