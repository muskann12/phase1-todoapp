---
id: 001
title: Toggle Task Status Specification
stage: spec
date: 2026-01-01
surface: agent
model: claude-sonnet-4-5
feature: 005-toggle-task-status
branch: 005-toggle-task-status
user: umzaid
command: /sp.specify
labels: ["specification", "toggle-task-status", "mark-complete", "mark-incomplete", "phase-i"]
links:
  spec: specs/005-toggle-task-status/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/005-toggle-task-status/spec.md (created specification)
  - specs/005-toggle-task-status/checklists/requirements.md (created validation checklist)
tests:
  - Validation Check: 16/16 items PASS
---

## Prompt

/sp.specify Mark Complete / Incomplete Task feature for an in-memory Python CLI Todo application

Context:
- Project: Evolution of Todo — Phase I
- Follow /sp.constitution strictly
- Spec-driven development only
- Manual coding is not allowed

Feature Intent:
Allow the user to toggle the completion status of an existing todo task using its unique task ID via a command-line interface.

Constraints:
- In-memory storage only
- Python 3.13+
- CLI-based interaction
- Task must be identified by a deterministic unique ID
- Toggle must switch between complete and incomplete states
- Changes persist only in-memory for the session

Reusable Intelligence (Reference Only):
- Task status toggle behavior follows reusable_intelligence/task_manager.skill.md
- Storage rules follow reusable_intelligence/in_memory_store.skill.md
- ID validation rules follow reusable_intelligence/id_policy.skill.md
- CLI input/output rules follow reusable_intelligence/cli_io.skill.md

## Response snapshot

Created comprehensive specification for Toggle Task Status feature following Spec-Driven Development workflow:

**Feature Name**: Toggle Task Status (005-toggle-task-status)
**Short Name Analysis**: "Mark Complete / Incomplete Task" → "toggle-task-status" (captures toggle/mark action and status concept)

**User Stories - Three Prioritized Increments**:
1. **User Story 1 (P1 - MVP)**: Mark Task as Complete
   - Core productivity: Users mark incomplete tasks as complete when finished
   - 3 acceptance scenarios (single task, multiple tasks, task with description)
   - Independent test: Create incomplete task → mark complete → verify status change

2. **User Story 2 (P2)**: Mark Task as Incomplete
   - Error correction: Users reverse completion for tasks needing rework
   - 2 acceptance scenarios (single task, multiple complete tasks)
   - Independent test: Create complete task → mark incomplete → verify status change

3. **User Story 3 (P3)**: Toggle Task Status
   - Convenience: Single command flips status regardless of current state
   - 2 acceptance scenarios (incomplete → complete, complete → incomplete)
   - Independent test: Create task → toggle → verify opposite state

**Functional Requirements**: 16 requirements (FR-001 to FR-016)
- Three commands: `complete`, `incomplete`, `toggle`
- Task identification via UUID5
- Idempotent operations (marking complete task as complete is valid)
- Error messages match existing pattern: "Error: Task not found with ID: [id]"
- Exit codes: 0 (success), 1 (not found), 2 (missing arg)
- Unicode support
- Help flags for all commands

**Edge Cases**: 8 identified with clear responses
- Task already in target state (idempotent - show success)
- Non-existent task ID (error message + exit code 1)
- Invalid ID format (lenient validation - same error as non-existent)
- Empty task list (same error)
- No task ID provided (argparse error + exit code 2)
- Unicode in task data (display correctly)
- Status change persistence (in-memory for session)

**Success Criteria**: 8 measurable outcomes (SC-001 to SC-008)
- Single command status change
- Immediate appearance in views
- Clear confirmation messages
- Error messages for all scenarios
- < 1 second operation time
- Unicode display
- Help documentation
- Toggle without knowing current state

**Key Entities**:
- Task: Object with status field (id, title, description, status, created)
- TaskStatus: Enum with INCOMPLETE and COMPLETE values

**Dependencies**:
- Add Task feature (001-add-task) - create tasks to change
- View Task List feature (002-view-task-list) - discover task IDs
- Task Model (src/models/task.py) - TaskStatus enum exists

**Validation Results**: ✅ 16/16 checklist items PASS
- Content Quality: 4/4 PASS (no implementation details, user-focused, non-technical)
- Requirement Completeness: 8/8 PASS (no clarifications needed, testable, measurable, scoped)
- Feature Readiness: 4/4 PASS (clear acceptance criteria, primary flows covered)

## Outcome

- ✅ Impact: Toggle Task Status feature specification complete. Three user stories provide independently testable MVP increments (P1: mark complete, P2: mark incomplete, P3: toggle). Feature scope is clear with 16 functional requirements and 8 success criteria.
- 🧪 Tests: Validation checklist passed 16/16 items. No clarifications needed - spec is complete and unambiguous.
- 📁 Files: Created specs/005-toggle-task-status/spec.md (161 lines), specs/005-toggle-task-status/checklists/requirements.md (validation checklist).
- 🔁 Next prompts: `/sp.plan` to generate implementation plan with technical approach, `/sp.clarify` if user needs clarification on requirements.
- 🧠 Reflection: Toggle Task Status extends existing Task model with status change operations. Three user stories allow incremental delivery (P1 MVP: mark complete only, P2 adds reversibility, P3 adds convenience). Idempotent operations design decision (marking complete task as complete is valid) simplifies error handling and improves user experience. All three commands share same error handling pattern for consistency with existing features (Add/Update/Delete).

## Evaluation notes (flywheel)

- Failure modes observed: None. Specification generated without issues.
- Graders run and results (PASS/FAIL): Requirements checklist - 16/16 PASS
- Prompt variant (if applicable): Standard /sp.specify workflow
- Next experiment (smallest change to try): None needed - specification complete and ready for planning phase.
