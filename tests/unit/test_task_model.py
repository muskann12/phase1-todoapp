import pytest
from datetime import datetime
from src.models.task import Task, TaskStatus


def test_task_creation_with_title_only():
    """Test creating a task with just a title"""
    task = Task(id="test-123", title="Buy milk")

    assert task.id == "test-123"
    assert task.title == "Buy milk"
    assert task.description == ""
    assert task.status == TaskStatus.INCOMPLETE
    assert isinstance(task.created, datetime)


def test_task_creation_with_description():
    """Test creating a task with title and description"""
    task = Task(id="test-123", title="Buy milk", description="From the store")

    assert task.title == "Buy milk"
    assert task.description == "From the store"


def test_task_title_trimming():
    """Test that title whitespace is trimmed"""
    task = Task(id="test-123", title="  Buy milk  ")

    assert task.title == "Buy milk"


def test_empty_title_raises_error():
    """Test that empty title raises ValueError"""
    with pytest.raises(ValueError, match="Title cannot be empty"):
        Task(id="test-123", title="")


def test_whitespace_only_title_raises_error():
    """Test that whitespace-only title raises ValueError"""
    with pytest.raises(ValueError, match="Title cannot be empty"):
        Task(id="test-123", title="   ")


def test_title_too_long_raises_error():
    """Test that title over 500 chars raises ValueError"""
    with pytest.raises(ValueError, match="Title cannot exceed 500 characters"):
        Task(id="test-123", title="a" * 501)


def test_description_too_long_raises_error():
    """Test that description over 5000 chars raises ValueError"""
    with pytest.raises(ValueError, match="Description cannot exceed 5000 characters"):
        Task(id="test-123", title="Valid", description="a" * 5001)


def test_special_characters_in_title():
    """Test that special characters are preserved"""
    task = Task(id="test-123", title='Review PR #123 "urgent"')

    assert task.title == 'Review PR #123 "urgent"'


def test_unicode_in_title():
    """Test that Unicode characters are supported"""
    task = Task(id="test-123", title="Café ☕")

    assert task.title == "Café ☕"


def test_empty_description():
    """Test that description defaults to empty string"""
    task = Task(id="test-123", title="Test")

    assert task.description == ""
