# CLI Interface Contracts: Toggle Task Status

**Feature**: 005-toggle-task-status
**Date**: 2026-01-01
**Phase**: 1 (Design)

## Overview

This document defines the CLI interface contracts for the three status change commands: `complete`, `incomplete`, and `toggle`. Each command follows the established CLI pattern from existing features (Add Task, Update Task, Delete Task).

---

## Command 1: Mark Task as Complete

### Command Signature

```bash
python src/main.py complete <task_id>
```

### Parameters

**Positional Arguments**:
- `task_id` (required): The unique identifier of the task to mark as complete

**Optional Arguments**:
- `--help`, `-h`: Display help message

### Input Validation

**Required**: Task ID must be provided
**Format**: Any string (lenient validation - if not found, show error)

**argparse Configuration**:
```python
parser = argparse.ArgumentParser(
    description="Mark a task as complete",
    prog="complete"
)
parser.add_argument(
    "task_id",
    help="The ID of the task to mark as complete"
)
```

### Success Output

**Format**:
```
Task marked as complete! ID: <id>, Title: <title>, Description: <description>, Status: Complete
```

**Example**:
```
Task marked as complete! ID: abc-123, Title: Buy milk, Description: (none), Status: Complete
```

**Fields**:
- `ID`: Task UUID5 identifier
- `Title`: Task title
- `Description`: Task description or "(none)" if empty
- `Status`: Always "Complete" for this command

**Exit Code**: 0

### Error Output

#### Error 1: Task Not Found

**Condition**: Task ID does not exist in storage

**Output** (stderr):
```
Error: Task not found with ID: <task_id>
```

**Exit Code**: 1

**Example**:
```
Error: Task not found with ID: non-existent-id
```

#### Error 2: Missing Task ID

**Condition**: No task ID provided

**Output** (stderr):
```
usage: complete [-h] task_id
complete: error: the following arguments are required: task_id
```

**Exit Code**: 2

**Note**: This is handled automatically by argparse

### Help Output

**Command**:
```bash
python src/main.py complete --help
```

**Output**:
```
usage: complete [-h] task_id

Mark a task as complete

positional arguments:
  task_id     The ID of the task to mark as complete

options:
  -h, --help  show this help message and exit
```

### Idempotent Behavior

**Scenario**: Task is already COMPLETE

**Output** (stdout):
```
Task marked as complete! ID: <id>, Title: <title>, Description: <description>, Status: Complete
```

**Exit Code**: 0

**Note**: No error - displays success message confirming task is complete

### Examples

**Example 1: Mark incomplete task as complete**
```bash
$ python src/main.py complete abc-123
Task marked as complete! ID: abc-123, Title: Buy milk, Description: (none), Status: Complete
$ echo $?
0
```

**Example 2: Mark already complete task as complete (idempotent)**
```bash
$ python src/main.py complete abc-123
Task marked as complete! ID: abc-123, Title: Buy milk, Description: (none), Status: Complete
$ echo $?
0
```

**Example 3: Non-existent task ID**
```bash
$ python src/main.py complete non-existent-id
Error: Task not found with ID: non-existent-id
$ echo $?
1
```

**Example 4: Missing task ID**
```bash
$ python src/main.py complete
usage: complete [-h] task_id
complete: error: the following arguments are required: task_id
$ echo $?
2
```

**Example 5: Task with description**
```bash
$ python src/main.py complete xyz-789
Task marked as complete! ID: xyz-789, Title: Write report, Description: Q4 financial summary, Status: Complete
$ echo $?
0
```

---

## Command 2: Mark Task as Incomplete

### Command Signature

```bash
python src/main.py incomplete <task_id>
```

### Parameters

**Positional Arguments**:
- `task_id` (required): The unique identifier of the task to mark as incomplete

**Optional Arguments**:
- `--help`, `-h`: Display help message

### Input Validation

**Required**: Task ID must be provided
**Format**: Any string (lenient validation - if not found, show error)

**argparse Configuration**:
```python
parser = argparse.ArgumentParser(
    description="Mark a task as incomplete",
    prog="incomplete"
)
parser.add_argument(
    "task_id",
    help="The ID of the task to mark as incomplete"
)
```

### Success Output

**Format**:
```
Task marked as incomplete! ID: <id>, Title: <title>, Description: <description>, Status: Incomplete
```

**Example**:
```
Task marked as incomplete! ID: abc-123, Title: Review document, Description: (none), Status: Incomplete
```

**Fields**:
- `ID`: Task UUID5 identifier
- `Title`: Task title
- `Description`: Task description or "(none)" if empty
- `Status`: Always "Incomplete" for this command

**Exit Code**: 0

### Error Output

#### Error 1: Task Not Found

**Condition**: Task ID does not exist in storage

**Output** (stderr):
```
Error: Task not found with ID: <task_id>
```

**Exit Code**: 1

**Example**:
```
Error: Task not found with ID: non-existent-id
```

#### Error 2: Missing Task ID

**Condition**: No task ID provided

**Output** (stderr):
```
usage: incomplete [-h] task_id
incomplete: error: the following arguments are required: task_id
```

**Exit Code**: 2

**Note**: This is handled automatically by argparse

### Help Output

**Command**:
```bash
python src/main.py incomplete --help
```

**Output**:
```
usage: incomplete [-h] task_id

Mark a task as incomplete

positional arguments:
  task_id     The ID of the task to mark as incomplete

options:
  -h, --help  show this help message and exit
```

### Idempotent Behavior

**Scenario**: Task is already INCOMPLETE

**Output** (stdout):
```
Task marked as incomplete! ID: <id>, Title: <title>, Description: <description>, Status: Incomplete
```

**Exit Code**: 0

**Note**: No error - displays success message confirming task is incomplete

### Examples

**Example 1: Mark complete task as incomplete**
```bash
$ python src/main.py incomplete abc-123
Task marked as incomplete! ID: abc-123, Title: Review document, Description: (none), Status: Incomplete
$ echo $?
0
```

**Example 2: Mark already incomplete task as incomplete (idempotent)**
```bash
$ python src/main.py incomplete abc-123
Task marked as incomplete! ID: abc-123, Title: Review document, Description: (none), Status: Incomplete
$ echo $?
0
```

**Example 3: Non-existent task ID**
```bash
$ python src/main.py incomplete non-existent-id
Error: Task not found with ID: non-existent-id
$ echo $?
1
```

**Example 4: Missing task ID**
```bash
$ python src/main.py incomplete
usage: incomplete [-h] task_id
incomplete: error: the following arguments are required: task_id
$ echo $?
2
```

**Example 5: Task with description**
```bash
$ python src/main.py incomplete xyz-789
Task marked as incomplete! ID: xyz-789, Title: Complete project, Description: Final deliverables, Status: Incomplete
$ echo $?
0
```

---

## Command 3: Toggle Task Status

### Command Signature

```bash
python src/main.py toggle <task_id>
```

### Parameters

**Positional Arguments**:
- `task_id` (required): The unique identifier of the task to toggle

**Optional Arguments**:
- `--help`, `-h`: Display help message

### Input Validation

**Required**: Task ID must be provided
**Format**: Any string (lenient validation - if not found, show error)

**argparse Configuration**:
```python
parser = argparse.ArgumentParser(
    description="Toggle a task's completion status",
    prog="toggle"
)
parser.add_argument(
    "task_id",
    help="The ID of the task to toggle"
)
```

### Success Output

**Format**:
```
Task status toggled! ID: <id>, Title: <title>, Description: <description>, Status: <new_status>
```

**Example (incomplete → complete)**:
```
Task status toggled! ID: abc-123, Title: Buy milk, Description: (none), Status: Complete
```

**Example (complete → incomplete)**:
```
Task status toggled! ID: abc-123, Title: Buy milk, Description: (none), Status: Incomplete
```

**Fields**:
- `ID`: Task UUID5 identifier
- `Title`: Task title
- `Description`: Task description or "(none)" if empty
- `Status`: "Complete" or "Incomplete" (opposite of original status)

**Exit Code**: 0

### Error Output

#### Error 1: Task Not Found

**Condition**: Task ID does not exist in storage

**Output** (stderr):
```
Error: Task not found with ID: <task_id>
```

**Exit Code**: 1

**Example**:
```
Error: Task not found with ID: non-existent-id
```

#### Error 2: Missing Task ID

**Condition**: No task ID provided

**Output** (stderr):
```
usage: toggle [-h] task_id
toggle: error: the following arguments are required: task_id
```

**Exit Code**: 2

**Note**: This is handled automatically by argparse

### Help Output

**Command**:
```bash
python src/main.py toggle --help
```

**Output**:
```
usage: toggle [-h] task_id

Toggle a task's completion status

positional arguments:
  task_id     The ID of the task to toggle

options:
  -h, --help  show this help message and exit
```

### Toggle Behavior

**Rule**: Always flip to opposite status

**Incomplete → Complete**:
```
Task status toggled! ID: <id>, Title: <title>, Description: <description>, Status: Complete
```

**Complete → Incomplete**:
```
Task status toggled! ID: <id>, Title: <title>, Description: <description>, Status: Incomplete
```

### Examples

**Example 1: Toggle incomplete task to complete**
```bash
$ python src/main.py toggle abc-123
Task status toggled! ID: abc-123, Title: Buy milk, Description: (none), Status: Complete
$ echo $?
0
```

**Example 2: Toggle complete task to incomplete**
```bash
$ python src/main.py toggle abc-123
Task status toggled! ID: abc-123, Title: Buy milk, Description: (none), Status: Incomplete
$ echo $?
0
```

**Example 3: Toggle back to complete (repeated toggle)**
```bash
$ python src/main.py toggle abc-123
Task status toggled! ID: abc-123, Title: Buy milk, Description: (none), Status: Complete
$ echo $?
0
```

**Example 4: Non-existent task ID**
```bash
$ python src/main.py toggle non-existent-id
Error: Task not found with ID: non-existent-id
$ echo $?
1
```

**Example 5: Missing task ID**
```bash
$ python src/main.py toggle
usage: toggle [-h] task_id
toggle: error: the following arguments are required: task_id
$ echo $?
2
```

**Example 6: Task with description**
```bash
$ python src/main.py toggle xyz-789
Task status toggled! ID: xyz-789, Title: Write report, Description: Q4 financial summary, Status: Complete
$ echo $?
0
```

---

## Common Patterns

### Exit Codes

All three commands follow the same exit code convention:

| Exit Code | Meaning | Scenario |
|-----------|---------|----------|
| 0 | Success | Status changed successfully OR idempotent operation (desired state achieved) |
| 1 | Business error | Task ID not found |
| 2 | Validation error | Missing required argument (task_id) |

### Error Message Format

**Pattern**: `Error: <error_description>`

**Examples**:
- `Error: Task not found with ID: abc-123`

**Output Stream**: stderr (standard error)

### Success Message Format

**Pattern**: `Task <action>! ID: <id>, Title: <title>, Description: <description>, Status: <status>`

**Actions**:
- `marked as complete` (complete command)
- `marked as incomplete` (incomplete command)
- `status toggled` (toggle command)

**Description Field**: Shows "(none)" if task.description is empty string

**Status Field**: Capitalized ("Complete" or "Incomplete")

**Output Stream**: stdout (standard output)

### Unicode Handling

All three commands display Unicode characters natively (no special encoding):

```bash
$ python src/main.py complete xyz-789
Task marked as complete! ID: xyz-789, Title: 📝 Write résumé, Description: Update with new job, Status: Complete
```

---

## Integration with Main Router

### Main Router Updates (src/main.py)

**Help Text**:
```python
if len(sys.argv) == 1 or sys.argv[1] in ["--help", "-h"]:
    print("Usage: python src/main.py <command> [options]")
    print("Commands: add, view, update, delete, complete, incomplete, toggle")
    sys.exit(0)
```

**Command Routing**:
```python
elif command == "complete":
    from cli.complete_task import complete_task_command
    complete_task_command(sys.argv[2:])

elif command == "incomplete":
    from cli.incomplete_task import incomplete_task_command
    incomplete_task_command(sys.argv[2:])

elif command == "toggle":
    from cli.toggle_task import toggle_task_command
    toggle_task_command(sys.argv[2:])
```

**Error Message**:
```python
else:
    print(f"Unknown command: {command}", file=sys.stderr)
    print("Valid commands: add, view, update, delete, complete, incomplete, toggle", file=sys.stderr)
    sys.exit(1)
```

---

## Summary

- **Three commands**: `complete`, `incomplete`, `toggle`
- **Same argument structure**: Single positional `task_id` argument
- **Same exit codes**: 0 (success), 1 (not found), 2 (missing arg)
- **Same error format**: `Error: Task not found with ID: <id>`
- **Different success messages**: Indicate which action was performed
- **Idempotent operations**: Exit code 0 for all successful state assignments
- **Unicode support**: Native display (no special encoding)
- **Help text**: Standard argparse format for all three commands
