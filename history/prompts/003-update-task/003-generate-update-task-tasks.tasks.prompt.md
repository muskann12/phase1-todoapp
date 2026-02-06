---
id: 003
title: Generate Update Task Tasks
stage: tasks
date: 2025-12-31
surface: agent
model: claude-sonnet-4-5-20250929
feature: 003-update-task
branch: 003-update-task
user: umzaid
command: /sp.tasks
labels: ["task-decomposition", "update-task", "test-first", "red-green-refactor", "phase-i"]
links:
  spec: specs/003-update-task/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-update-task/tasks.md (created - 492 lines)
tests:
  - Task format validation (PASS - all tasks follow checklist format)
  - User story organization validation (PASS - organized by P1, P2, P3)
  - Test-First Development validation (PASS - RED-GREEN-REFACTOR enforced)
---

## Prompt

/sp.tasks

Generate actionable, dependency-ordered tasks.md for Update Task feature (003-update-task) based on available design artifacts.

**Context**: Planning complete (spec.md, plan.md, research.md, data-model.md, contracts/cli-interface.md, quickstart.md available). Ready for task decomposition following Test-First Development methodology.

**Requirements**: Organize tasks by user story (P1, P2, P3), enforce RED-GREEN-REFACTOR cycle per story, ensure independent testability, generate dependency graph, identify parallel opportunities.

## Response snapshot

**Task decomposition created successfully for Update Task feature (003-update-task).**

### Execution Summary

**Prerequisites Check**: Ran `.specify/scripts/powershell/check-prerequisites.ps1 -Json`
- FEATURE_DIR: E:\Hackathon 2\Todo_phase_1\specs\003-update-task
- AVAILABLE_DOCS: research.md, data-model.md, contracts/, quickstart.md

**Design Documents Loaded**:
- ✅ spec.md (required) - 3 user stories with priorities
- ✅ plan.md (required) - Technical stack, file changes, testing strategy
- ✅ research.md (optional) - 4 technical decisions
- ✅ data-model.md (optional) - Task entity mutability matrix
- ✅ contracts/cli-interface.md (optional) - CLI interface specification

**User Stories Extracted from spec.md**:
1. **US1 (P1 - MVP)**: Update Task Title - Update title without changing description
2. **US2 (P2)**: Update Task Description - Update description without changing title
3. **US3 (P3)**: Update Both Title and Description - Atomic updates for both fields

**Technical Stack from plan.md**:
- Language: Python 3.13+
- Dependencies: argparse, pytest (stdlib + existing)
- Testing: pytest with coverage
- Structure: Single project (src/, tests/)
- File changes: 2 new files, 3 modified files (~295 LOC)

**Test-First Development Requirement**:
- Constitution Principle V (NON-NEGOTIABLE): Tests MUST be written before implementation
- RED-GREEN-REFACTOR cycle enforced per user story
- 10 unit tests + 6 integration tests specified in plan.md

### Task Generation Results

**Total Tasks**: 46 tasks

**Phase Breakdown**:
1. **Phase 1 (Setup)**: 0 tasks - ✅ COMPLETE (reused from Add Task, View Task List)
2. **Phase 2 (Foundational)**: 1 task - Add update_task() to service layer (BLOCKS all user stories)
3. **Phase 3 (User Story 1 - P1 MVP)**: 12 tasks
   - 7 test tasks (unit + integration)
   - 1 verify RED task
   - 2 implementation tasks (CLI + main routing)
   - 1 verify GREEN task
   - 1 refactor task
4. **Phase 4 (User Story 2 - P2)**: 9 tasks
   - 5 test tasks
   - 1 verify RED task
   - 1 implementation task (add --description flag)
   - 1 verify GREEN task
   - 1 refactor task
5. **Phase 5 (User Story 3 - P3)**: 10 tasks
   - 5 test tasks
   - 1 verify RED task
   - 2 implementation tasks (validation)
   - 1 verify GREEN task
   - 1 refactor task
6. **Phase 6 (Polish)**: 14 tasks - Documentation, coverage, manual validation, success criteria verification

**Parallel Opportunities**: 24 tasks marked [P] - Different files, no dependencies

**MVP Scope**: Phases 1 + 2 + 3 = 13 tasks (User Story 1 only)

### Task Organization by User Story

**User Story 1 (P1 - MVP)**: Update Task Title
- Independent Test: Create task "Buy mlk", update to "Buy milk", verify title changed
- Tasks: T002-T013 (12 tasks)
- Tests: 7 (unit: title update, preserve description, KeyError, empty title, title too long; integration: --title flag, --help)
- Implementation: Create update_task.py CLI, add update command routing
- Checkpoint: US1 fully functional and testable independently

**User Story 2 (P2)**: Update Task Description
- Independent Test: Create task with empty description, update to "Details", verify description changed
- Tasks: T014-T022 (9 tasks)
- Tests: 5 (unit: description update, preserve title, allow empty, description too long; integration: --description flag)
- Implementation: Add --description flag to CLI
- Checkpoint: US1 AND US2 both work independently

**User Story 3 (P3)**: Update Both
- Independent Test: Create task, update both fields, verify both changed
- Tasks: T023-T032 (10 tasks)
- Tests: 5 (unit: both updated, no updates error, preserve immutables; integration: both flags, Unicode)
- Implementation: Validate combined usage, "no updates" error
- Checkpoint: All user stories independently functional

### RED-GREEN-REFACTOR Cycle Enforcement

**User Story 1 Workflow**:
1. T002-T008: Write tests FIRST (7 tests in parallel)
2. T009: Run tests → Verify FAIL (RED phase)
3. T010-T011: Implement CLI + routing
4. T012: Run tests → Verify PASS (GREEN phase)
5. T013: Refactor if needed (preserve test passing)

**User Story 2 Workflow**:
1. T014-T018: Write tests FIRST (5 tests in parallel)
2. T019: Run tests → Verify FAIL (RED phase)
3. T020: Add --description flag
4. T021: Run tests → Verify PASS (GREEN phase, includes US1 regression)
5. T022: Refactor if needed

**User Story 3 Workflow**:
1. T023-T027: Write tests FIRST (5 tests in parallel)
2. T028: Run tests → Verify FAIL (RED phase)
3. T029-T030: Validate combined usage
4. T031: Run tests → Verify PASS (GREEN phase, includes US1+US2 regression)
5. T032: Refactor if needed

**Validation Rule**: If any GREEN phase fails, DO NOT proceed to next user story. Fix implementation until all tests pass.

### Dependencies & Execution Order

**Phase Dependencies**:
- Setup → Foundational → User Stories (P1, P2, P3 can start in parallel after Foundational) → Polish

**User Story Dependencies**:
- US1 (P1): Independent (no dependencies on other stories)
- US2 (P2): Independent (builds on US1 CLI but independently testable)
- US3 (P3): Independent (uses US1+US2 flags but independently testable)

**Within-Story Dependencies**:
- Tests → RED verification → Implementation → GREEN verification → Refactor (strict sequence)

**Parallel Opportunities**:
- All test-writing tasks within a story can run in parallel
- Implementation tasks can run in parallel if different developers
- Polish tasks (T033-T044) can run in parallel

### Task Format Validation

**All tasks follow strict checklist format** ✅:
- ✅ Checkbox: `- [ ]` (markdown checkbox)
- ✅ Task ID: Sequential (T001, T002, ..., T046)
- ✅ [P] marker: Present for parallelizable tasks (24 tasks)
- ✅ [Story] label: Present for user story tasks (US1, US2, US3)
- ✅ Description: Clear action with exact file path
- ✅ File paths: All tasks specify exact file locations

**Examples**:
- `- [ ] T001 [P] Add update_task() function to src/services/task_service.py ...`
- `- [ ] T002 [P] [US1] Write unit test for update_task() with title-only update in tests/unit/test_task_service.py`
- `- [ ] T010 [US1] Create src/cli/update_task.py with update_task_command() function ...`

### Implementation Strategy

**MVP First (Recommended)**:
1. Complete Foundational (T001)
2. Complete User Story 1 (T002-T013)
3. STOP and VALIDATE independently
4. Demo MVP if ready

**Incremental Delivery**:
- Each user story adds value without breaking previous stories
- Each story independently testable
- Each story can be validated in isolation

**Sequential Order** (if implementing alone):
1. T001 (Foundation)
2. T002-T013 (US1 - MVP)
3. T014-T022 (US2)
4. T023-T032 (US3)
5. T033-T046 (Polish)

### Constitution Compliance

**All 8 Constitution Principles Enforced**:
- ✅ **I. Specifications as Single Source of Truth**: All tasks derived from approved spec.md and plan.md
- ✅ **II. AI-Generated Code Only**: Tasks executable via `/sp.implement` command
- ✅ **III. Reusable Intelligence**: Reuses existing test patterns from Add Task and View Task List
- ✅ **IV. Mandatory Five-Step Workflow**: Currently at step 3/5 (Task Decomposition)
- ✅ **V. Test-First Development**: RED-GREEN-REFACTOR strictly enforced per user story
- ✅ **VI. Modularity and Clean Code**: Clear separation (service, CLI, main routing)
- ✅ **VII. Explicit Over Implicit**: All file paths specified, all validations explicit
- ✅ **VIII. Small, Testable Changes**: Each user story independently testable (~295 LOC total)

## Outcome

- ✅ Impact: Task decomposition complete for Update Task feature. 46 tasks organized by 3 user stories (P1, P2, P3) following Test-First Development. Each story independently testable with RED-GREEN-REFACTOR cycle enforced. Ready for implementation via `/sp.implement`.
- 🧪 Tests: 17 test tasks across 3 user stories (7 for US1, 5 for US2, 5 for US3). All tests written BEFORE implementation per Constitution Principle V. RED phase verification ensures tests fail before implementation.
- 📁 Files: 1 file created (specs/003-update-task/tasks.md - 492 lines). Total tasks: 46 (1 foundational + 31 user stories + 14 polish). Parallel opportunities: 24 tasks marked [P].
- 🔁 Next prompts: `/sp.implement` to execute tasks following RED-GREEN-REFACTOR workflow.
- 🧠 Reflection: Task organization by user story enables independent implementation and testing. MVP scope (US1 only) = 13 tasks. Incremental delivery allows validating each story before proceeding. Constitution Principle V (Test-First Development) strictly enforced with RED-GREEN verification checkpoints. All 46 tasks follow checklist format with exact file paths.

## Evaluation notes (flywheel)

- Failure modes observed: None. All tasks generated successfully following template structure and Constitution requirements.
- Graders run and results (PASS/FAIL):
  - User story extraction: PASS (3 stories with priorities P1, P2, P3)
  - Task format validation: PASS (all 46 tasks follow checklist format)
  - Test-First Development enforcement: PASS (RED-GREEN-REFACTOR per story)
  - Independent testability: PASS (each story has independent test criteria)
  - Parallel opportunities: PASS (24 tasks marked [P])
  - Constitution compliance: PASS (all 8 principles enforced)
- Prompt variant (if applicable): Standard /sp.tasks workflow with Test-First Development enforcement
- Next experiment (smallest change to try): For future features, consider auto-generating test task descriptions from contract specifications to reduce manual test planning effort.
