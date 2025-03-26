from main_code.priority_queue import Queue
import pytest
from main_code.priority_queue import Queue

@pytest.fixture
def queue():
    return Queue()

def test_is_empty(queue):
    """Test if the queue is empty initially."""
    assert queue.is_empty() is True

def test_enqueue(queue):
    """Test if the enqueue method adds items correctly to the queue."""
    queue.enqueue((1, 10))
    assert queue.size() == 1
    queue.enqueue((2, 5))
    assert queue.size() == 2
    assert queue.items == [(2, 5), (1, 10)]

def test_dequeue(queue):
    """Test if the dequeue method removes the correct item."""
    queue.enqueue((1, 10))
    queue.enqueue((2, 5))
    assert queue.dequeue() == (2, 5)  # item with lower priory dequeued first
    assert queue.size() == 1
    assert queue.dequeue() == (1, 10)
    assert queue.is_empty() is True

def test_size(queue):
    """Test the size method."""
    assert queue.size() == 0
    queue.enqueue((1, 10))
    assert queue.size() == 1
    queue.enqueue((2, 5))
    assert queue.size() == 2

def test_show(queue):
    """Test the show method."""
    queue.enqueue((1, 10))
    queue.enqueue((2, 5))
    assert queue.show() == [(2, 5), (1, 10)]
def test_show_front(queue):
    """Test if the showFront method shows the front item correctly."""
    queue.enqueue((1, 10))
    queue.enqueue((2, 5))
    assert queue.show_front() == (2, 5)
