from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from datetime import time, datetime


@dataclass
class Task:
    """Task class that represents a single activity for a pet"""
    description: str
    time: time  # Use time object for easy comparison (e.g., time(9, 30))
    instructions: str
    pet: 'Pet'  # Reference to which pet this task belongs to
    frequency: str = "daily"  # daily, weekly, once, etc.
    completion_status: bool = False  # Whether the task is completed
    
    def get_description(self):
        """Get the task description"""
        return self.description
    
    def get_time(self):
        """Get the scheduled time for this task"""
        return self.time
    
    def get_instructions(self):
        """Get the instructions for this task"""
        return self.instructions
    
    def get_pet(self):
        """Get the pet this task belongs to"""
        return self.pet
    
    def get_frequency(self):
        """Get the frequency of this task"""
        return self.frequency
    
    def is_completed(self):
        """Check if the task is completed"""
        return self.completion_status
    
    def mark_complete(self):
        """Mark the task as completed"""
        self.completion_status = True
    
    def mark_incomplete(self):
        """Mark the task as incomplete"""
        self.completion_status = False


@dataclass
class Pet:
    """Pet class that holds information about pets and their tasks"""
    identifier: str
    breed: str
    age: int
    owner: 'Owner'
    assigned_tasks: List[Task] = field(default_factory=list)
    
    def get_identifier(self):
        """Get the pet's identifier"""
        return self.identifier
    
    def get_breed(self):
        """Get the pet's breed"""
        return self.breed
    
    def get_age(self):
        """Get the pet's age"""
        return self.age
    
    def get_assigned_tasks(self):
        """Get all tasks assigned to this pet"""
        return self.assigned_tasks
    
    def get_owner(self):
        """Get the owner of this pet"""
        return self.owner
    
    def add_task(self, task: Task):
        """Add a task to this pet's task list"""
        self.assigned_tasks.append(task)
    
    def get_completed_tasks(self):
        """Get all completed tasks for this pet"""
        return [task for task in self.assigned_tasks if task.is_completed()]
    
    def get_pending_tasks(self):
        """Get all pending (incomplete) tasks for this pet"""
        return [task for task in self.assigned_tasks if not task.is_completed()]


class Owner:
    """Owner class that manages pets"""
    
    def __init__(self, name: str):
        """Initialize owner with name and empty pets list"""
        self.name = name
        self.pets = []
    
    def get_name(self):
        """Get the owner's name"""
        return self.name
    
    def add_pet(self, pet: Pet):
        """Add a pet to the owner's collection"""
        self.pets.append(pet)
    
    def get_pets(self):
        """Get all pets belonging to this owner"""
        return self.pets
    
    def get_all_tasks(self):
        """Get all tasks across all of this owner's pets"""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_assigned_tasks())
        return all_tasks
    
    def get_pets_count(self):
        """Get the number of pets this owner has"""
        return len(self.pets)


class Schedule:
    """Centralized schedule that manages all tasks and detects scheduling conflicts"""
    
    def __init__(self):
        """Initialize schedule with empty tasks list"""
        self.tasks = []
    
    def add_task(self, task: Task):
        """Add a task to the schedule and to the corresponding pet"""
        self.tasks.append(task)
        task.pet.add_task(task)
    
    def get_tasks_info(self):
        """Get information about all scheduled tasks"""
        return self.tasks

    def get_tasks_sorted_by_time(self) -> List[Task]:
        """Return all tasks sorted by scheduled time"""
        return sorted(self.tasks, key=lambda task: task.get_time())
    
    def get_tasks_by_pet(self, pet: Pet) -> List[Task]:
        """Get all tasks for a specific pet"""
        return [task for task in self.tasks if task.get_pet() == pet]
    
    def get_tasks_by_owner(self, owner: Owner) -> List[Task]:
        """Get all tasks for all pets belonging to a specific owner"""
        owner_tasks = []
        for pet in owner.get_pets():
            owner_tasks.extend(self.get_tasks_by_pet(pet))
        return owner_tasks
    
    def get_tasks_by_time(self, target_time: time) -> List[Task]:
        """Get all tasks scheduled for a specific time"""
        return [task for task in self.tasks if task.get_time() == target_time]

    def filter_tasks(self, pet: Optional[Pet] = None, status: Optional[str] = None) -> List[Task]:
        """Filter tasks by pet and completion status"""
        pet_name = pet.get_identifier() if pet is not None else None
        return self._filter_tasks_core(status=status, pet_name=pet_name)

    def filter_tasks_by_status_or_pet_name(
        self,
        status: Optional[str] = None,
        pet_name: Optional[str] = None,
    ) -> List[Task]:
        """Filter tasks by completion status and/or pet name"""
        return self._filter_tasks_core(status=status, pet_name=pet_name)

    def _filter_tasks_core(
        self,
        status: Optional[str] = None,
        pet_name: Optional[str] = None,
    ) -> List[Task]:
        """Shared filtering implementation used by public task-filter methods"""
        filtered_tasks = self.tasks

        normalized_pet_name = pet_name.strip().lower() if pet_name else None
        normalized_status = self._normalize_status(status)

        if normalized_pet_name is not None:
            filtered_tasks = [
                task for task in filtered_tasks
                if task.get_pet().get_identifier().strip().lower() == normalized_pet_name
            ]

        if normalized_status == "completed":
            filtered_tasks = [task for task in filtered_tasks if task.is_completed()]
        elif normalized_status == "pending":
            filtered_tasks = [task for task in filtered_tasks if not task.is_completed()]

        return filtered_tasks

    def _normalize_status(self, status: Optional[str]) -> Optional[str]:
        """Normalize status aliases to completed/pending when recognized"""
        if status is None:
            return None

        normalized_status = status.strip().lower()
        completed_aliases = {"completed", "complete", "done"}
        pending_aliases = {"pending", "incomplete", "not completed"}

        if normalized_status in completed_aliases:
            return "completed"
        if normalized_status in pending_aliases:
            return "pending"
        return None

    def get_recurring_tasks(self) -> List[Task]:
        """Get tasks that recur (all frequencies except 'once')"""
        return [task for task in self.tasks if task.get_frequency().lower() != "once"]

    def get_tasks_for_day(self, day_name: str) -> List[Task]:
        """Get tasks that should appear on a specific day"""
        normalized_day = day_name.lower()

        def appears_on_day(task: Task) -> bool:
            frequency = task.get_frequency().lower()
            if frequency in {"daily", "once"}:
                return True
            if frequency == normalized_day:
                return True
            if frequency.startswith("weekly:"):
                return frequency.split(":", 1)[1] == normalized_day
            return False

        day_tasks = [task for task in self.tasks if appears_on_day(task)]
        return sorted(day_tasks, key=lambda task: task.get_time())

    def _find_conflicting_task_pairs(self) -> List[Tuple[Task, Task]]:
        """Return task pairs that overlap in time (same or different pets)"""
        conflicts: List[Tuple[Task, Task]] = []

        tasks_by_time = self._group_tasks_by_time()
        for grouped_tasks in tasks_by_time.values():
            if len(grouped_tasks) < 2:
                continue

            for i, task1 in enumerate(grouped_tasks):
                for task2 in grouped_tasks[i + 1:]:
                    conflicts.append((task1, task2))

        return conflicts

    def _group_tasks_by_time(self) -> Dict[time, List[Task]]:
        """Group tasks by scheduled time for efficient overlap checks"""
        tasks_by_time: Dict[time, List[Task]] = {}
        for task in self.tasks:
            task_time = task.get_time()
            if task_time not in tasks_by_time:
                tasks_by_time[task_time] = []
            tasks_by_time[task_time].append(task)
        return tasks_by_time
    
    def check_conflicts(self) -> List[str]:
        """Check for same-time conflicts for tasks across all pets"""
        conflicts = []

        for task1, task2 in self._find_conflicting_task_pairs():
            pet1 = task1.get_pet()
            pet2 = task2.get_pet()
            owner1 = pet1.get_owner().get_name()
            owner2 = pet2.get_owner().get_name()

            if pet1 == pet2:
                conflict_msg = (
                    f"CONFLICT (SAME PET): {owner1}'s {pet1.get_identifier()} has two tasks "
                    f"at {task1.get_time().strftime('%H:%M')} - "
                    f"'{task1.get_description()}' and '{task2.get_description()}'"
                )
            else:
                conflict_msg = (
                    f"CONFLICT (TIME OVERLAP): {owner1}'s {pet1.get_identifier()} and "
                    f"{owner2}'s {pet2.get_identifier()} both have tasks at "
                    f"{task1.get_time().strftime('%H:%M')} - "
                    f"'{task1.get_description()}' and '{task2.get_description()}'"
                )
            conflicts.append(conflict_msg)

        return conflicts
    
    def modify_task(self, task: Task, new_time: time):
        """Modify a task's time to resolve conflicts"""
        task.time = new_time
    
    def get_pending_tasks(self) -> List[Task]:
        """Get all incomplete tasks in the schedule"""
        return [task for task in self.tasks if not task.is_completed()]
    
    def get_completed_tasks(self) -> List[Task]:
        """Get all completed tasks in the schedule"""
        return [task for task in self.tasks if task.is_completed()]
    
    def get_daily_tasks(self) -> List[Task]:
        """Get all daily recurring tasks"""
        return [task for task in self.tasks if task.get_frequency() == "daily"]
    
    def mark_task_complete(self, task: Task):
        """Mark a task as completed and spawn next instance for recurring tasks"""
        if task.is_completed():
            return

        task.mark_complete()
        if self._is_auto_recurring_frequency(task.get_frequency()):
            next_task = self._create_next_occurrence(task)
            self.add_task(next_task)

    def _is_auto_recurring_frequency(self, frequency: str) -> bool:
        """Return True when a frequency should auto-create its next occurrence"""
        normalized_frequency = frequency.strip().lower()
        return normalized_frequency == "daily" or normalized_frequency.startswith("weekly")

    def _create_next_occurrence(self, task: Task) -> Task:
        """Create a new pending task instance representing the next recurrence"""
        return Task(
            description=task.get_description(),
            time=task.get_time(),
            instructions=task.get_instructions(),
            pet=task.get_pet(),
            frequency=task.get_frequency(),
        )
    
    def remove_task(self, task: Task):
        """Remove a task from the schedule"""
        if task in self.tasks:
            self.tasks.remove(task)
            # Remove from pet's task list as well
            pet = task.get_pet()
            if task in pet.get_assigned_tasks():
                pet.assigned_tasks.remove(task)
