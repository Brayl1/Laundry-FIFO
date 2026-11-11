# Suds & Stats: laundry order tracker

A Django web app for small laundry shops. Customers drop off a bag, the shop weighs it, works out the price,
washes bags in the order they arrived, and tells the customer when it is ready. The service queue is a real
first-in-first-out queue and the laundry workflow is a real singly linked list, both written by hand in
`backend/dsa/`.

> **App idea:** Laundry service tracker (bags waiting to be washed; the process is Receive, Wash, Dry, Fold).
> Concept approval from the instructor: _fill in the approval date here before submitting_.

## Who it helps

Owners and attendants of small laundry shops, laundromats and dormitory laundry rooms. Today they usually keep orders
on paper slips or in a chat group, so bags get washed out of order, customers argue about whose turn it is, and nobody
knows how much money is waiting at the counter. Suds & Stats gives the counter one shared line that is always
fair (earliest bag first), records the customer, weight and price of each bag, shows what is ready for pickup, and
writes the pickup message so the attendant only has to press Copy.

## How to run

Requirements: Python 3.12 or 3.13 (tick "Add python.exe to PATH") and internet for the first setup. Use Windows PowerShell.

```powershell
.\SETUP.bat
.\START.bat --port 8001
```

Open http://127.0.0.1:8001/ and create your account and your laundry shop. There are no default accounts. If the port is
busy, use `--port 8002`.

## What was built

### Part A: the service queue (`backend/dsa/queue.py`)
A first-in-first-out queue on a `collections.deque`. `enqueue` adds at the rear, `dequeue` removes the earliest bag
still waiting, `peek` reads the same bag without removing it, and an empty `dequeue` or `peek` raises `IndexError`.

### Part B: the workflow (`backend/dsa/singly_linked_list.py`)
A real singly linked list. Every value lives in a `Node` with `data` and one `next`. The list keeps `head`, `tail` and a
cached `_size`. It stores no Python list, tuple, dictionary, set or deque, and existing nodes stay the same objects when
another node is added or removed. The Data structure inspector on the Workflow page shows the real chain.

### Part C: the laundry app
- **Rebrand:** name, wording, labels, sample data and favicon. Orders have a customer, a service and turnaround labels
  (Standard, Express, Rush). Statuses read Waiting, Washing and Ready for pickup, and "archive" became Picked up.
- **Redesign:** a new light, flat design with a dark sidebar, laundry status colors, a washer graphic on the queue, larger
  readable text, and layouts that turn into cards on phones (see `docs/DESIGN_REFERENCE.md`).
- **New feature 1: customer and load details with automatic pricing.** Each order records the customer name, mobile number,
  service (Wash & fold, Wash & dry, Dry only, Bedding & comforters) and weight in kilograms. The amount due is the weight
  times the service's price per kilogram, and appears on the queue, the order list, the order page and the CSV export.
  This added four columns (`database/migrations/0003_laundry_order_details.py`).
- **New feature 2: sales report.** Sales & reports shows total sales, kilos washed, kilos still waiting, and sales and
  kilos for each service. Dashboard shows how much money is waiting in bags that are ready for pickup.
- **New feature 3: pickup message.** When an order is Ready for pickup, its page shows a ready-to-send text with the
  customer's name, reference, weight and amount due, and a Copy button.

Login, roles (a viewer cannot edit), shops (workspaces) and their separation are unchanged. The files in `challenge/` and
`tests/` were not edited.

## Price per kilogram

| Service | Price |
|---|---|
| Wash & fold | PHP 40 |
| Wash & dry | PHP 35 |
| Dry only | PHP 20 |
| Bedding & comforters | PHP 60 |

The rates are in `database/models.py` (`RATE_PER_KG`).

## How the queue and the linked list work

**Queue.** When a bag joins, Django rebuilds the `ServiceQueue` from the saved list of waiting order IDs, calls
`enqueue`, and saves `to_list()` again. When the attendant presses Start washing, it calls `dequeue`, and the Next up
card calls `peek`. Because the queue is a deque, adding at the rear and removing from the front are both O(1). A plain list
would use `pop(0)`, which shifts every remaining item and is O(n).

**Linked list.** The workflow steps are nodes: `head -> [Receive | next] -> [Wash | next] -> [Dry | next] -> [Fold | None]`,
with `tail` pointing at Fold. `append` is O(1) because `tail` already points at the last node, so the new node is attached
without walking the chain. `get(index)` is O(n) because a singly linked list has no positions: it must follow `next`
from `head` one node at a time. Removing the last node is also O(n), since the node before it has to be found.

| Operation | Time |
|---|---|
| Queue enqueue, dequeue, peek, size, is_empty | O(1) |
| List prepend, append, remove_at(0), size, is_empty | O(1) |
| List get, index_of, middle insert, middle remove | O(n) |
| List remove last node | O(n) |
| to_list() and loading a saved snapshot | O(n) |

A whole web request is not O(1) just because the queue operation is: it also loads and saves data and renders a page.

## Checks

```powershell
.\RUN_TESTS.bat        # application tests, must say OK (57 tests)
.\CHECK_QUEUE.bat      # FIFO goal tests
.\CHECK_LINKED_LIST.bat   # linked list goal tests
.\CHECK_ACTIVITY.bat
.\RUN_ALL_CHECKS.bat   # must say OK
```

## Evidence for submission

Save screenshots and outputs in `docs/evidence/`. `docs/SUBMISSION_EVIDENCE.md` lists exactly what to capture, before and
after.

## Contribution table

| Member | What they built |
|---|---|
| _Your name_ | _e.g. Part A queue, Part B linked list_ |
| _Teammate name_ | _e.g. Part C design and features_ |

## Do not submit

The `.venv` folder, `database/data/*.sqlite3`, `__pycache__` folders or any secret keys.
