---
id: 003
title: Generate View Task List Tasks
stage: tasks
date: 2025-12-31
surface: agent
model: claude-sonnet-4-5
feature: 002-view-task-list
branch: 002-view-task-list
user: umzaid
command: /sp.tasks
labels: ["tasks", "decomposition", "view-task-list", "test-first"]
links:
  spec: specs/002-view-task-list/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-view-task-list/tasks.md
tests:
  - 31 tasks generated (8 unit tests + 2 integration tests + implementation + validation)
  - RED-GREEN-REFACTOR cycle enforced per user story
---

## Prompt

```text
/sp.tasks
```

## Response snapshot

Successfully generated comprehensive task decomposition for "View Task List" feature with 31 tasks organized by user story following Test-First Development methodology:

**Task Organization**:

- **Phase 1 (Setup)**: 0 tasks - ✅ COMPLETE (reused from Add Task feature)
  - No additional setup needed (pytest, .gitignore, __init__.py already exist)

- **Phase 2 (Foundational - BLOCKING)**: 1 task
  - T001: Add `get_all_tasks()` function to `src/services/task_service.py`
  - Returns sorted list of all tasks by ID ascending
  - CRITICAL: Blocks all user story work until complete

- **Phase 3 (User Story 1 - P1 MVP)**: 13 tasks
  - **Tests (T002-T009)**: 8 test writing tasks (3 unit, 5 integration) - parallelizable
    - Unit tests: empty storage, sorted by ID, read-only guarantee
    - Integration tests: empty list, single task, multiple tasks, Unicode, --help
  - **RED Phase (T010)**: Verify all tests FAIL
  - **Implementation (T011-T012)**: 2 tasks
    - Create `src/cli/view_tasks.py` with `view_tasks_command()`
    - Add "view" command routing to `src/main.py`
  - **GREEN Phase (T013)**: Verify all tests PASS
  - **Refactor (T014)**: Review and improve code quality

- **Phase 4 (User Story 2 - P2)**: 6 tasks
  - **Tests (T015-T016)**: 2 integration tests - parallelizable
    - Test summary display with counts
    - Test empty list has no summary (only empty-state message)
  - **RED Phase (T017)**: Verify tests FAIL
  - **Implementation (T018)**: Add summary calculation and display to `view_tasks.py`
  - **GREEN Phase (T019)**: Verify all tests PASS (US1 + US2)
  - **Refactor (T020)**: Review and improve code quality

- **Phase 5 (Polish & Validation)**: 11 tasks
  - Docstring and type hint verification (T021-T022)
  - Coverage testing (T023-T024) - target >90%
  - Manual validation (T025-T029) - 5 scenarios
  - Success criteria verification (T030) - all 6 criteria
  - Final code review (T031) - constitution compliance

**Test-First Development (RED-GREEN-REFACTOR)**:
- User Story 1: T002-T009 (tests) → T010 (RED) → T011-T012 (implementation) → T013 (GREEN) → T014 (refactor)
- User Story 2: T015-T016 (tests) → T017 (RED) → T018 (implementation) → T019 (GREEN) → T020 (refactor)

**Independent Testing**:
- User Story 1: Create 3 tasks, run view, verify display (ID, title, description, status, sorted)
- User Story 2: Create 10 tasks (7 incomplete, 3 complete), verify summary "Total: 10 | Incomplete: 7 | Complete: 3"

**Parallel Opportunities** (18 tasks marked [P]):
- US1 tests: T002-T009 (8 tasks in parallel)
- US1 implementation: T011-T012 (2 tasks in parallel if team)
- US2 tests: T015-T016 (2 tasks in parallel)
- Polish: T021-T022, T025-T029 (8 tasks in parallel)

**MVP Scope**: 14 tasks (Phase 2 + Phase 3 User Story 1)
- Foundational: 1 task
- User Story 1: 13 tasks (tests → RED → implementation → GREEN → refactor)

**Dependencies**:
- Setup (Phase 1) → Foundational (Phase 2) → User Stories (Phase 3-4) → Polish (Phase 5)
- User Story 1 and User Story 2 both depend on Foundational but are independent of each other
- Each story has RED-GREEN-REFACTOR checkpoints

**Constitution Compliance**:
- ✅ Principle V (Test-First): Tests written before implementation, RED-GREEN-REFACTOR enforced
- ✅ Principle VIII (Small, Testable): Each user story independently testable
- ✅ Principle VI (Modularity): Clear separation - service, CLI, main routing
- ✅ All file paths explicit, all validation criteria specified

## Outcome

- ✅ Impact: Complete task decomposition for View Task List with 31 tasks across 5 phases; 2 user stories (P1 MVP + P2 enhancement); RED-GREEN-REFACTOR cycles enforced; 18 parallel opportunities identified
- 🧪 Tests: 10 test tasks total (8 for US1: 3 unit + 5 integration; 2 for US2: 2 integration); RED-GREEN checkpoints after each user story
- 📁 Files: 1 file created (tasks.md)
- 🔁 Next prompts: Run `/sp.implement` to execute tasks following Test-First Development; MVP deliverable after Phase 3 (User Story 1)
- 🧠 Reflection: Task organization by user story enables independent implementation and testing; RED-GREEN-REFACTOR cycle ensures tests validate functionality; MVP scope (14 tasks) delivers core value; User Story 2 extends US1 without breaking independence; parallel opportunities (18 tasks) maximize efficiency; constitution compliance perfect (test-first, modularity, explicit paths)

## Evaluation notes (flywheel)

- Failure modes observed: None - tasks organized by user story as required; all tasks follow checklist format (checkbox + ID + [P] + [Story] + description + file path); RED-GREEN-REFACTOR enforced
- Graders run and results (PASS/FAIL): PASS - All 31 tasks follow strict format; user stories independently testable; test-first enforced; file paths explicit; parallel opportunities identified; MVP scope clear
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): none
