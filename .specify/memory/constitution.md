# Evolution of Todo — Phase I Constitution

<!--
Sync Impact Report:
Version Change: Initial → 1.0.0
Modified Principles: N/A (initial creation)
Added Sections:
  - Core Principles (8 principles)
  - Phase I Constraints
  - Development Workflow
  - Governance
Removed Sections: N/A
Templates Requiring Updates:
  ✅ .specify/templates/spec-template.md - aligned with Test-First and Independent Testing principles
  ✅ .specify/templates/plan-template.md - aligned with Constitution Check requirement
  ✅ .specify/templates/tasks-template.md - aligned with Test-First and incremental delivery principles
Follow-up TODOs: None
-->

## Core Principles

### I. Specifications as Single Source of Truth

All development decisions, feature definitions, and system behavior MUST be explicitly documented in specifications before implementation. Specifications supersede all other artifacts including code, documentation, and conversation history.

**Rationale**: Ensures alignment between intent and implementation, prevents scope drift, and provides auditable decision trail.

### II. AI-Generated Code Only

Claude Code is the ONLY permitted code generator. Manual coding by humans is explicitly prohibited during implementation phases. Humans MAY only refine specifications, clarify requirements, and approve generated outputs.

**Rationale**: Enforces discipline in spec-first workflow, ensures consistency with Spec-Driven Development methodology, and prevents ad-hoc implementations that bypass the specification process.

### III. Reusable Intelligence Encouraged

Skills, subagents, agent workflows, and architectural blueprints MUST be reused when applicable. Reusable intelligence MAY be imported from Frontend Agent Systems, previous Todo implementations, or general-purpose Task Management skills. All imported intelligence MUST be referenced (not duplicated) and adapted only via project-specific constraints.

**Rationale**: Maximizes efficiency, leverages proven patterns, prevents reinventing solutions, and builds institutional knowledge.

### IV. Mandatory Five-Step Workflow

Every feature MUST follow this exact sequence without exception:
1. Write or reference a specification
2. Generate an implementation plan
3. Decompose into tasks
4. Implement via Claude Code
5. Validate against success criteria

Skipping steps is NOT permitted. Each step MUST be completed and approved before proceeding to the next.

**Rationale**: Ensures systematic development, prevents premature implementation, and maintains traceability from requirements through validation.

### V. Test-First Development (NON-NEGOTIABLE)

When tests are required by the specification:
- Tests MUST be written BEFORE implementation code
- Tests MUST fail initially (Red phase)
- Implementation proceeds only after test failure is confirmed (Green phase)
- Refactoring follows successful implementation (Refactor phase)

The Red-Green-Refactor cycle is strictly enforced.

**Rationale**: Validates that tests actually detect missing functionality, prevents false positives from poorly written tests, and ensures test-driven development discipline.

### VI. Modularity and Clean Code

All generated code MUST:
- Be modular with clear separation of concerns (data, logic, interface)
- Follow clean code principles (readable, self-documenting, maintainable)
- Use deterministic task IDs for reproducibility
- Separate data models from business logic from user interface

**Rationale**: Ensures code quality, maintainability, testability, and supports future evolution of the system.

### VII. Explicit Over Implicit

All specifications MUST be explicit and unambiguous:
- Behavior MUST be clearly defined
- Ambiguities MUST be resolved before implementation
- Assumptions MUST be documented
- Edge cases MUST be addressed

If requirements are unclear, clarification MUST be obtained before proceeding.

**Rationale**: Prevents misinterpretation, reduces rework, and ensures generated code matches intended behavior.

### VIII. Small, Testable Changes

All implementations MUST:
- Produce the smallest viable diff that satisfies requirements
- Be independently testable
- Reference existing code with precise file:line citations
- Propose new code in clearly marked, fenced blocks

Refactoring unrelated code is NOT permitted unless explicitly specified.

**Rationale**: Minimizes risk, simplifies review, isolates failures, and maintains focus on specified requirements.

## Phase I Constraints

These constraints apply exclusively to Phase I of the Evolution of Todo project and override any conflicting general practices:

**Storage**: In-memory ONLY. No file I/O, no database, no persistence across sessions.

**Interface**: Python command-line interface ONLY. No GUI, no web interface, no REST API.

**Runtime**: Python 3.13+ required. No backward compatibility with earlier Python versions.

**Scope**: Exactly five features MUST be implemented, no more, no fewer:
1. Add Task
2. Delete Task
3. Update Task
4. View Task List
5. Mark Task as Complete/Incomplete

Additional features beyond these five are explicitly NOT permitted in Phase I.

**Feature Specifications**: MAY be thin if reusable skills exist, BUT behavior MUST remain explicit and unambiguous.

## Development Workflow

### Workflow Stages

1. **Specification Phase**: Define feature requirements, user scenarios, acceptance criteria, and success metrics in `specs/<feature>/spec.md`

2. **Planning Phase**: Generate architectural design, technical approach, and implementation strategy in `specs/<feature>/plan.md`

3. **Task Decomposition Phase**: Break down implementation into discrete, testable tasks in `specs/<feature>/tasks.md`

4. **Implementation Phase**: Execute tasks via Claude Code, following Test-First discipline when tests are specified

5. **Validation Phase**: Verify all acceptance criteria met, all tests passing, all success metrics achieved

### Approval Gates

- Specification MUST be approved before planning begins
- Plan MUST be approved before task decomposition begins
- Tasks MUST be approved before implementation begins
- Implementation MUST pass validation before feature is considered complete

### Human-AI Collaboration

- **Humans**: Provide requirements, clarify ambiguities, approve specifications, approve plans, approve task lists, validate outcomes
- **AI (Claude Code)**: Generate specifications (from human input), generate plans, generate tasks, generate implementation code, execute tests, report results

## Governance

### Authority Hierarchy

1. This Constitution (highest authority)
2. Feature Specifications (in `specs/<feature>/spec.md`)
3. Implementation Plans (in `specs/<feature>/plan.md`)
4. Task Definitions (in `specs/<feature>/tasks.md`)
5. Generated Code (lowest authority, MUST conform to above)

If generated code deviates from specifications, the specification MUST be revised to either:
- Clarify the original intent and regenerate code, OR
- Accept the deviation and update the specification accordingly

### Amendment Process

Constitution amendments require:
1. Written proposal with rationale
2. Impact analysis on existing specifications and implementations
3. Migration plan for affected artifacts
4. Approval before adoption
5. Version increment following semantic versioning

### Versioning

Constitution follows semantic versioning (MAJOR.MINOR.PATCH):
- **MAJOR**: Backward-incompatible changes (e.g., removing a principle, changing workflow order)
- **MINOR**: Backward-compatible additions (e.g., new principle, expanded guidance)
- **PATCH**: Clarifications, typo fixes, non-semantic refinements

### Compliance

All pull requests and code reviews MUST verify:
- Workflow steps followed in order
- Code generated by Claude Code only
- Specifications exist and match implementation
- No manual code additions
- All constraints satisfied

Complexity MUST be justified in writing when it cannot be avoided.

### Runtime Development Guidance

For detailed development procedures, workflows, and command usage, refer to `CLAUDE.md` and `.claude/commands/*.md`.

**Version**: 1.0.0 | **Ratified**: 2025-12-31 | **Last Amended**: 2025-12-31
