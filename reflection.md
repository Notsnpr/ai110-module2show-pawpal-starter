# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- **A user should be able to add a pet**
- **A user should be able to scheduel a task for a pet**
- **The user should be able to see todays tasks**
- What classes did you include, and what responsibilities did you assign to each?
- **Pet Class which should contain tasks assgined to it**
- **Tasks Class which should contain name of task and what time said task is set for**
- **Scheduel class which should contain the order of what tasks are for the specific day**
- **Owner class which should contain which pet belongs to them**

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
