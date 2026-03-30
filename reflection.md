# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My initial UML design focused on a simple workflow where a user could add pets, schedule tasks, and view today's tasks in order.

The original classes and responsibilities were:

- **Owner**: stores owner identity and the pets belonging to that owner.
- **Pet**: stores pet details and the tasks assigned to that pet.
- **Task**: stores task description and scheduled time.
- **Schedule**: stores daily tasks and displays them in chronological order.

This first version gave me a clean baseline to build from, even though it was missing some cross-owner scheduling behavior and recurrence details.

**b. Design changes**

**Yes, the design changed significantly as we clarified the system's user:**

1. **Centralized Schedule**: Initially, the Schedule was meant to be per-owner. We changed it to be a single centralized system because the front desk person is the actual user—they need to see ALL tasks across ALL owners and pets to detect and resolve conflicts.

2. **Task-Pet Relationship**: We added a direct reference from Task to the Pet it belongs to. This allows the Schedule to trace back which pet has conflicting tasks, enabling the front desk to quickly identify and resolve issues like "John's Fluffy has two tasks at 9:30 AM."

3. **Time Format**: We changed from string time (e.g., "9:30") to Python's `time` object. This makes comparing times for conflicts much easier and more reliable.

4. **Owner Identity**: Added a `name` attribute to Owner so the front desk can identify owners in conflict reports.

5. **Task Management on Pet**: Added an `add_task()` method directly to Pet so tasks can be managed at the pet level, improving encapsulation.

**Why we made these changes**: Once we understood that the front desk person is the system operator (not the pet owner), we realized the architecture needed to support a centralized, conflict-aware view of all tasks. The initial design was too fragmented and didn't provide the front desk with the visibility they need.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

**Our scheduler currently prioritizes time consistency, conflict visibility, and operational clarity over advanced optimization.**

The main constraints it considers are:

1. **Scheduled time (`time` object)**: Tasks are sorted chronologically so the front desk can view the day in execution order.
2. **Conflict checks at the same time**: The system flags warnings when two tasks share the same start time, for both the same pet and different pets.
3. **Completion status**: Tasks are tracked as pending vs completed so staff can monitor progress quickly.
4. **Pet/owner association**: Every task is tied to a pet (and therefore owner), which allows filtering and clear conflict messages.
5. **Recurrence frequency**: Daily and weekly tasks automatically generate a next instance after completion to keep recurring care on schedule.

We treated these as highest priority because they map directly to front-desk workflow: see what is next, detect collisions early, and keep recurring care from being forgotten. We deferred lower-priority constraints (owner preferences, task duration balancing, and weighted priorities) to keep the first version reliable and easy to maintain.

**b. Tradeoffs**

**One key tradeoff is that conflict detection only checks for exact same start times, not overlapping durations.**

For example, if one task runs from 10:00-10:30 and another starts at 10:15, the current scheduler will not detect that overlap unless both are set to exactly 10:00. This is reasonable for this version because tasks currently store only a single time (not duration), and the goal was to provide lightweight, reliable warnings without adding complex time-interval logic. It keeps the system simple, fast, and easy to explain for front-desk use, while still catching the most obvious scheduling collisions.

---

## 3. AI Collaboration

**a. How you used AI**

I used VS Code Copilot in multiple phases: UML planning, implementation, test design, and documentation cleanup.

Copilot features that were most effective for building this scheduler were:

- **#codebase chat grounding**: helped me ask for implementation-accurate updates (for example, matching README and UML to actual method names and behavior).
- **Targeted test ideation**: useful for generating high-value edge cases around sorting, recurrence, and conflict detection.
- **Refactor assistance**: helped convert UI logic to use scheduler methods directly, reducing duplicated logic in the Streamlit layer.
- **Documentation drafting**: sped up converting technical behavior into rubric-friendly feature descriptions and reflection language.

The most helpful prompts were specific and constraint-based, such as:

- "List edge cases for sorting and recurring tasks based on this codebase."
- "Update app display logic to use Scheduler methods, not ad-hoc list logic."
- "Align UML names/signatures with implemented Python classes."

**b. Judgment and verification**

One moment I did not accept AI output as-is was when reviewing documentation/diagram naming. Some suggestions initially leaned toward generic or camelCase-style labels, but my implementation is Pythonic and uses snake_case methods. I modified the output so UML and docs matched the real code exactly.

I validated AI suggestions by:

- Comparing against implementation in `pawpal_system.py` method-by-method.
- Running tests (`python -m pytest`) after code changes.
- Rejecting or editing any suggestion that introduced claims not backed by implemented behavior.

This kept the architecture clean and prevented "docs drift" from the real system.

I also used separate chat sessions for different phases (design/UML, testing, UI polish, documentation). That separation helped me stay organized by keeping each thread focused on one decision space, reducing context mixing and making it easier to audit what changed and why.

---

## 4. Testing and Verification

**a. What you tested**

I tested the core scheduling behaviors that are most likely to break in real usage:

- Task completion state transitions (`mark_complete`, `mark_incomplete`).
- Task addition to pets and schedule-level task tracking.
- Chronological sorting of tasks.
- Conflict detection for same-time tasks (same pet and different pets).
- Filtering by pet and status (including combined filters).
- Recurrence behavior:
	- recurring task identification,
	- day-based recurrence expansion,
	- auto-creation of the next recurring instance on completion,
	- no duplicate instance creation when marking an already-completed task.
- Edge cases:
	- empty schedule behavior,
	- unknown status input handling,
	- whitespace-normalized pet name filtering,
	- boundary time sorting (00:00 and 23:59),
	- schedule/pet list consistency on task removal.

These tests were important because they validate both correctness (expected outputs) and reliability (stable behavior on edge conditions).

**b. Confidence**

I am **4/5 confident** in the scheduler's reliability for the current scope. The test suite passes and covers core behavior plus key edge cases.

If I had more time, I would test:

- Overlap detection with task durations (not just exact start-time conflicts).
- Invalid recurrence formats and stricter recurrence validation.
- Time zone/day-boundary behavior for recurring tasks.
- Multi-owner, high-volume stress scenarios for conflict pairing and UI readability.

---

## 5. Reflection

**a. What went well**

I am most satisfied with the progression from a basic class model to a practical scheduler that is test-driven and UI-connected. The system now has a clear separation of concerns: scheduling logic in the backend, presentation in Streamlit, and behavior verification in tests.

**b. What you would improve**

In a second iteration, I would add task duration and priority scoring so schedule generation could move from "ordered list + warnings" to true optimization. I would also redesign recurrence to include explicit date anchoring so one-time and recurring semantics are more precise.

**c. Key takeaway**

My biggest takeaway is that using AI effectively requires acting as the **lead architect**, not just a code accepter. Copilot is powerful for speed and breadth, but system quality depends on human decisions about boundaries, naming consistency, test strategy, and scope. The best results came when I gave precise constraints, verified outputs against the codebase, and treated AI suggestions as draft proposals that must pass architectural review.
