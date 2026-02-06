---

description: "Task decomposition for Delete Task feature following Test-First Development"
---

# Tasks: Delete Task

**Input**: Design documents from `/specs/004-delete-task/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/cli-interface.md, quickstart.md

**Tests**: Test-First Development (TDD) is REQUIRED for this feature - all tests must be written BEFORE implementation code (RED-GREEN-REFACTOR cycle).

**Organization**: Tasks are organized by Test-First Development workflow phases to ensure proper RED-GREEN-REFACTOR cycle compliance.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1)
- Include exact file paths in descriptions

## Path Conventions

- Single Python CLI project
- `src/` for source code, `tests/` for tests at repository root
- Service layer: `src/services/task_service.py`
- CLI layer: `src/cli/delete_task.py`
- Main router: `src/main.py`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

**Status**: ✅ COMPLETE - All infrastructure already exists from Add Task, View Task List, and Update Task features

**Tasks**: None required - reusing existing project structure

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**Status**: ✅ COMPLETE - All foundational components exist from previous features:
- Task dataclass and TaskStatus enum (src/models/task.py)
- In-memory storage `_tasks: Dict[str, Task]` (src/services/task_service.py)
- Test infrastructure (pytest, fixtures)
- Main router (src/main.py)

**Tasks**: None required - Delete Task only adds new function to existing service layer

---

## Phase 3: User Story 1 - Delete Task by ID (Priority: P1) 🎯 MVP

**Goal**: Allow users to remove completed or obsolete tasks from their todo list using the task's unique identifier

**Independent Test**:
1. Create a task using Add Task feature
2. Run `python -m src.main delete <task_id>`
3. Verify success message displays deleted task details (ID, title, description, status)
4. Run View Task List to verify task no longer appears
5. Try deleting same task again to verify "Task not found" error

### 🔴 RED Phase: Write Failing Tests (MUST FAIL INITIALLY)

**⚠️ CRITICAL**: These tests MUST be written FIRST and MUST FAIL before any implementation code is written

- [x] T001 [P] [US1] Write unit test: `test_delete_task_returns_deleted_task()` in tests/unit/test_task_service.py
- [x] T002 [P] [US1] Write unit test: `test_delete_task_removes_from_storage()` in tests/unit/test_task_service.py
- [x] T003 [P] [US1] Write unit test: `test_delete_task_nonexistent_id_raises_keyerror()` in tests/unit/test_task_service.py
- [x] T004 [P] [US1] Write unit test: `test_delete_task_works_for_any_status()` in tests/unit/test_task_service.py
- [x] T005 [P] [US1] Write unit test: `test_delete_task_with_unicode()` in tests/unit/test_task_service.py
- [x] T006 [P] [US1] Write unit test: `test_delete_task_only_removes_specified_task()` in tests/unit/test_task_service.py
- [x] T007 [US1] Create integration test file: tests/integration/test_delete_task_integration.py with 4 tests (test_delete_task_in_process, test_delete_help, test_delete_nonexistent_task, test_delete_missing_task_id)
- [x] T008 [US1] Run all Delete Task tests to verify RED phase (all 10 tests MUST FAIL with ImportError or AttributeError)

**Checkpoint**: ❌ All 10 tests failing - Ready for GREEN phase

### 🟢 GREEN Phase: Implement Minimal Code (MAKE TESTS PASS)

**⚠️ CRITICAL**: Write ONLY enough code to make tests pass - no extra features, no premature optimization

- [x] T009 [US1] Implement `delete_task(task_id: str) -> Task` function in src/services/task_service.py (~20 lines per plan.md)
- [x] T010 [US1] Run unit tests for delete_task() to verify service layer implementation (6 tests should PASS)
- [x] T011 [US1] Create CLI command module: src/cli/delete_task.py with delete_task_command() function (~60 lines per plan.md)
- [x] T012 [US1] Update main router in src/main.py: Add "delete" to help text, add elif block for delete command routing, add "delete" to error message (~3 lines per plan.md)
- [x] T013 [US1] Run all Delete Task tests to verify GREEN phase (all 10 tests MUST PASS)

**Checkpoint**: ✅ All 10 tests passing - Ready for REFACTOR phase

### 🔵 REFACTOR Phase: Clean Up Code (KEEP TESTS GREEN)

**⚠️ CRITICAL**: Improve code quality while keeping tests green - NO new functionality

- [x] T014 [US1] Review code for DRY violations, naming consistency, documentation completeness, type hints, error message accuracy
- [x] T015 [US1] Refactor if needed: Extract constants, improve variable names, add missing docstrings, simplify complex expressions
- [x] T016 [US1] Run all tests (including Add Task, View Task List, Update Task) to verify no regressions introduced

**Checkpoint**: ✅ User Story 1 complete - All tests passing, code refactored, feature fully functional

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Validation, coverage verification, and final quality checks

- [x] T017 [P] Run manual testing checklist from quickstart.md (success scenarios, error scenarios, help and Unicode)
- [x] T018 [P] Run coverage report: `pytest --cov=src tests/` and verify ≥90% service layer, ≥80% CLI layer
- [x] T019 Validate all success criteria from spec.md (SC-001 through SC-007)
- [x] T020 Run full test suite one final time to ensure 100% pass rate

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: ✅ COMPLETE (no tasks)
- **Foundational (Phase 2)**: ✅ COMPLETE (no tasks)
- **User Story 1 (Phase 3)**: Can start immediately - follows Test-First Development workflow
  - RED Phase (T001-T008) → GREEN Phase (T009-T013) → REFACTOR Phase (T014-T016)
- **Polish (Phase 4)**: Depends on User Story 1 completion

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies - can start immediately (foundational components already exist)

### Within User Story 1 - Test-First Development Flow

**RED Phase (Write Failing Tests)**:
1. T001-T006 (unit tests) can run in parallel [P] - different test functions
2. T007 (integration tests) - create file with all 4 tests
3. T008 (verify tests fail) - BLOCKS GREEN phase (must confirm RED)

**GREEN Phase (Implement Code)**:
1. T009 (service function) - MUST complete before T011 (CLI depends on service)
2. T010 (verify unit tests) - validate service layer works
3. T011 (CLI command) - depends on T009 completion
4. T012 (main router) - depends on T011 completion (routing needs CLI command to exist)
5. T013 (verify all tests) - BLOCKS REFACTOR phase (must confirm GREEN)

**REFACTOR Phase (Clean Up)**:
1. T014 (code review) - identify refactor opportunities
2. T015 (refactor) - make improvements
3. T016 (verify no regressions) - validate refactor didn't break anything

### Parallel Opportunities

**RED Phase**:
```bash
# All unit tests can be written in parallel:
T001: "Write test_delete_task_returns_deleted_task()"
T002: "Write test_delete_task_removes_from_storage()"
T003: "Write test_delete_task_nonexistent_id_raises_keyerror()"
T004: "Write test_delete_task_works_for_any_status()"
T005: "Write test_delete_task_with_unicode()"
T006: "Write test_delete_task_only_removes_specified_task()"
```

**Polish Phase**:
```bash
# Manual testing and coverage can run in parallel:
T017: "Run manual testing checklist"
T018: "Run coverage report"
```

---

## Parallel Example: User Story 1 - RED Phase

```bash
# Launch all unit test writing tasks together:
Task T001: "Write test_delete_task_returns_deleted_task() in tests/unit/test_task_service.py"
Task T002: "Write test_delete_task_removes_from_storage() in tests/unit/test_task_service.py"
Task T003: "Write test_delete_task_nonexistent_id_raises_keyerror() in tests/unit/test_task_service.py"
Task T004: "Write test_delete_task_works_for_any_status() in tests/unit/test_task_service.py"
Task T005: "Write test_delete_task_with_unicode() in tests/unit/test_task_service.py"
Task T006: "Write test_delete_task_only_removes_specified_task() in tests/unit/test_task_service.py"
```

---

## Implementation Strategy

### Test-First Development Workflow (RED-GREEN-REFACTOR)

**Phase 3 - User Story 1 Implementation**:

1. **RED Phase** (T001-T008):
   - Write all 6 unit tests in parallel
   - Create integration test file with 4 tests
   - Run tests to verify all FAIL (ImportError or AttributeError)
   - **STOP**: Do not proceed to GREEN until RED is confirmed

2. **GREEN Phase** (T009-T013):
   - Implement service function (delete_task)
   - Verify unit tests pass
   - Implement CLI command (delete_task_command)
   - Update main router
   - Run all tests to verify all PASS
   - **STOP**: Do not proceed to REFACTOR until GREEN is confirmed

3. **REFACTOR Phase** (T014-T016):
   - Review code quality
   - Make improvements while keeping tests green
   - Verify no regressions
   - **COMPLETE**: User Story 1 delivered

4. **Polish Phase** (T017-T020):
   - Manual validation
   - Coverage verification
   - Success criteria validation
   - Final test run

### MVP Delivery (User Story 1 Only)

1. Complete Phase 3: User Story 1 (RED-GREEN-REFACTOR)
2. Complete Phase 4: Polish & Validation
3. **STOP and VALIDATE**: Test Delete Task independently
4. Verify all success criteria met (SC-001 through SC-007)
5. Feature complete and ready for deployment

### Incremental Testing Strategy

1. After RED phase → Verify all tests FAIL
2. After service implementation → Verify unit tests PASS
3. After CLI implementation → Verify all tests PASS
4. After refactor → Verify no regressions
5. After polish → Verify success criteria met

---

## Task Execution Checklist

Before marking any task complete, verify:

- [ ] Task follows Test-First Development workflow (tests before code)
- [ ] RED phase confirmed (tests fail initially)
- [ ] GREEN phase confirmed (tests pass after implementation)
- [ ] File paths match exactly as specified
- [ ] Code follows existing patterns (Add Task, Update Task)
- [ ] Error messages match spec.md exactly
- [ ] Exit codes match contracts/cli-interface.md (0/1/2)
- [ ] Unicode support verified
- [ ] No implementation details leak from planning docs
- [ ] All tests remain green after refactor

---

## Notes

- **Test-First Development is NON-NEGOTIABLE**: Constitution Principle V mandates RED-GREEN-REFACTOR cycle
- **[P] tasks**: Different files, no dependencies - can run in parallel
- **[US1] label**: All tasks map to User Story 1 (only story in Delete Task feature)
- **RED phase**: Tests MUST fail initially to validate they detect missing functionality
- **GREEN phase**: Implement ONLY enough code to make tests pass (no extra features)
- **REFACTOR phase**: Improve code quality while keeping tests green
- **Total tasks**: 20 tasks total (6 unit tests + 1 integration test file + 1 RED verify + 5 GREEN implementation + 3 REFACTOR + 4 Polish)
- **Estimated LOC**: ~183 lines (simplest CRUD operation per plan.md)
- **File changes**: 2 new files (src/cli/delete_task.py, tests/integration/test_delete_task_integration.py), 3 modified files (src/services/task_service.py, tests/unit/test_task_service.py, src/main.py)
- **Test count**: 10 tests (6 unit + 4 integration)
- **Parallel opportunities**: 8 tasks can run in parallel (6 unit test writes, 2 polish tasks)
- **Completion criteria**: All 10 tests passing, all 7 success criteria validated, coverage requirements met (≥90% service, ≥80% CLI)
