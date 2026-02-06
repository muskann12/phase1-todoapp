# CLI Interface Contract: View Task List

**Feature**: View Task List
**Date**: 2025-12-31
**Purpose**: Complete CLI specification for viewing all tasks

---

## Command Specification

### Command Name

```bash
python -m src.main view
```

**Alias**: None (Phase I has single "view" command)

**Category**: Read operation (does not modify data)

---

## Command Syntax

### Basic Usage

```bash
python -m src.main view
```

**Arguments**: None (displays all tasks)

**Options**: None (Phase I has no filtering or sorting options)

---

## Help Output

### Invocation

```bash
python -m src.main view --help
```

### Expected Output

```text
usage: todo view [-h]

View all tasks in your todo list

options:
  -h, --help  show this help message and exit
```

---

## Success Scenarios

### Scenario 1: View Tasks with Mixed Statuses

**Pre-condition**: 3 tasks exist (2 incomplete, 1 complete)

**Command**:
```bash
python -m src.main view
```

**Expected Output** (with User Story 2 summary):
```text
Total: 3 | Incomplete: 2 | Complete: 1

[ ] ID: 550e8400-e29b-41d4-a716-446655440000
    Title: Buy groceries
    Description: Milk, eggs, bread
    Status: Incomplete

[ ] ID: 6ba7b810-9dad-11d1-80b4-00c04fd430c9
    Title: Call dentist
    Description: (none)
    Status: Incomplete

[✓] ID: 7c9e6679-7425-40de-944b-e07fc1f90ae7
    Title: Finish report
    Description: Q4 metrics analysis
    Status: Complete
```

**Exit Code**: 0

**Notes**:
- Tasks displayed in ascending ID order (deterministic sort)
- Empty description shown as "(none)"
- Status icons: `[ ]` for incomplete, `[✓]` for complete
- Summary line at top with total, incomplete, and complete counts
- Blank line separates summary from task entries

---

### Scenario 2: View Empty Task List

**Pre-condition**: No tasks exist

**Command**:
```bash
python -m src.main view
```

**Expected Output**:
```text
No tasks found. Add your first task with: python -m src.main add "<title>"
```

**Exit Code**: 0

**Notes**:
- Helpful onboarding message guides user to Add Task command
- No summary line displayed (only for non-empty list)
- Not treated as error (exit code 0)

---

### Scenario 3: View Single Task

**Pre-condition**: 1 task exists (incomplete, with description)

**Command**:
```bash
python -m src.main view
```

**Expected Output**:
```text
Total: 1 | Incomplete: 1 | Complete: 0

[ ] ID: 550e8400-e29b-41d4-a716-446655440000
    Title: Review pull request #42
    Description: Check tests and code coverage
    Status: Incomplete
```

**Exit Code**: 0

---

### Scenario 4: View Tasks with Unicode Characters

**Pre-condition**: 2 tasks exist with Unicode in title/description

**Command**:
```bash
python -m src.main view
```

**Expected Output**:
```text
Total: 2 | Incomplete: 2 | Complete: 0

[ ] ID: 550e8400-e29b-41d4-a716-446655440000
    Title: Visit Café ☕
    Description: Try the new espresso
    Status: Incomplete

[ ] ID: 6ba7b810-9dad-11d1-80b4-00c04fd430c9
    Title: Read "Naïve Résumé" article
    Description: Focus on résumé tips 📄
    Status: Incomplete
```

**Exit Code**: 0

**Notes**:
- Unicode characters (emoji, accents) displayed correctly
- Requires UTF-8 terminal support (Spec Assumption #6)

---

### Scenario 5: View Large Task List (1000 tasks)

**Pre-condition**: 1000 tasks exist

**Command**:
```bash
python -m src.main view
```

**Expected Behavior**:
- All 1000 tasks displayed (no pagination in Phase I)
- Tasks displayed in ascending ID order
- Summary line shows: "Total: 1000 | Incomplete: X | Complete: Y"
- Command completes in under 2 seconds (SC-001)
- Output may scroll in terminal (user can use terminal scroll or pipe to `less`)

**Exit Code**: 0

**Notes**:
- No truncation or pagination (Phase I constraint)
- User can pipe output: `python -m src.main view | less`

---

## Error Scenarios

**View Task List has NO error scenarios** (read-only, no user input)

Possible system-level errors (not feature-specific):
- Python not installed: OS error before command runs
- Module import failure: Python error before command runs
- Out of memory: System-level error (extremely unlikely with in-memory tasks)

**All error scenarios are out of scope for View Task List feature**

---

## Exit Codes

| Code | Scenario | Description |
|------|----------|-------------|
| 0 | Success (any case) | Tasks displayed successfully (including empty list) |

**Note**: View is read-only with no user input, so no error exit codes needed.

---

## Output Format Specification

### Summary Line (User Story 2)

**Format**:
```text
Total: {total_count} | Incomplete: {incomplete_count} | Complete: {complete_count}
```

**Display Rule**:
- Show ONLY if task count > 0
- Omit if task count = 0 (show empty-state message instead)
- Followed by blank line before task entries

**Example**:
```text
Total: 10 | Incomplete: 7 | Complete: 3

```

---

### Task Entry Format (User Story 1)

**Format** (multi-line per task):
```text
{status_icon} ID: {task_id}
    Title: {task_title}
    Description: {task_description_or_none}
    Status: {status_text}
```

**Field Specifications**:
- `{status_icon}`: `[ ]` for INCOMPLETE, `[✓]` for COMPLETE
- `{task_id}`: Full UUID5 string (e.g., "550e8400-e29b-41d4-a716-446655440000")
- `{task_title}`: Exact title as stored (preserves Unicode, special chars, whitespace)
- `{task_description_or_none}`: Description if non-empty, otherwise "(none)"
- `{status_text}`: "Incomplete" or "Complete" (capitalized)

**Indentation**:
- Status icon at column 0
- ID, Title, Description, Status indented 4 spaces
- Blank line separates task entries (optional for visual clarity)

**Example**:
```text
[ ] ID: 550e8400-e29b-41d4-a716-446655440000
    Title: Buy groceries
    Description: Milk, eggs, bread
    Status: Incomplete
```

---

### Empty-State Message

**Format**:
```text
No tasks found. Add your first task with: python -m src.main add "<title>"
```

**Display Rule**:
- Show ONLY if task count = 0
- Omit summary line and task entries
- Provides onboarding guidance

---

## Implementation Requirements

### Service Layer Contract

**Function**: `get_all_tasks()`

**Signature**:
```python
def get_all_tasks() -> list[Task]:
    """Retrieve all tasks sorted by ID in ascending order."""
```

**Behavior**:
- Returns list of Task objects sorted by `task.id` (ascending)
- Returns empty list if no tasks exist
- MUST NOT modify `_tasks` dict (read-only guarantee)

**Example**:
```python
from src.services.task_service import get_all_tasks

tasks = get_all_tasks()  # Returns sorted list
```

---

### CLI Layer Contract

**Module**: `src/cli/view_tasks.py`

**Function**: `view_tasks_command(args: list[str] | None = None)`

**Responsibilities**:
1. Parse arguments (none expected, but support `--help`)
2. Call `get_all_tasks()` from service layer
3. Check if list is empty:
   - If empty: Display empty-state message, exit 0
   - If not empty: Display summary + task entries, exit 0
4. Format output according to specification above

**Pseudo-code**:
```python
def view_tasks_command(args: list[str] = None):
    # Parse args (handle --help)
    parser = argparse.ArgumentParser(description='View all tasks', prog='todo view')
    parser.parse_args(args)

    # Get tasks
    tasks = get_all_tasks()

    # Empty state
    if not tasks:
        print('No tasks found. Add your first task with: python -m src.main add "<title>"')
        sys.exit(0)

    # Display summary (User Story 2)
    total = len(tasks)
    incomplete = sum(1 for t in tasks if t.status == TaskStatus.INCOMPLETE)
    complete = total - incomplete
    print(f"Total: {total} | Incomplete: {incomplete} | Complete: {complete}")
    print()  # Blank line

    # Display tasks (User Story 1)
    for task in tasks:
        icon = "[✓]" if task.status == TaskStatus.COMPLETE else "[ ]"
        desc = task.description if task.description else "(none)"
        print(f"{icon} ID: {task.id}")
        print(f"    Title: {task.title}")
        print(f"    Description: {desc}")
        print(f"    Status: {task.status.value.capitalize()}")
        print()  # Blank line between tasks

    sys.exit(0)
```

---

### Main Entry Contract

**Module**: `src/main.py`

**Update Required**: Add "view" command routing

**Code Addition**:
```python
elif command == 'view':
    from src.cli.view_tasks import view_tasks_command
    view_tasks_command(sys.argv[2:])
```

**Updated Help Output** (when no command given):
```text
Usage: python -m src.main <command> [args]
Commands: add, view
```

---

## Testing Contract

### Integration Tests Required

1. **test_view_empty_list**: Verify empty-state message
2. **test_view_single_task**: Verify single task display with summary
3. **test_view_multiple_tasks**: Verify sorting, summary, all fields displayed
4. **test_view_mixed_statuses**: Verify status icons ([ ] and [✓])
5. **test_view_unicode_characters**: Verify Unicode display (emoji, accents)
6. **test_view_empty_description**: Verify "(none)" for empty descriptions
7. **test_view_help**: Verify --help output
8. **test_view_read_only**: Verify task count unchanged before/after view

**Test Execution**:
```bash
pytest tests/integration/test_view_tasks_integration.py -v
```

---

## Performance Requirements

**From Success Criteria**:
- SC-001: View completes in under 2 seconds (even for 1000+ tasks)
- SC-002: Deterministic sort order (ascending by ID) 100% of the time

**Measurement**:
```python
import time

start = time.time()
view_tasks_command()
elapsed = time.time() - start

assert elapsed < 2.0  # Under 2 seconds
```

---

## Accessibility Considerations

**Visual Indicators**:
- Status icons ([ ] and [✓]) provide quick visual scan for sighted users
- Status text ("Incomplete" / "Complete") ensures screen reader compatibility

**Terminal Compatibility**:
- Plain text output (no ANSI color codes in Phase I)
- UTF-8 encoding for Unicode support
- Multi-line format works with all terminal widths (wrapping allowed)

---

## Summary

**Command**: `python -m src.main view`

**Purpose**: Display all tasks in ascending ID order with summary counts

**User Stories Covered**:
- ✅ US1 (P1): View all tasks with ID, title, description, status
- ✅ US2 (P2): View summary counts (total, incomplete, complete)

**Success Criteria Validated**:
- ✅ SC-001: Completes in under 2 seconds
- ✅ SC-002: Deterministic sort order (ascending ID)
- ✅ SC-003: Empty-state message 100% of the time
- ✅ SC-004: Unicode displayed correctly
- ✅ SC-005: Accurate summary counts 100% of the time
- ✅ SC-006: Read-only (no data mutation)

**Exit Code**: Always 0 (success, including empty list)

**No Error Cases**: Read-only operation with no user input
