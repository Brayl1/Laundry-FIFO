"""PART B: a real singly linked list.

Every value lives in its own Node. A node knows only its data and ONE pointer,
next, to the node after it. The list itself keeps three things:

    head   the first node, or None when the list is empty
    tail   the last node, or None when the list is empty
    _size  a cached count, updated after every add or remove

    head -> [10 | next] -> [20 | next] -> [30 | None]
                                              ^ tail

Nothing here stores the values in a Python list, tuple, dictionary, set or
deque. A temporary list inside to_list() is allowed, and that is the only
place one appears.

Indices are zero-based integers. Negative indices are invalid.
"""


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


def require_integer(index):
    """Shared input contract; bool is not a usable position."""
    if not isinstance(index, int) or isinstance(index, bool):
        raise TypeError("Index must be an integer.")


class SinglyLinkedList:
    def __init__(self, items=None):
        self.head = None
        self.tail = None
        self._size = 0
        if items is not None:
            # append() is O(1) because of tail, so building n nodes is O(n).
            # Reading the iterable once also means it is copied into nodes.
            for value in items:
                self.append(value)

    # ------------------------------------------------------------------ helpers
    def _node_at(self, index):
        """Walk forward from head and return the node at a valid index. O(n)."""
        node = self.head
        for _ in range(index):
            node = node.next
        return node

    # ------------------------------------------------------------------ adding
    def prepend(self, value):
        """Add a new head. O(1)."""
        node = Node(value)
        node.next = self.head          # new node points at the old first node
        self.head = node
        if self.tail is None:          # the list was empty: it is also the tail
            self.tail = node
        self._size += 1

    def append(self, value):
        """Add a new tail. O(1) because tail gives us the last node directly."""
        node = Node(value)
        if self.tail is None:          # empty list: first node is head and tail
            self.head = node
        else:
            self.tail.next = node      # old last node now points at the new one
        self.tail = node
        self._size += 1

    def insert_at(self, index, value):
        """Insert at 0 <= index <= size. Raise IndexError otherwise."""
        require_integer(index)
        if not 0 <= index <= self._size:
            raise IndexError(index)
        if index == 0:
            self.prepend(value)
        elif index == self._size:
            self.append(value)
        else:
            # Find the node BEFORE the new position, then rewire two links.
            # Existing nodes are reused; nothing is rebuilt.
            before = self._node_at(index - 1)
            node = Node(value)
            node.next = before.next
            before.next = node
            self._size += 1

    # ---------------------------------------------------------------- removing
    def _unlink(self, before, node):
        """Remove `node`, which follows `before` (None when node is the head)."""
        if before is None:
            self.head = node.next      # removing the head: the second node leads
        else:
            before.next = node.next    # skip over the removed node
        if node is self.tail:
            self.tail = before         # removed the last node: tail steps back
        node.next = None               # detach the removed node completely
        self._size -= 1
        return node.data

    def remove_at(self, index):
        """Remove and return the value at 0 <= index < size."""
        require_integer(index)
        if not 0 <= index < self._size:
            raise IndexError(index)
        before = None if index == 0 else self._node_at(index - 1)
        node = self.head if before is None else before.next
        return self._unlink(before, node)

    def remove(self, value):
        """Remove the first match and return True; return False if missing."""
        before, node = None, self.head
        while node is not None:
            if node.data == value:
                self._unlink(before, node)
                return True
            before, node = node, node.next
        return False

    # ----------------------------------------------------------------- reading
    def get(self, index):
        """Read the value at an index without changing any link. O(n)."""
        require_integer(index)
        if not 0 <= index < self._size:
            raise IndexError(index)
        return self._node_at(index).data

    def index_of(self, value):
        """Return the first matching index, or -1 if missing. O(n)."""
        node, position = self.head, 0
        while node is not None:
            if node.data == value:
                return position
            node, position = node.next, position + 1
        return -1

    def size(self):
        """The cached node count. O(1)."""
        return self._size

    def is_empty(self):
        return self._size == 0

    def to_list(self):
        """Return a fresh snapshot, head to tail. O(n)."""
        result = []
        node = self.head
        while node is not None:
            result.append(node.data)
            node = node.next
        return result
