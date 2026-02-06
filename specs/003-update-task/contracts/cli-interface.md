# CLI Interface Contract: Update Task

**Feature**: 003-update-task
**Date**: 2025-12-31
**Interface Type**: Command-line interface (CLI)
**Tool**: argparse (Python stdlib)

## Overview

This document defines the command-line interface contract for the Update Task feature. It specifies argument structure, validation rules, output formats, and exit codes.

---

## Command Signature

```bash
python -m src.main update <TASK_ID> [--title TITLE] [--description DESCRIPTION]
```

### Positional Arguments

| Argument | Type | Required | Description | Validation |
|----------|------|----------|-------------|------------|
| `task_id` | string | ✅ Yes | Unique task identifier (UUID5 format) | Must exist in storage (KeyError if not found) |

### Optional Arguments (Flags)

| Flag | Type | Required | Default | Description | Validation |
|------|------|----------|---------|-------------|------------|
| `--title` | string | ❌ No | None (unchanged) | New task title | 1-500 chars (after trim), non-empty |
| `--description` | string | ❌ No | None (unchanged) | New task description | 0-2000 chars, can be empty string |
| `--help` or `-h` | flag | ❌ No | N/A | Display usage help | Auto-handled by argparse |

### Constraints

1. **At least one update required**: User MUST provide `--title` OR `--description` OR both
   - If neither provided → error: "No updates provided. Use --title and/or --description"

2. **Partial updates supported**:
   - `--title` only → updates title, preserves description
   - `--description` only → updates description, preserves title
   - Both flags → updates both fields

3. **Empty description allowed**:
   - `--description ""` → clears description to empty string (valid)
   - `--title ""` → error: "Title cannot be empty" (invalid)

---

## Input Examples

### Valid Invocations

```bash
# Update title only
python -m src.main update abc-123-uuid --title "Buy organic milk"

# Update description only
python -m src.main update xyz-789-uuid --description "Get from Trader Joe's"

# Update both
python -m src.main update def-456-uuid --title "Call Sarah" --description "Discuss Q1 roadmap"

# Clear description (empty string)
python -m src.main update abc-123-uuid --description ""

# Show help
python -m src.main update --help
python -m src.main update -h
```

### Invalid Invocations

```bash
# Missing task ID
python -m src.main update --title "New Title"
→ Error: positional argument required: task_id

# No updates provided
python -m src.main update abc-123-uuid
→ Error: No updates provided. Use --title and/or --description

# Empty title
python -m src.main update abc-123-uuid --title ""
→ Error: Title cannot be empty

# Title too long (> 500 chars)
python -m src.main update abc-123-uuid --title "a" * 501
→ Error: Title cannot exceed 500 characters

# Description too long (> 2000 chars)
python -m src.main update abc-123-uuid --description "a" * 2001
→ Error: Description cannot exceed 2000 characters

# Non-existent task ID
python -m src.main update nonexistent-id --title "New Title"
→ Error: Task not found with ID: nonexistent-id
```

---

## Output Formats

### Success Output

**Exit Code**: 0

**Format**:
```
Task updated successfully!
ID: <task_id>
Title: <title>
Description: <description or "(none)">
Status: <status>
```

**Example 1 - Title Updated**:
```bash
$ python -m src.main update abc-123-uuid --title "Buy organic milk"
Task updated successfully!
ID: abc-123-uuid-here
Title: Buy organic milk
Description: (none)
Status: Incomplete
```

**Example 2 - Description Updated**:
```bash
$ python -m src.main update xyz-789-uuid --description "Get from Trader Joe's"
Task updated successfully!
ID: xyz-789-uuid-here
Title: Buy milk
Description: Get from Trader Joe's
Status: Incomplete
```

**Example 3 - Both Updated**:
```bash
$ python -m src.main update def-456-uuid --title "Call Sarah" --description "Discuss Q1 roadmap"
Task updated successfully!
ID: def-456-uuid-here
Title: Call Sarah
Description: Discuss Q1 roadmap
Status: Complete
```

**Example 4 - Description Cleared**:
```bash
$ python -m src.main update abc-123-uuid --description ""
Task updated successfully!
ID: abc-123-uuid-here
Title: Buy milk
Description: (none)
Status: Incomplete
```

---

### Error Output

**Exit Code**: Non-zero (typically 1)

**Format**: `Error: <error_message>`

| Error Scenario | Exit Code | Error Message | Triggered By |
|----------------|-----------|---------------|--------------|
| Task not found | 1 | `Error: Task not found with ID: {task_id}` | KeyError from service layer |
| No updates provided | 1 | `Error: No updates provided. Use --title and/or --description` | Neither flag provided |
| Empty title | 1 | `Error: Title cannot be empty` | ValueError from Task validation |
| Title too long | 1 | `Error: Title cannot exceed 500 characters` | ValueError from Task validation |
| Description too long | 1 | `Error: Description cannot exceed 2000 characters` | ValueError from Task validation |
| Missing task_id | 2 | `error: the following arguments are required: task_id` | argparse validation |
| Invalid flag | 2 | `error: unrecognized arguments: {flag}` | argparse validation |

**Example Error Outputs**:

```bash
$ python -m src.main update nonexistent-id --title "New Title"
Error: Task not found with ID: nonexistent-id

$ python -m src.main update abc-123
Error: No updates provided. Use --title and/or --description

$ python -m src.main update abc-123 --title ""
Error: Title cannot be empty

$ python -m src.main update abc-123 --title "a very long title..." # (> 500 chars)
Error: Title cannot exceed 500 characters

$ python -m src.main update --title "No ID"
usage: todo update [-h] [--title TITLE] [--description DESCRIPTION] task_id
error: the following arguments are required: task_id
```

---

### Help Output

**Trigger**: `python -m src.main update --help` or `python -m src.main update -h`

**Exit Code**: 0

**Format**:
```
usage: todo update [-h] [--title TITLE] [--description DESCRIPTION] task_id

Update an existing task's title and/or description

positional arguments:
  task_id              Unique task identifier (UUID)

options:
  -h, --help           show this help message and exit
  --title TITLE        New task title (1-500 characters)
  --description DESCRIPTION
                       New task description (0-2000 characters, optional)

Examples:
  python -m src.main update abc-123 --title "New Title"
  python -m src.main update abc-123 --description "New Description"
  python -m src.main update abc-123 --title "New Title" --description "New Desc"
```

---

## Exit Codes

| Code | Meaning | Scenarios |
|------|---------|-----------|
| 0 | Success | Task updated successfully, or help displayed |
| 1 | Application error | Task not found, validation failed, no updates provided |
| 2 | Usage error | Missing required argument, unrecognized flag (argparse errors) |

---

## Argument Parsing Implementation

### argparse Configuration

```python
import argparse

parser = argparse.ArgumentParser(
    description='Update an existing task\'s title and/or description',
    prog='todo update'
)

# Positional argument
parser.add_argument(
    'task_id',
    type=str,
    help='Unique task identifier (UUID)'
)

# Optional flags
parser.add_argument(
    '--title',
    type=str,
    default=None,
    help='New task title (1-500 characters)'
)

parser.add_argument(
    '--description',
    type=str,
    default=None,
    help='New task description (0-2000 characters, optional)'
)

# Parse arguments
args = parser.parse_args(args)  # args=None uses sys.argv
```

### Validation Flow

1. **argparse validation** (automatic):
   - `task_id` required (positional) → exit code 2 if missing
   - `--title` and `--description` are optional → None if not provided
   - Unknown flags → exit code 2

2. **Application validation** (in CLI function):
   - Check at least one update provided: `if args.title is None and args.description is None`
   - If neither → print error, sys.exit(1)

3. **Service layer validation** (in update_task function):
   - Task exists → KeyError if not found
   - Title validation → ValueError if empty or > 500 chars
   - Description validation → ValueError if > 2000 chars

4. **Error handling** (in CLI function):
   ```python
   try:
       updated_task = update_task(args.task_id, args.title, args.description)
       # Print success message
       sys.exit(0)
   except KeyError:
       print(f"Error: Task not found with ID: {args.task_id}", file=sys.stderr)
       sys.exit(1)
   except ValueError as e:
       print(f"Error: {e}", file=sys.stderr)
       sys.exit(1)
   ```

---

## Unicode Support

**Requirement**: FR-013 - System MUST support Unicode characters (UTF-8) in title and description fields

**Implementation**:
- Python 3.13+ uses UTF-8 by default for strings
- argparse handles Unicode input automatically
- No special encoding/decoding needed

**Examples**:
```bash
# Unicode in title
python -m src.main update abc-123 --title "Café ☕ meeting"
→ Success (stored and displayed correctly)

# Unicode in description
python -m src.main update xyz-789 --description "Discuss 日本語 documentation"
→ Success (stored and displayed correctly)

# Emoji in both
python -m src.main update def-456 --title "🎉 Party planning" --description "Buy 🎂 and 🎈"
→ Success (stored and displayed correctly)
```

**Validation**: Unicode characters count toward length limits (title ≤ 500 chars, description ≤ 2000 chars)

---

## Integration with Main Router

**Location**: `src/main.py`

**Pattern**: Add "update" command routing (consistent with "add", "view" commands)

```python
def main():
    """Main entry point for the todo CLI application"""
    if len(sys.argv) < 2:
        print("Usage: python -m src.main <command> [args]", file=sys.stderr)
        print("Commands: add, view, update", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]

    if command == 'add':
        from src.cli.add_task import add_task_command
        add_task_command(sys.argv[2:])
    elif command == 'view':
        from src.cli.view_tasks import view_tasks_command
        view_tasks_command(sys.argv[2:])
    elif command == 'update':  # NEW
        from src.cli.update_task import update_task_command
        update_task_command(sys.argv[2:])
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        print("Available commands: add, view, update", file=sys.stderr)
        sys.exit(1)
```

---

## Testing Contract

### Unit Tests (Service Layer)

Test `update_task()` function in isolation:
- ✅ Update title only
- ✅ Update description only
- ✅ Update both title and description
- ✅ Preserve immutable fields (id, created, status)
- ✅ Raise KeyError for non-existent task
- ✅ Raise ValueError for empty title
- ✅ Raise ValueError for title > 500 chars
- ✅ Raise ValueError for description > 2000 chars
- ✅ Raise ValueError when no updates provided (both None)
- ✅ Allow empty description ("")

### Integration Tests (CLI Layer)

Test `update_task_command()` via subprocess:
- ✅ Success output format (title updated)
- ✅ Success output format (description updated)
- ✅ Success output format (both updated)
- ✅ Error message for non-existent ID
- ✅ Error message for no updates provided
- ✅ Error message for empty title
- ✅ Error message for title too long
- ✅ Error message for description too long
- ✅ Unicode character handling
- ✅ Help text display (--help)
- ✅ Exit code 0 on success
- ✅ Exit code 1 on errors

---

## Summary

**CLI Interface Characteristics**:
- ✅ Follows argparse conventions (consistent with Add Task, View Task List)
- ✅ Supports partial updates (title-only, description-only, or both)
- ✅ Clear error messages for all failure scenarios
- ✅ Unicode support (UTF-8 native in Python 3.13+)
- ✅ Standard exit codes (0=success, 1=error, 2=usage)
- ✅ Comprehensive help text with examples
- ✅ Validation at multiple layers (argparse, application, service)
