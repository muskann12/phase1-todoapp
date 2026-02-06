---
id: 002
title: Toggle Task Status Planning
stage: plan
date: 2026-01-01
surface: agent
model: claude-sonnet-4-5
feature: 005-toggle-task-status
branch: 005-toggle-task-status
user: umzaid
command: /sp.plan
labels: ["planning", "toggle-task-status", "phase-0", "phase-1", "design", "phase-i"]
links:
  spec: specs/005-toggle-task-status/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/005-toggle-task-status/plan.md (created - 209 lines)
  - specs/005-toggle-task-status/research.md (created - Phase 0 technical decisions)
  - specs/005-toggle-task-status/data-model.md (created - Phase 1 data model)
  - specs/005-toggle-task-status/contracts/cli-interface.md (created - Phase 1 CLI contracts)
  - specs/005-toggle-task-status/quickstart.md (created - Phase 1 TDD workflow)
tests:
  - Constitution Check: 8/8 gates PASS
  - All planning artifacts validated
---

## Prompt

/sp.plan

Execute planning workflow for Toggle Task Status feature (005-toggle-task-status) following Spec-Driven Development process.

## Response snapshot

Successfully generated comprehensive planning documentation for Toggle Task Status feature following five phases (Setup, Phase 0 Research, Phase 1 Design, Constitution Re-Check, Report):

**Technical Context**:
- Language: Python 3.13+
- Dependencies: argparse (stdlib), pytest (testing)
- Storage: In-memory `Dict[str, Task]` (Phase I constraint)
- Testing: Test-First Development (RED-GREEN-REFACTOR cycle)
- Performance: Status change operation < 1 second (O(1) dict operations)

**Constitution Check**: ✅ ALL 8 GATES PASS
- I. Specifications as Single Source of Truth: PASS (spec complete, 16 FRs, 8 SCs)
- II. AI-Generated Code Only: PASS (implementation via /sp.implement)
- III. Reusable Intelligence Encouraged: PASS (reuses Task model, service pattern, CLI pattern)
- IV. Mandatory Five-Step Workflow: PASS (Step 2/5 - planning complete)
- V. Test-First Development: PASS (quickstart.md mandates RED-GREEN-REFACTOR cycle)
- VI. Modularity and Clean Code: PASS (service/CLI separation, 3 focused functions)
- VII. Explicit Over Implicit: PASS (all edge cases defined, idempotent behavior explicit)
- VIII. Small, Testable Changes: PASS (3 independently testable user stories)

**Phase 0: Research (research.md)** - 10 Technical Decisions:
1. Service Layer Function Design → **Three separate functions** (mark_complete, mark_incomplete, toggle_status)
2. Idempotent Operation Behavior → **Show success** (exit code 0, no error)
3. Status Change Implementation Method → **Create new Task instance** (immutable pattern from Update Task)
4. Toggle Status Logic → **Check current status, then flip** (simple conditional)
5. CLI Structure → **Three separate files** (complete_task.py, incomplete_task.py, toggle_task.py)
6. Success Message Format → **ID, Title, Description, Status** (matches spec acceptance scenarios)
7. Error Handling Pattern → **Raise KeyError, CLI translates** (consistent with Delete Task)
8. Exit Code Strategy for Idempotent Operations → **Exit code 0 always** (desired state achieved)
9. Unicode Character Handling → **Display natively** (trust Python 3.13+ UTF-8 mode)
10. Status Validation Strategy → **Trust storage, no extra validation** (Task dataclass validates on creation)

**Phase 1: Design Artifacts**:

1. **data-model.md**: Status transition model
   - Task entity (existing, no changes): id, title, description, status, created
   - TaskStatus enum (existing, no changes): INCOMPLETE, COMPLETE
   - Status transitions: INCOMPLETE↔COMPLETE with idempotent support
   - Storage mutation pattern: Replace-in-place (create new Task, update dict)
   - Validation: Task ID existence check only

2. **contracts/cli-interface.md**: CLI contracts for 3 commands
   - **complete** command: `python src/main.py complete <task_id>`
     - Success: "Task marked as complete! ID: ..., Title: ..., Description: ..., Status: Complete"
     - Error: "Error: Task not found with ID: <id>" (exit code 1)
     - Missing arg: argparse error (exit code 2)
   - **incomplete** command: `python src/main.py incomplete <task_id>`
     - Success: "Task marked as incomplete! ID: ..., Title: ..., Description: ..., Status: Incomplete"
     - Same error handling as complete
   - **toggle** command: `python src/main.py toggle <task_id>`
     - Success: "Task status toggled! ID: ..., Title: ..., Description: ..., Status: <new_status>"
     - Same error handling as complete/incomplete
   - All commands: Exit codes 0 (success), 1 (not found), 2 (missing arg)

3. **quickstart.md**: Test-First Development workflow
   - Total tests: 23 tests (11 unit + 12 integration)
   - Coverage target: ≥90% service layer, ≥80% CLI layer
   - RED-GREEN-REFACTOR cycle for each user story:
     - User Story 1 (P1 - MVP): Mark Complete (8 tests)
     - User Story 2 (P2): Mark Incomplete (8 tests)
     - User Story 3 (P3): Toggle Status (7 tests)
   - Checkpoints at each phase: Verify RED (tests fail), Verify GREEN (tests pass), Verify REFACTOR (no regressions)

**File Changes Summary**:
- **New files** (6 total): 3 CLI modules, 3 integration test files
- **Modified files** (3 total): task_service.py (+3 functions), test_task_service.py (+11 tests), main.py (+3 routes)
- **Total LOC estimate**: ~476 lines
  - Service layer: ~65 lines (3 functions × ~20 lines)
  - CLI layer: ~165 lines (3 files × ~55 lines)
  - Main routing: ~11 lines
  - Unit tests: ~110 lines
  - Integration tests: ~125 lines

**Implementation Strategy**:
- Test-First Development with three independent user stories
- Each user story is independently deliverable (follows P1→P2→P3 priority)
- Phase 1 (P1 - MVP): Mark Task as Complete (standalone delivery)
- Phase 2 (P2): Mark Task as Incomplete (adds reversibility)
- Phase 3 (P3): Toggle Task Status (adds convenience)

**Key Design Patterns**:
- Service layer: Immutable Task pattern (create new instance, replace in storage)
- CLI layer: Separate file per command (modularity)
- Error handling: KeyError at service → user message at CLI
- Idempotent operations: Always exit code 0 (desired state achieved)
- Message format: Consistent across all three commands (ID, Title, Description, Status)

## Outcome

- ✅ Impact: Toggle Task Status implementation plan complete with all Phase 0 and Phase 1 artifacts. All 10 technical decisions documented with rationale and alternatives. Constitution check passed all 8 gates. Feature scope is clear with 3 independently testable user stories (P1: mark complete, P2: mark incomplete, P3: toggle).
- 🧪 Tests: Planning complete - 23 tests specified (11 unit + 12 integration). Test-First Development workflow documented in quickstart.md with RED-GREEN-REFACTOR checkpoints. Coverage targets defined: ≥90% service layer, ≥80% CLI layer.
- 📁 Files: Created 5 planning artifacts (plan.md, research.md, data-model.md, contracts/cli-interface.md, quickstart.md). Total documentation: ~800 lines. File changes planned: 6 new files, 3 modified files, ~476 LOC.
- 🔁 Next prompts: `/sp.tasks` to generate task decomposition (tasks.md), `/sp.implement` to execute Test-First Development workflow, `/sp.analyze` after tasks.md creation to validate cross-artifact consistency.
- 🧠 Reflection: Toggle Task Status extends existing Task model with status change operations. Three separate service functions provide clear API (mark_complete, mark_incomplete, toggle_status) rather than unified function, following single-responsibility principle and matching CLI command structure. Idempotent operations design decision (always exit code 0 for desired state) simplifies scripting and follows HTTP PUT semantics. All three commands share same error handling pattern for consistency with existing features (Add/Update/Delete). Total LOC (~476) is higher than Delete Task (~183) but lower than Update Task (~295) - three commands add more code but follow same patterns. Planning phase required detailed analysis of 10 technical decisions to ensure consistency with existing codebase patterns.

## Evaluation notes (flywheel)

- Failure modes observed: None. Planning workflow executed without issues. All Constitution gates passed.
- Graders run and results (PASS/FAIL): Constitution Check - 8/8 gates PASS. All planning artifacts validated against template structure.
- Prompt variant (if applicable): Standard /sp.plan workflow with emphasis on Test-First Development (Constitution Principle V - NON-NEGOTIABLE)
- Next experiment (smallest change to try): None needed - planning complete and validated. Ready for task decomposition phase (/sp.tasks).
