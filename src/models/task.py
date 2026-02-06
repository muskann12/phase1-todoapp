from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class TaskStatus(Enum):
    """Task completion status"""
    INCOMPLETE = "incomplete"
    COMPLETE = "complete"


@dataclass
class Task:
    """Represents a single todo item"""
    id: str
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.INCOMPLETE
    created: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate task fields after initialization"""
        # Title validation
        self.title = self.title.strip()
        if not self.title:
            raise ValueError("Title cannot be empty")
        if len(self.title) > 500:
            raise ValueError(f"Title cannot exceed 500 characters (provided: {len(self.title)})")

        # Description validation
        if len(self.description) > 5000:
            raise ValueError(f"Description cannot exceed 5000 characters (provided: {len(self.description)})")
