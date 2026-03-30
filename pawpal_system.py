from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    """Task class that represents a task for a pet"""
    description: str
    time: str
    instructions: str
    
    def get_description(self):
        """Get the task description"""
        return self.description
    
    def get_time(self):
        """Get the scheduled time for this task"""
        return self.time
    
    def get_instructions(self):
        """Get the instructions for this task"""
        return self.instructions


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


class Owner:
    """Owner class that manages pets and schedules tasks for them"""
    
    def __init__(self):
        """Initialize owner with empty pets list"""
        self.pets = []
    
    def add_pet(self, pet):
        """Add a pet to the owner's collection"""
        pass
    
    def get_pets(self):
        """Get all pets belonging to this owner"""
        pass
    
    def add_task_to_pet(self, pet, task):
        """Add a task to a specific pet"""
        pass


class Schedule:
    """Schedule class that manages tasks and handles scheduling conflicts"""
    
    def __init__(self):
        """Initialize schedule with empty tasks list and conflicts list"""
        self.tasks = []
        self.conflicts = []
    
    def modify_tasks(self, task):
        """Modify tasks to resolve scheduling conflicts"""
        pass
    
    def get_tasks_info(self):
        """Get information about all scheduled tasks"""
        pass
    
    def check_conflicts(self):
        """Check for time conflicts in scheduled tasks"""
        pass
