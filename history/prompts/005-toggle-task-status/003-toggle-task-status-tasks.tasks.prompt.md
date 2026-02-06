---
id: 003
title: Toggle Task Status Tasks
stage: tasks
date: 2026-01-01
surface: agent
model: claude-sonnet-4-5
feature: 005-toggle-task-status
branch: 005-toggle-task-status
user: umzaid
command: /sp.tasks
labels: ["tasks", "toggle-task-status", "task-decomposition", "tdd", "phase-i"]
links:
  spec: specs/005-toggle-task-status/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/005-toggle-task-status/tasks.md (created - 53 tasks with TDD workflow)
tests:
  - Task format validation: All 53 tasks follow checklist format (checkbox, ID, labels, file paths)
  - Organization validation: Tasks grouped by user story (US1, US2, US3)
  - TDD validation: RED-GREEN-REFACTOR checkpoints present for all stories
---

## Prompt

/sp.tasks

Execute task decomposition for Toggle Task Status feature (005-toggle-task-status) following Test-First Development workflow.

## Response snapshot

Successfully generated comprehensive task decomposition for Toggle Task Status feature with 53 tasks organized by user story following strict Test-First Development (TDD) workflow:

**Task Organization - By User Story**:
- **Phase 1: Setup** - 0 tasks (infrastructure already exists)
- **Phase 2: Foundational** - 0 tasks (Task model and service pattern already exist)
- **Phase 3: User Story 1 (P1 - MVP)** - Mark Task as Complete - 16 tasks
  - 🔴 RED Phase: 9 tasks (4 unit tests + 4 integration tests + 1 checkpoint)
  - 🟢 GREEN Phase: 5 tasks (1 service function + 1 CLI module + 1 main router update + 2 checkpoints)
  - 🔵 REFACTOR Phase: 2 tasks (1 code review + 1 checkpoint)
- **Phase 4: User Story 2 (P2)** - Mark Task as Incomplete - 16 tasks
  - 🔴 RED Phase: 9 tasks (4 unit tests + 4 integration tests + 1 checkpoint)
  - 🟢 GREEN Phase: 5 tasks (1 service function + 1 CLI module + 1 main router update + 2 checkpoints)
  - 🔵 REFACTOR Phase: 2 tasks (1 code review + 1 checkpoint)
- **Phase 5: User Story 3 (P3)** - Toggle Task Status - 15 tasks
  - 🔴 RED Phase: 8 tasks (3 unit tests + 4 integration tests + 1 checkpoint)
  - 🟢 GREEN Phase: 5 tasks (1 service function + 1 CLI module + 1 main router update + 2 checkpoints)
  - 🔵 REFACTOR Phase: 2 tasks (1 code review + 1 checkpoint)
- **Phase 6: Polish** - 6 tasks (3 manual testing + 3 validation)

**Test-First Development (TDD) Workflow**:
Each user story follows strict RED-GREEN-REFACTOR cycle:
1. **🔴 RED Phase**: Write tests FIRST, verify they FAIL (no implementation exists)
   - All unit tests written in parallel (marked [P])
   - All integration tests written in parallel (marked [P])
   - RED Checkpoint: Verify all tests FAIL with ImportError/AttributeError
2. **🟢 GREEN Phase**: Implement minimal code to pass tests
   - Service layer implementation (mark_complete, mark_incomplete, toggle_status)
   - GREEN Checkpoint (Service): Verify unit tests PASS
   - CLI layer implementation (complete_task.py, incomplete_task.py, toggle_task.py)
   - Main router updates (add command routing)
   - GREEN Checkpoint (Full): Verify all tests PASS, no regressions
3. **🔵 REFACTOR Phase**: Code quality review
   - Code review per checklist (DRY, naming, docstrings, type hints, error messages)
   - REFACTOR Checkpoint: Verify no regressions (all tests still PASS)

**Task Format Compliance**:
All 53 tasks follow strict checklist format:
- `- [ ]` checkbox (markdown format)
- Task ID (T001-T053 sequential)
- `[P]` marker for parallelizable tasks (27 tasks marked [P])
- `[US1]`, `[US2]`, `[US3]` story labels (47 tasks have story labels)
- Clear description with exact file path

**Parallel Opportunities Identified**:
- **Within User Story 1 RED Phase**: 8 tests (T001-T008) can run in parallel
- **Within User Story 1 GREEN Phase**: CLI + main router (T012-T013) can run in parallel after service layer
- **Within User Story 2 RED Phase**: 8 tests (T017-T024) can run in parallel
- **Within User Story 2 GREEN Phase**: CLI + main router (T028-T029) can run in parallel after service layer
- **Within User Story 3 RED Phase**: 7 tests (T033-T039) can run in parallel
- **Within User Story 3 GREEN Phase**: CLI + main router (T043-T044) can run in parallel after service layer
- **Across User Stories**: All 3 user stories can proceed in parallel with different developers
- **Polish Phase**: All 3 manual testing tasks (T048-T050) can run in parallel

**Dependencies & Execution Order**:
- **Phase 1-2**: ✅ Complete (infrastructure exists)
- **Phase 3-5 (User Stories)**: Can start immediately, no blocking prerequisites
  - User stories are INDEPENDENT (no cross-story dependencies)
  - Can proceed in parallel (parallel team strategy)
  - Or sequentially by priority (MVP-first strategy: P1 → P2 → P3)
- **Phase 6 (Polish)**: Depends on all desired user stories being complete

**Implementation Strategies Documented**:
1. **MVP First (User Story 1 Only)**: 16 tasks → Deploy complete command (minimum viable product)
2. **Incremental Delivery**: P1 → Deploy → P2 → Deploy → P3 → Deploy (3 incremental releases)
3. **Parallel Team**: 3 developers work on US1/US2/US3 simultaneously after foundation ready

**Independent Test Criteria**:
- **User Story 1**: Create incomplete task → mark complete → verify status changes from incomplete to complete
- **User Story 2**: Create complete task → mark incomplete → verify status changes from complete to incomplete
- **User Story 3**: Create task (any status) → toggle → verify switches to opposite state

**File Changes per Task**:
- **Service layer**: src/services/task_service.py (3 functions: mark_complete, mark_incomplete, toggle_status)
- **CLI layer**: 3 new files (src/cli/complete_task.py, src/cli/incomplete_task.py, src/cli/toggle_task.py)
- **Main router**: src/main.py (3 elif blocks + help text updates)
- **Unit tests**: tests/unit/test_task_service.py (11 new tests)
- **Integration tests**: 3 new files (tests/integration/test_complete_task_integration.py, test_incomplete_task_integration.py, test_toggle_task_integration.py with 12 tests total)

**Checkpoints Defined**:
- 7 TDD checkpoints across all user stories (RED, GREEN Service, GREEN Full, REFACTOR for each story)
- 3 validation checkpoints in Polish phase (manual testing, coverage report, success criteria validation)

## Outcome

- ✅ Impact: Toggle Task Status task decomposition complete with 53 tasks organized by user story following strict Test-First Development workflow. All tasks follow checklist format (checkbox, ID, [P] marker, [Story] label, file path). Three user stories are independently implementable and testable with no cross-story dependencies.
- 🧪 Tests: 23 test tasks specified following RED-GREEN-REFACTOR cycle (8 tests for US1, 8 tests for US2, 7 tests for US3). All tests written BEFORE implementation with RED checkpoints to verify tests FAIL. GREEN checkpoints verify tests PASS. REFACTOR checkpoints verify no regressions.
- 📁 Files: Created specs/005-toggle-task-status/tasks.md (444 lines). Task breakdown: 0 setup + 0 foundational + 16 US1 + 16 US2 + 15 US3 + 6 polish = 53 tasks total. File changes: 6 new files (3 CLI + 3 integration tests), 3 modified files (task_service.py, test_task_service.py, main.py).
- 🔁 Next prompts: `/sp.implement` to execute Test-First Development workflow for all user stories, `/sp.analyze` to validate cross-artifact consistency after implementation.
- 🧠 Reflection: Task decomposition organized by user story enables independent implementation and incremental delivery. Each user story (P1: mark complete, P2: mark incomplete, P3: toggle) can be implemented, tested, and deployed independently following MVP-first approach. 27 tasks marked [P] for parallel execution within phases. TDD workflow with RED-GREEN-REFACTOR checkpoints ensures tests written BEFORE code (Constitution Principle V - NON-NEGOTIABLE). No setup or foundational tasks needed - feature reuses existing infrastructure from Add/Update/Delete features. Total 53 tasks is higher than Delete Task (20 tasks) due to three independent commands, but task structure follows same TDD pattern. Independent test criteria defined for each user story to enable standalone validation.

## Evaluation notes (flywheel)

- Failure modes observed: None. Task decomposition generated without issues. All tasks follow strict checklist format.
- Graders run and results (PASS/FAIL): Format validation - PASS (all 53 tasks have checkbox, ID, file path). Organization validation - PASS (tasks grouped by user story US1/US2/US3). TDD validation - PASS (RED-GREEN-REFACTOR checkpoints present for all stories).
- Prompt variant (if applicable): Standard /sp.tasks workflow with emphasis on Test-First Development (Constitution Principle V) and user story independence
- Next experiment (smallest change to try): None needed - task decomposition complete and validated. Ready for implementation phase (/sp.implement).
