"""PART A: a real first-in, first-out (FIFO) queue.

The Service queue page calls this class. The earliest request that joined must
be the first one served: if A, B and C join in that order, A leaves first.

Representation: a collections.deque. A deque is a doubly-ended queue, so adding
at the rear (append) and removing from the front (popleft) are both O(1).
A plain list would need list.pop(0), which shifts every remaining item left
and is O(n).

to_list() returns a NEW list in arrival order (front to rear), because Django
saves that snapshot in SQLite and rebuilds the queue from it on the next request.
"""
from collections import deque


class ServiceQueue:
    def __init__(self, items=None):
        # deque(items) copies the values, so changing the caller's list later
        # cannot change this queue. Saved values are already in arrival order.
        self._items = deque(items) if items is not None else deque()

    def enqueue(self, value):
        """Add a request at the rear. O(1)."""
        self._items.append(value)

    def dequeue(self):
        """Remove and return the earliest request still waiting. O(1)."""
        if self.is_empty():
            raise IndexError("The service queue is empty.")
        return self._items.popleft()

    def peek(self):
        """Read the front request without removing it. Same item dequeue returns."""
        if self.is_empty():
            raise IndexError("The service queue is empty.")
        return self._items[0]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def to_list(self):
        """Return a fresh arrival-order snapshot (front to rear) for persistence."""
        return list(self._items)
