import uuid
from datetime import datetime
from typing import Dict

from src.models.task import Task, TaskStatus

# In-memory storage: maps task ID to Task object
_tasks: Dict[str, Task] = {}

# Namespace UUID for deterministic ID generation
TODO_NAMESPACE = uuid.UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')


def generate_task_id(counter: int) -> str:
    """
    Generate a unique, deterministic task ID using UUID5.

    Args:
        counter: Sequential counter for uniqueness (typically len(_tasks))

    Returns:
        str: UUID5-based task ID
    """
    name = f"task-{datetime.now().isoformat()}-{counter}"
    return str(uuid.uuid5(TODO_NAMESPACE, name))


def create_task(title: str, description: str = "") -> Task:
    """
    Create a new task with the given title and optional description.

    Args:
        title: Task title (required, will be trimmed, must be non-empty)
        description: Task description (optional, defaults to empty string)

    Returns:
        Task: The created task object

    Raises:
        ValueError: If title is empty/whitespace-only, title > 500 chars,
                    or description > 5000 chars
    """
    # Generate unique ID
    task_id = generate_task_id(len(_tasks))

    # Create task (validation happens in Task.__post_init__)
    task = Task(
        id=task_id,
        title=title,
        description=description,
        status=TaskStatus.INCOMPLETE,
        created=datetime.now()
    )

    # Store in memory
    _tasks[task.id] = task

    return task


def get_task(task_id: str) -> Task:
    """
    Retrieve a task by ID.

    Args:
        task_id: The task's unique identifier

    Returns:
        Task: The task object

    Raises:
        KeyError: If task ID not found
    """
    return _tasks[task_id]


def get_all_tasks() -> list[Task]:
    """
    Retrieve all tasks sorted by ID in ascending order.

    Returns:
        list[Task]: All tasks sorted by task ID (deterministic order)

    Note:
        This is a read-only operation. The internal _tasks dict is not modified.
    """
    return sorted(_tasks.values(), key=lambda task: task.id)


def update_task(task_id: str, title: str | None = None, description: str | None = None) -> Task:
    """
    Update an existing task's title and/or description.

    Args:
        task_id: The task's unique identifier
        title: New title (None = unchanged)
        description: New description (None = unchanged)

    Returns:
        Task: The updated task object

    Raises:
        KeyError: If task ID not found
        ValueError: If no updates provided or validation fails
    """
    # Validate task exists
    if task_id not in _tasks:
        raise KeyError(f"Task not found with ID: {task_id}")

    # Validate at least one update provided
    if title is None and description is None:
        raise ValueError("No updates provided. Use title and/or description parameters")

    # Get existing task
    existing_task = _tasks[task_id]

    # Determine new values (preserve if None)
    new_title = title if title is not None else existing_task.title
    new_description = description if description is not None else existing_task.description

    # Create updated task (triggers validation in __post_init__)
    updated_task = Task(
        id=existing_task.id,           # Preserve (immutable)
        title=new_title,               # New or existing
        description=new_description,   # New or existing
        status=existing_task.status,   # Preserve (not updated here)
        created=existing_task.created  # Preserve (immutable)
    )

    # Replace in storage
    _tasks[task_id] = updated_task

    return updated_task


def delete_task(task_id: str) -> Task:
    """
    Delete a task from in-memory storage.

    Args:
        task_id: The task's unique identifier

    Returns:
        Task: The deleted task object (captured before removal)

    Raises:
        KeyError: If task ID not found
    """
    # Validate task exists
    if task_id not in _tasks:
        raise KeyError(f"Task not found with ID: {task_id}")

    # Remove from storage and capture deleted task
    deleted_task = _tasks.pop(task_id)

    return deleted_task


def mark_complete(task_id: str) -> Task:
    """
    Mark a task as complete.

    Args:
        task_id: The ID of the task to mark as complete

    Returns:
        Task: The updated task with COMPLETE status

    Raises:
        KeyError: If task with given ID does not exist
    """
    if task_id not in _tasks:
        raise KeyError(f"Task not found with ID: {task_id}")

    task = _tasks[task_id]
    updated_task = Task(
        id=task.id,
        title=task.title,
        description=task.description,
        status=TaskStatus.COMPLETE,
        created=task.created
    )
    _tasks[task_id] = updated_task
    return updated_task


def mark_incomplete(task_id: str) -> Task:
    """
    Mark a task as incomplete.

    Args:
        task_id: The ID of the task to mark as incomplete

    Returns:
        Task: The updated task with INCOMPLETE status

    Raises:
        KeyError: If task with given ID does not exist
    """
    if task_id not in _tasks:
        raise KeyError(f"Task not found with ID: {task_id}")

    task = _tasks[task_id]
    updated_task = Task(
        id=task.id,
        title=task.title,
        description=task.description,
        status=TaskStatus.INCOMPLETE,
        created=task.created
    )
    _tasks[task_id] = updated_task
    return updated_task


def toggle_status(task_id: str) -> Task:
    """
    Toggle a task's completion status.

    Args:
        task_id: The ID of the task to toggle

    Returns:
        Task: The updated task with toggled status

    Raises:
        KeyError: If task with given ID does not exist
    """
    if task_id not in _tasks:
        raise KeyError(f"Task not found with ID: {task_id}")

    task = _tasks[task_id]
    new_status = TaskStatus.COMPLETE if task.status == TaskStatus.INCOMPLETE else TaskStatus.INCOMPLETE

    updated_task = Task(
        id=task.id,
        title=task.title,
        description=task.description,
        status=new_status,
        created=task.created
    )
    _tasks[task_id] = updated_task
    return updated_task


def clear_tasks():
    """Clear all tasks from storage (useful for testing)"""
    _tasks.clear()
