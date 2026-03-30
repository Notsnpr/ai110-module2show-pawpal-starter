import pytest
from datetime import time
from pawpal_system import Owner, Pet, Task, Schedule


class TestTaskCompletion:
    """Tests for task completion functionality"""
    
    def test_mark_complete_changes_status(self):
        """Verify that calling mark_complete() changes the task's status from incomplete to complete"""
        # Arrange
        owner = Owner("John Doe")
        pet = Pet("Fluffy", "Golden Retriever", 3, owner)
        task = Task(
            description="Morning Feeding",
            time=time(8, 0),
            instructions="Give 2 cups of dry food",
            pet=pet
        )
        
        # Assert initial state
        assert task.is_completed() == False, "Task should start as incomplete"
        
        # Act
        task.mark_complete()
        
        # Assert
        assert task.is_completed() == True, "Task should be marked as complete"
    
    def test_mark_incomplete_changes_status(self):
        """Verify that calling mark_incomplete() changes a completed task back to incomplete"""
        # Arrange
        owner = Owner("Jane Doe")
        pet = Pet("Buddy", "Labrador", 2, owner)
        task = Task(
            description="Afternoon Walk",
            time=time(14, 0),
            instructions="Walk for 30 minutes",
            pet=pet
        )
        
        # Mark as complete first
        task.mark_complete()
        assert task.is_completed() == True, "Task should be marked as complete"
        
        # Act
        task.mark_incomplete()
        
        # Assert
        assert task.is_completed() == False, "Task should be marked as incomplete"


class TestTaskAddition:
    """Tests for task addition to pets"""
    
    def test_add_task_increases_pet_task_count(self):
        """Verify that adding a task to a Pet increases that pet's task count"""
        # Arrange
        owner = Owner("John Smith")
        pet = Pet("Max", "Tabby Cat", 5, owner)
        
        # Assert initial state
        initial_task_count = len(pet.get_assigned_tasks())
        assert initial_task_count == 0, "Pet should start with no tasks"
        
        # Act
        task = Task(
            description="Feed the cat",
            time=time(9, 0),
            instructions="Give 1 can of wet food",
            pet=pet
        )
        pet.add_task(task)
        
        # Assert
        final_task_count = len(pet.get_assigned_tasks())
        assert final_task_count == 1, "Pet should have exactly 1 task after adding"
        assert final_task_count == initial_task_count + 1, "Task count should increase by 1"
    
    def test_add_multiple_tasks_to_pet(self):
        """Verify that multiple tasks can be added to the same pet and count increases correctly"""
        # Arrange
        owner = Owner("Sarah Johnson")
        pet = Pet("Daisy", "Poodle", 4, owner)
        
        # Act - Add multiple tasks
        task1 = Task("Morning Walk", time(7, 0), "30 minute walk", pet)
        task2 = Task("Feeding", time(12, 0), "1 cup dry food", pet)
        task3 = Task("Evening Walk", time(17, 0), "30 minute walk", pet)
        
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)
        
        # Assert
        assert len(pet.get_assigned_tasks()) == 3, "Pet should have 3 tasks"
        assert task1 in pet.get_assigned_tasks(), "First task should be in pet's task list"
        assert task2 in pet.get_assigned_tasks(), "Second task should be in pet's task list"
        assert task3 in pet.get_assigned_tasks(), "Third task should be in pet's task list"


class TestScheduleIntegration:
    """Tests for schedule management and conflict detection"""
    
    def test_add_task_to_schedule(self):
        """Verify that adding a task to the schedule properly tracks it"""
        # Arrange
        schedule = Schedule()
        owner = Owner("John Doe")
        pet = Pet("Fluffy", "Golden Retriever", 3, owner)
        task = Task("Feeding", time(8, 0), "Give dry food", pet)
        
        # Act
        schedule.add_task(task)
        
        # Assert
        assert len(schedule.get_tasks_info()) == 1, "Schedule should have 1 task"
        assert task in schedule.get_tasks_info(), "Task should be in schedule"
    
    def test_detect_scheduling_conflict(self):
        """Verify that scheduling conflicts (same pet, same time) are detected"""
        # Arrange
        schedule = Schedule()
        owner = Owner("John Smith")
        pet = Pet("Fluffy", "Golden Retriever", 3, owner)
        
        task1 = Task("Feeding", time(9, 0), "Give dry food", pet)
        task2 = Task("Bath", time(9, 0), "Give a bath", pet)
        
        # Act
        schedule.add_task(task1)
        schedule.add_task(task2)
        conflicts = schedule.check_conflicts()
        
        # Assert
        assert len(conflicts) > 0, "Conflict should be detected"
        assert "CONFLICT" in conflicts[0], "Conflict message should contain 'CONFLICT'"
        assert "Fluffy" in conflicts[0], "Conflict message should mention the pet name"
        assert "09:00" in conflicts[0], "Conflict message should mention the conflicting time"
    
    def test_no_conflict_with_different_times(self):
        """Verify that no conflict is detected when tasks are at different times"""
        # Arrange
        schedule = Schedule()
        owner = Owner("John Smith")
        pet = Pet("Fluffy", "Golden Retriever", 3, owner)
        
        task1 = Task("Feeding", time(8, 0), "Give dry food", pet)
        task2 = Task("Walk", time(14, 0), "Walk in park", pet)
        
        # Act
        schedule.add_task(task1)
        schedule.add_task(task2)
        conflicts = schedule.check_conflicts()
        
        # Assert
        assert len(conflicts) == 0, "No conflict should be detected for different times"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
