# Tasks: Toggle Task Status

**Input**: Design documents from `/specs/005-toggle-task-status/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/cli-interface.md, quickstart.md

**Tests**: Test-First Development (TDD) is REQUIRED per Constitution Principle V (NON-NEGOTIABLE). All tasks follow RED-GREEN-REFACTOR cycle.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verify existing infrastructure is ready for status change feature

**Status**: ✅ No setup needed - reusing existing src/, tests/, and Task model infrastructure from Add/Update/Delete features

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**Status**: ✅ No foundational tasks needed - Task model with TaskStatus enum already exists, service pattern established

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Mark Task as Complete (Priority: P1) 🎯 MVP

**Goal**: Allow users to mark an incomplete task as complete using its unique task ID via CLI

**Independent Test**: Create an incomplete task, mark it as complete using its task ID, verify task status changes from incomplete to complete and persists in storage

### 🔴 RED Phase: Write Tests FIRST

**Checkpoint**: Run tests and verify they FAIL (T001-T008)

- [x] T001 [P] [US1] Write unit test test_mark_complete_returns_completed_task() in tests/unit/test_task_service.py
- [x] T002 [P] [US1] Write unit test test_mark_complete_updates_storage() in tests/unit/test_task_service.py
- [x] T003 [P] [US1] Write unit test test_mark_complete_nonexistent_id_raises_keyerror() in tests/unit/test_task_service.py
- [x] T004 [P] [US1] Write unit test test_mark_complete_idempotent() in tests/unit/test_task_service.py
- [x] T005 [P] [US1] Write integration test test_complete_task_in_process() in tests/integration/test_complete_task_integration.py
- [x] T006 [P] [US1] Write integration test test_complete_help() in tests/integration/test_complete_task_integration.py
- [x] T007 [P] [US1] Write integration test test_complete_nonexistent_task() in tests/integration/test_complete_task_integration.py
- [x] T008 [P] [US1] Write integration test test_complete_missing_task_id() in tests/integration/test_complete_task_integration.py
- [x] T009 [US1] RED Checkpoint: Run pytest tests/unit/test_task_service.py::test_mark_complete* -v and pytest tests/integration/test_complete_task_integration.py -v to verify all 8 tests FAIL

### 🟢 GREEN Phase: Implement Minimal Code

**Checkpoint**: Run tests and verify they PASS (T010-T013)

- [x] T010 [US1] Implement mark_complete(task_id: str) -> Task function in src/services/task_service.py (~20 lines)
- [x] T011 [US1] GREEN Checkpoint (Service): Run pytest tests/unit/test_task_service.py::test_mark_complete* -v to verify 4 unit tests PASS
- [x] T012 [US1] Create complete_task_command(args: list[str]) in src/cli/complete_task.py (~55 lines)
- [x] T013 [P] [US1] Update main router in src/main.py: add "complete" to help text, add complete command elif block, add "complete" to error message (~3 lines)
- [x] T014 [US1] GREEN Checkpoint (Full): Run pytest tests/integration/test_complete_task_integration.py -v to verify 4 integration tests PASS and run pytest -v to verify no regressions

### 🔵 REFACTOR Phase: Code Quality

**Checkpoint**: Verify code quality and no regressions (T015-T016)

- [x] T015 [US1] Code review for User Story 1: Check DRY, naming, docstrings, type hints, error messages, success messages, exit codes per checklist in quickstart.md
- [x] T016 [US1] REFACTOR Checkpoint: Run pytest -v to verify all tests still PASS (including existing Add/View/Update/Delete features)

**✅ User Story 1 Complete**: Complete command is fully functional and independently testable

---

## Phase 4: User Story 2 - Mark Task as Incomplete (Priority: P2)

**Goal**: Allow users to mark a complete task as incomplete when it needs rework or was marked complete by mistake

**Independent Test**: Create a complete task, mark it as incomplete using its task ID, verify task status changes from complete to incomplete

### 🔴 RED Phase: Write Tests FIRST

**Checkpoint**: Run tests and verify they FAIL (T017-T024)

- [ ] T017 [P] [US2] Write unit test test_mark_incomplete_returns_incomplete_task() in tests/unit/test_task_service.py
- [ ] T018 [P] [US2] Write unit test test_mark_incomplete_updates_storage() in tests/unit/test_task_service.py
- [ ] T019 [P] [US2] Write unit test test_mark_incomplete_nonexistent_id_raises_keyerror() in tests/unit/test_task_service.py
- [ ] T020 [P] [US2] Write unit test test_mark_incomplete_idempotent() in tests/unit/test_task_service.py
- [ ] T021 [P] [US2] Write integration test test_incomplete_task_in_process() in tests/integration/test_incomplete_task_integration.py
- [ ] T022 [P] [US2] Write integration test test_incomplete_help() in tests/integration/test_incomplete_task_integration.py
- [ ] T023 [P] [US2] Write integration test test_incomplete_nonexistent_task() in tests/integration/test_incomplete_task_integration.py
- [ ] T024 [P] [US2] Write integration test test_incomplete_missing_task_id() in tests/integration/test_incomplete_task_integration.py
- [ ] T025 [US2] RED Checkpoint: Run pytest tests/unit/test_task_service.py::test_mark_incomplete* -v and pytest tests/integration/test_incomplete_task_integration.py -v to verify all 8 tests FAIL

### 🟢 GREEN Phase: Implement Minimal Code

**Checkpoint**: Run tests and verify they PASS (T026-T029)

- [ ] T026 [US2] Implement mark_incomplete(task_id: str) -> Task function in src/services/task_service.py (~20 lines)
- [ ] T027 [US2] GREEN Checkpoint (Service): Run pytest tests/unit/test_task_service.py::test_mark_incomplete* -v to verify 4 unit tests PASS
- [ ] T028 [US2] Create incomplete_task_command(args: list[str]) in src/cli/incomplete_task.py (~55 lines)
- [ ] T029 [P] [US2] Update main router in src/main.py: add "incomplete" to help text, add incomplete command elif block, add "incomplete" to error message (~3 lines)
- [ ] T030 [US2] GREEN Checkpoint (Full): Run pytest tests/integration/test_incomplete_task_integration.py -v to verify 4 integration tests PASS and run pytest -v to verify no regressions

### 🔵 REFACTOR Phase: Code Quality

**Checkpoint**: Verify code quality and no regressions (T031-T032)

- [ ] T031 [US2] Code review for User Story 2: Check for common patterns between mark_complete and mark_incomplete, extract helper if needed per DRY principle
- [ ] T032 [US2] REFACTOR Checkpoint: Run pytest -v to verify all tests still PASS (including existing features and User Story 1)

**✅ User Story 2 Complete**: Incomplete command is fully functional and independently testable

---

## Phase 5: User Story 3 - Toggle Task Status (Priority: P3)

**Goal**: Allow users to quickly toggle a task's status (complete ↔ incomplete) without needing to know its current state

**Independent Test**: Create a task (any status), toggle its status, verify it switches to the opposite state

### 🔴 RED Phase: Write Tests FIRST

**Checkpoint**: Run tests and verify they FAIL (T033-T039)

- [ ] T033 [P] [US3] Write unit test test_toggle_status_incomplete_to_complete() in tests/unit/test_task_service.py
- [ ] T034 [P] [US3] Write unit test test_toggle_status_complete_to_incomplete() in tests/unit/test_task_service.py
- [ ] T035 [P] [US3] Write unit test test_toggle_status_nonexistent_id_raises_keyerror() in tests/unit/test_task_service.py
- [ ] T036 [P] [US3] Write integration test test_toggle_task_in_process() in tests/integration/test_toggle_task_integration.py
- [ ] T037 [P] [US3] Write integration test test_toggle_help() in tests/integration/test_toggle_task_integration.py
- [ ] T038 [P] [US3] Write integration test test_toggle_nonexistent_task() in tests/integration/test_toggle_task_integration.py
- [ ] T039 [P] [US3] Write integration test test_toggle_missing_task_id() in tests/integration/test_toggle_task_integration.py
- [ ] T040 [US3] RED Checkpoint: Run pytest tests/unit/test_task_service.py::test_toggle_status* -v and pytest tests/integration/test_toggle_task_integration.py -v to verify all 7 tests FAIL

### 🟢 GREEN Phase: Implement Minimal Code

**Checkpoint**: Run tests and verify they PASS (T041-T044)

- [ ] T041 [US3] Implement toggle_status(task_id: str) -> Task function with flip logic in src/services/task_service.py (~25 lines)
- [ ] T042 [US3] GREEN Checkpoint (Service): Run pytest tests/unit/test_task_service.py::test_toggle_status* -v to verify 3 unit tests PASS
- [ ] T043 [US3] Create toggle_task_command(args: list[str]) in src/cli/toggle_task.py (~55 lines)
- [ ] T044 [P] [US3] Update main router in src/main.py: add "toggle" to help text, add toggle command elif block, add "toggle" to error message (~3 lines)
- [ ] T045 [US3] GREEN Checkpoint (Full): Run pytest tests/integration/test_toggle_task_integration.py -v to verify 4 integration tests PASS and run pytest -v to verify no regressions

### 🔵 REFACTOR Phase: Code Quality

**Checkpoint**: Verify code quality and no regressions (T046-T047)

- [ ] T046 [US3] Code review for User Story 3: Final review of all three commands (complete, incomplete, toggle), extract any common patterns if needed
- [ ] T047 [US3] REFACTOR Checkpoint: Run pytest -v to verify all tests still PASS (all 23 new tests + existing features)

**✅ User Story 3 Complete**: Toggle command is fully functional and independently testable

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final validation, coverage, and documentation

- [ ] T048 [P] Manual testing: Test complete command with success scenarios (with and without description), help text, non-existent ID error, Unicode characters
- [ ] T049 [P] Manual testing: Test incomplete command with success scenarios (with and without description), help text, non-existent ID error, Unicode characters
- [ ] T050 [P] Manual testing: Test toggle command with success scenarios (incomplete→complete, complete→incomplete), help text, non-existent ID error, Unicode characters
- [ ] T051 Run coverage report: pytest --cov=src --cov-report=term-missing and verify ≥90% service layer coverage, ≥80% CLI layer coverage
- [ ] T052 Success criteria validation: Verify all 8 success criteria from spec.md (SC-001 through SC-008) are met
- [ ] T053 Final test run: Run pytest -v and verify all 23 new tests + all existing tests PASS (100% pass rate, no regressions)

**✅ Feature Complete**: All three commands (complete, incomplete, toggle) are implemented, tested, and validated

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: ✅ No dependencies - infrastructure already exists
- **Foundational (Phase 2)**: ✅ No dependencies - Task model and service pattern already exist
- **User Stories (Phase 3-5)**: Can start immediately (no blocking prerequisites)
  - User stories can proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3) for MVP-first approach
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies - can start immediately (MVP)
- **User Story 2 (P2)**: No dependencies on US1 - can start in parallel or after US1 for sequential delivery
- **User Story 3 (P3)**: No dependencies on US1/US2 - can start in parallel or after US2 for sequential delivery

### Within Each User Story (TDD Cycle)

1. **RED Phase**: Write tests FIRST, verify they FAIL (no implementation exists)
2. **GREEN Phase**: Implement minimal code to pass tests
   - Service layer before CLI layer
   - Main router updates after CLI layer
   - Verify tests PASS after each step
3. **REFACTOR Phase**: Code quality review, extract common patterns, verify no regressions

### Parallel Opportunities

**Within User Story 1 (RED Phase)**:
- T001-T008: All 8 tests can be written in parallel (different test files/functions)

**Within User Story 1 (GREEN Phase)**:
- T012 (CLI) and T013 (main router) can run in parallel after T010-T011 complete

**Within User Story 2 (RED Phase)**:
- T017-T024: All 8 tests can be written in parallel (different test files/functions)

**Within User Story 2 (GREEN Phase)**:
- T028 (CLI) and T029 (main router) can run in parallel after T026-T027 complete

**Within User Story 3 (RED Phase)**:
- T033-T039: All 7 tests can be written in parallel (different test files/functions)

**Within User Story 3 (GREEN Phase)**:
- T043 (CLI) and T044 (main router) can run in parallel after T041-T042 complete

**Across User Stories (if team capacity allows)**:
- After Phase 2 complete, all three user stories can proceed in parallel by different developers
- User Story 1 (T001-T016): Developer A
- User Story 2 (T017-T032): Developer B
- User Story 3 (T033-T047): Developer C

**Polish Phase**:
- T048-T050: All manual testing can run in parallel

---

## Parallel Example: User Story 1 (RED Phase)

```bash
# Launch all unit tests for User Story 1 together:
Task: "Write unit test test_mark_complete_returns_completed_task() in tests/unit/test_task_service.py"
Task: "Write unit test test_mark_complete_updates_storage() in tests/unit/test_task_service.py"
Task: "Write unit test test_mark_complete_nonexistent_id_raises_keyerror() in tests/unit/test_task_service.py"
Task: "Write unit test test_mark_complete_idempotent() in tests/unit/test_task_service.py"

# Launch all integration tests for User Story 1 together:
Task: "Write integration test test_complete_task_in_process() in tests/integration/test_complete_task_integration.py"
Task: "Write integration test test_complete_help() in tests/integration/test_complete_task_integration.py"
Task: "Write integration test test_complete_nonexistent_task() in tests/integration/test_complete_task_integration.py"
Task: "Write integration test test_complete_missing_task_id() in tests/integration/test_complete_task_integration.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup ✅ (already done)
2. Complete Phase 2: Foundational ✅ (already done)
3. Complete Phase 3: User Story 1 (T001-T016)
   - RED: Write 8 tests, verify they FAIL
   - GREEN: Implement mark_complete() service + complete CLI command
   - REFACTOR: Code review, verify no regressions
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo complete command (MVP ready!)

### Incremental Delivery

1. Foundation ready ✅ (Setup + Foundational complete)
2. Add User Story 1 → Test independently → Deploy/Demo (MVP: complete command)
3. Add User Story 2 → Test independently → Deploy/Demo (adds incomplete command)
4. Add User Story 3 → Test independently → Deploy/Demo (adds toggle command)
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Foundation ready ✅ (Setup + Foundational already complete)
2. After foundation, assign in parallel:
   - Developer A: User Story 1 (complete command) - T001-T016
   - Developer B: User Story 2 (incomplete command) - T017-T032
   - Developer C: User Story 3 (toggle command) - T033-T047
3. Stories complete independently and integrate via main.py routing
4. Team converges for Phase 6: Polish

---

## Task Summary

**Total Tasks**: 53 tasks (20 per user story + 6 polish + 7 checkpoints)
- **Phase 1 (Setup)**: 0 tasks (infrastructure exists)
- **Phase 2 (Foundational)**: 0 tasks (Task model exists)
- **Phase 3 (User Story 1)**: 16 tasks (9 tests + 5 implementation + 2 checkpoints)
- **Phase 4 (User Story 2)**: 16 tasks (9 tests + 5 implementation + 2 checkpoints)
- **Phase 5 (User Story 3)**: 15 tasks (8 tests + 5 implementation + 2 checkpoints)
- **Phase 6 (Polish)**: 6 tasks (3 manual testing + 3 validation)

**Test Tasks**: 23 tests total
- User Story 1: 8 tests (4 unit + 4 integration)
- User Story 2: 8 tests (4 unit + 4 integration)
- User Story 3: 7 tests (3 unit + 4 integration)

**Parallel Opportunities**: 27 tasks marked [P] can run in parallel within their phase

**MVP Scope**: Phase 3 only (User Story 1: complete command) = 16 tasks

**Full Feature**: All phases = 53 tasks

---

## Notes

- [P] tasks = different files/functions, no dependencies, can run in parallel
- [Story] label maps task to specific user story (US1, US2, US3) for traceability
- Each user story is independently completable and testable (no cross-story dependencies)
- TDD cycle is MANDATORY (Constitution Principle V - NON-NEGOTIABLE)
- Verify tests FAIL before implementing (RED checkpoint)
- Verify tests PASS after implementing (GREEN checkpoint)
- Verify no regressions after refactoring (REFACTOR checkpoint)
- Commit after each checkpoint or logical group
- Stop at any user story checkpoint to validate and deploy incrementally
