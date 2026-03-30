from dataclasses import dataclass, field
from typing import List
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
    
    def check_conflicts(self) -> List[str]:
        """Check for time conflicts in scheduled tasks (same pet, same time)"""
        conflicts = []
        
        # Group tasks by pet
        tasks_by_pet = {}
        for task in self.tasks:
            pet_id = task.pet.get_identifier()
            if pet_id not in tasks_by_pet:
                tasks_by_pet[pet_id] = []
            tasks_by_pet[pet_id].append(task)
        
        # Check for conflicts within each pet's tasks
        for pet_id, pet_tasks in tasks_by_pet.items():
            for i, task1 in enumerate(pet_tasks):
                for task2 in pet_tasks[i+1:]:
                    if task1.get_time() == task2.get_time():
                        pet = task1.get_pet()
                        owner_name = pet.get_owner().get_name()
                        conflict_msg = (
                            f"CONFLICT: {owner_name}'s {pet.get_identifier()} has two tasks "
                            f"at {task1.get_time().strftime('%H:%M')} - "
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
        """Mark a task as completed"""
        task.mark_complete()
    
    def remove_task(self, task: Task):
        """Remove a task from the schedule"""
        if task in self.tasks:
            self.tasks.remove(task)
            # Remove from pet's task list as well
            pet = task.get_pet()
            if task in pet.get_assigned_tasks():
                pet.assigned_tasks.remove(task)
