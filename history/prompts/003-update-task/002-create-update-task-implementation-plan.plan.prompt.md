---
id: 002
title: Create Update Task Implementation Plan
stage: plan
date: 2025-12-31
surface: agent
model: claude-sonnet-4-5-20250929
feature: 003-update-task
branch: 003-update-task
user: umzaid
command: /sp.plan
labels: ["planning", "architecture", "update-task", "phase-i", "sdd-ri"]
links:
  spec: specs/003-update-task/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-update-task/plan.md (created - 518 lines)
  - specs/003-update-task/research.md (created - 134 lines)
  - specs/003-update-task/data-model.md (created - 261 lines)
  - specs/003-update-task/contracts/cli-interface.md (created - 472 lines)
  - specs/003-update-task/quickstart.md (created - 366 lines)
tests:
  - Constitution Check validation (PASS - all 8 principles)
---

## Prompt

/sp.plan

Execute the implementation planning workflow for Update Task feature (003-update-task) based on approved specification.

**Context**: Feature specification approved (specs/003-update-task/spec.md), ready for architectural design and implementation planning.

**Requirements**: Follow Spec-Driven Development methodology - generate research.md (Phase 0), data-model.md + contracts + quickstart.md (Phase 1), fill plan.md template with technical details, validate Constitution compliance.

## Response snapshot

**Implementation plan created successfully for Update Task feature (003-update-task).**

### Execution Summary

**Setup**: Ran `.specify/scripts/powershell/setup-plan.ps1 -Json` → Plan template copied to specs/003-update-task/plan.md

**Phase 0: Research** ✅ COMPLETE
- **Artifact**: `research.md` (134 lines)
- **4 Key Technical Decisions** documented:
  1. Update Task Service Function - Add `update_task(task_id, title=None, description=None)` to service layer
  2. CLI Argument Parsing - Use argparse with optional `--title` and `--description` flags
  3. Error Handling Strategy - Mirror Add Task pattern (exceptions → user messages → exit codes)
  4. Success Confirmation Output - Display updated task details in same format as Add Task
- **No unknowns remaining** - all technical context constrained by Phase I requirements + existing architecture
- **Technology stack confirmed** - No new dependencies (stdlib + existing codebase)

**Phase 1: Design & Contracts** ✅ COMPLETE
- **Artifacts**: 4 files created (data-model.md, contracts/cli-interface.md, quickstart.md, plan.md)

**Data Model (data-model.md - 261 lines)**:
- Task entity documented (existing, no changes required)
- Field mutability matrix: 2 mutable (title, description), 3 immutable (id, created, status)
- Validation rules reuse Task.__post_init__ (no duplication)
- State transitions defined (update preserves status)

**CLI Interface Contract (contracts/cli-interface.md - 472 lines)**:
- Command signature: `python -m src.main update <TASK_ID> [--title TITLE] [--description DESCRIPTION]`
- 8 error scenarios with exact error messages
- Exit codes: 0 (success), 1 (app error), 2 (usage error)
- Unicode support: Python 3.13+ UTF-8 native
- Help text format with examples

**Quickstart Implementation Guide (quickstart.md - 366 lines)**:
- 8-step RED-GREEN-REFACTOR workflow
- Code examples for service layer, CLI layer, main router
- 10 unit tests + 6 integration tests specified
- Manual validation checklist
- Success criteria verification (9 items from spec.md)

**Implementation Plan (plan.md - 518 lines)**:
- Summary: Partial update feature using Python optional parameters, reuses existing architecture
- Technical context: Python 3.13+, argparse, pytest, in-memory storage, CLI-only
- Constitution Check: ✅ ALL 8 PRINCIPLES PASS
- Architecture details: Service layer (update_task function), CLI layer (update_task.py), main router update
- Testing strategy: 10 unit tests + 6 integration tests, 100% service layer coverage goal
- File changes: 2 new files, 3 modified files, ~295 LOC total
- Dependencies: Add Task (required), View Task List (recommended), no new external dependencies
- Risk analysis: All risks mitigated through existing patterns

### Key Architectural Decisions

1. **Reuse existing architecture** (no new patterns introduced):
   - Service layer: Add one function to existing `task_service.py`
   - CLI layer: Create new file following `add_task.py` pattern
   - Main routing: Add elif block following existing pattern
   - Testing: Follow Add Task and View Task List test patterns

2. **Partial update implementation** using Python optional parameters:
   - `update_task(task_id, title=None, description=None)`
   - None = unchanged field
   - Enables title-only, description-only, or both updates

3. **Immutability enforcement** via Task dataclass recreation:
   - Create new Task instance with updated fields + preserved immutable fields
   - Triggers existing validation automatically
   - No validation logic duplication

4. **In-process testing pattern** (Phase I constraint adaptation):
   - In-memory storage doesn't persist between subprocess calls
   - Solution: Test service layer directly for data verification
   - Subprocess tests only for CLI-specific behavior (help text)

5. **Error handling consistency**:
   - Service layer: Raise domain exceptions (KeyError, ValueError)
   - CLI layer: Catch exceptions → user-friendly messages → exit codes
   - 8 error scenarios with exact messages specified in contract

### Constitution Compliance Validation

**All 8 Constitution principles verified** ✅

- ✅ **I. Specifications as Single Source of Truth**: spec.md approved, no ambiguity
- ✅ **II. AI-Generated Code Only**: Implementation via `/sp.implement` command
- ✅ **III. Reusable Intelligence**: Reuses Task model, service pattern, CLI pattern
- ✅ **IV. Mandatory Five-Step Workflow**: Currently at step 2/5 (Planning)
- ✅ **V. Test-First Development**: RED-GREEN-REFACTOR cycle in quickstart.md
- ✅ **VI. Modularity and Clean Code**: Service/CLI/Task separation maintained
- ✅ **VII. Explicit Over Implicit**: All edge cases, validation, errors explicit
- ✅ **VIII. Small, Testable Changes**: Minimal diff (1 function + 1 CLI file + routing)

**No complexity violations detected** - No complexity tracking table needed.

### Files Created (5)

1. **plan.md** (518 lines) - Complete implementation plan with architecture, testing, risks
2. **research.md** (134 lines) - Technical decisions with rationale and alternatives
3. **data-model.md** (261 lines) - Task entity documentation with mutability matrix
4. **contracts/cli-interface.md** (472 lines) - CLI contract with error messages and examples
5. **quickstart.md** (366 lines) - Step-by-step implementation guide with code examples

**Total documentation**: ~1,751 lines across 5 planning artifacts

### Implementation Scope

**File Changes Summary**:
- **New files**: 2 (src/cli/update_task.py ~60 lines, tests/integration/test_update_task_integration.py ~80 lines)
- **Modified files**: 3 (src/services/task_service.py +35 lines, src/main.py +10 lines, tests/unit/test_task_service.py +120 lines)
- **Total LOC**: ~295 lines of new/modified code

**Test Coverage**:
- **Unit tests**: 10 tests for update_task() function (service layer)
- **Integration tests**: 6 tests for CLI command
- **Coverage goal**: 100% for service layer, >90% overall

**Dependencies**:
- **Internal**: Add Task (required), View Task List (recommended)
- **External**: None (all stdlib + existing project dependencies)

### Technical Highlights

**Minimal Complexity**:
- No new data structures (reuses Task model)
- No new dependencies (stdlib only)
- No new validation logic (reuses Task.__post_init__)
- No new testing patterns (follows Add Task/View Task List)

**Architecture Consistency**:
- Service layer: Business logic, domain exceptions, no I/O
- CLI layer: Presentation, argparse, error messages, sys.exit
- Main router: Command routing, lazy imports
- Testing: Unit (service) + Integration (CLI)

**Risk Mitigation**:
- In-memory testing: Use in-process pattern (established)
- Unicode handling: Python 3.13+ native UTF-8 (no action)
- Immutability: Explicit tests for id/created/status preservation
- Validation: Reuse Task validation (no duplication)

## Outcome

- ✅ Impact: Implementation plan complete for Update Task feature. Provides comprehensive architectural design, technical decisions, testing strategy, and implementation guide. Ready for task decomposition (/sp.tasks) and implementation (/sp.implement).
- 🧪 Tests: Constitution Check - 8/8 principles PASS. No violations. All technical decisions documented with rationale and alternatives.
- 📁 Files: 5 planning artifacts created (plan.md: 518 lines, research.md: 134 lines, data-model.md: 261 lines, contracts/cli-interface.md: 472 lines, quickstart.md: 366 lines). Total: ~1,751 lines of documentation.
- 🔁 Next prompts: `/sp.tasks` to generate task decomposition with RED-GREEN-REFACTOR workflow.
- 🧠 Reflection: Planning phase leveraged existing architecture patterns (Add Task, View Task List) to minimize complexity. No new dependencies, no new data structures, no new validation logic. Partial update pattern (Python optional parameters) enables clean API. Constitution compliance verified across all 8 principles. In-process testing pattern addresses Phase I in-memory constraint. Implementation scope: ~295 LOC across 5 files (2 new, 3 modified).

## Evaluation notes (flywheel)

- Failure modes observed: None. All planning artifacts generated successfully. Constitution Check passed all 8 principles.
- Graders run and results (PASS/FAIL):
  - Phase 0 Research: PASS (4 decisions documented, no unknowns remaining)
  - Phase 1 Design: PASS (data-model, contracts, quickstart created)
  - Constitution Check: PASS (8/8 principles verified)
  - Architecture Consistency: PASS (follows existing patterns)
  - Risk Analysis: PASS (all risks mitigated)
- Prompt variant (if applicable): Standard /sp.plan workflow with Phase 0 research and Phase 1 design + contracts generation
- Next experiment (smallest change to try): For future features, consider whether research.md can be auto-generated from existing codebase analysis when all technical decisions follow established patterns (minimize manual research effort).
