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

    def test_tasks_are_sorted_by_time(self):
        """Verify schedule returns tasks ordered from earliest to latest"""
        # Arrange
        schedule = Schedule()
        owner = Owner("John Smith")
        pet = Pet("Fluffy", "Golden Retriever", 3, owner)

        late_task = Task("Evening Walk", time(18, 0), "Walk for 20 minutes", pet)
        early_task = Task("Breakfast", time(7, 30), "Serve dry food", pet)
        noon_task = Task("Lunch", time(12, 0), "Serve wet food", pet)

        # Act
        schedule.add_task(late_task)
        schedule.add_task(early_task)
        schedule.add_task(noon_task)
        sorted_tasks = schedule.get_tasks_sorted_by_time()

        # Assert
        assert sorted_tasks == [early_task, noon_task, late_task], "Tasks should be sorted by time"

    def test_filter_tasks_by_pet_and_status(self):
        """Verify filtering supports pet-level and completion-status queries"""
        # Arrange
        schedule = Schedule()
        owner = Owner("Alex")
        pet1 = Pet("Mochi", "Dog", 2, owner)
        pet2 = Pet("Nori", "Cat", 4, owner)

        task1 = Task("Walk", time(9, 0), "30 minute walk", pet1)
        task2 = Task("Feed", time(10, 0), "1 cup food", pet1)
        task3 = Task("Groom", time(11, 0), "Brush coat", pet2)

        schedule.add_task(task1)
        schedule.add_task(task2)
        schedule.add_task(task3)
        task1.mark_complete()

        # Act
        mochi_tasks = schedule.filter_tasks(pet=pet1)
        completed_tasks = schedule.filter_tasks(status="completed")
        pending_mochi_tasks = schedule.filter_tasks(pet=pet1, status="pending")

        # Assert
        assert mochi_tasks == [task1, task2], "Pet filter should only return that pet's tasks"
        assert completed_tasks == [task1], "Completed filter should only return completed tasks"
        assert pending_mochi_tasks == [task2], "Combined filter should apply both conditions"

    def test_filter_tasks_by_status_or_pet_name(self):
        """Verify filtering by pet name and status works independently and together"""
        # Arrange
        schedule = Schedule()
        owner = Owner("Taylor")
        pet1 = Pet("Mochi", "Dog", 2, owner)
        pet2 = Pet("Nori", "Cat", 4, owner)

        mochi_walk = Task("Walk", time(8, 0), "Morning walk", pet1)
        mochi_feed = Task("Feed", time(12, 0), "Lunch", pet1)
        nori_groom = Task("Groom", time(9, 0), "Brush coat", pet2)

        schedule.add_task(mochi_walk)
        schedule.add_task(mochi_feed)
        schedule.add_task(nori_groom)
        mochi_walk.mark_complete()

        # Act
        by_name = schedule.filter_tasks_by_status_or_pet_name(pet_name="mochi")
        by_status = schedule.filter_tasks_by_status_or_pet_name(status="completed")
        by_both = schedule.filter_tasks_by_status_or_pet_name(status="pending", pet_name="Mochi")

        # Assert
        assert by_name == [mochi_walk, mochi_feed], "Pet-name filter should match tasks for that pet"
        assert by_status == [mochi_walk], "Status filter should only include completed tasks"
        assert by_both == [mochi_feed], "Combined pet-name and status filters should both be applied"

    def test_recurring_task_queries(self):
        """Verify recurring task detection and day-based expansion"""
        # Arrange
        schedule = Schedule()
        owner = Owner("Jordan")
        pet = Pet("Buddy", "Labrador", 5, owner)

        daily_task = Task("Daily Feed", time(8, 0), "Feed daily", pet, frequency="daily")
        monday_task = Task("Training", time(15, 0), "Weekly class", pet, frequency="monday")
        weekly_tuesday_task = Task("Medication", time(9, 0), "Take meds", pet, frequency="weekly:tuesday")
        one_time_task = Task("Vet Visit", time(10, 0), "Annual checkup", pet, frequency="once")

        schedule.add_task(daily_task)
        schedule.add_task(monday_task)
        schedule.add_task(weekly_tuesday_task)
        schedule.add_task(one_time_task)

        # Act
        recurring_tasks = schedule.get_recurring_tasks()
        monday_plan = schedule.get_tasks_for_day("monday")
        tuesday_plan = schedule.get_tasks_for_day("tuesday")

        # Assert
        assert one_time_task not in recurring_tasks, "One-time tasks should not be recurring"
        assert daily_task in recurring_tasks, "Daily tasks should be recurring"
        assert monday_task in recurring_tasks, "Weekly-by-day tasks should be recurring"
        assert weekly_tuesday_task in recurring_tasks, "weekly:<day> tasks should be recurring"

        assert monday_plan == [daily_task, one_time_task, monday_task], "Monday plan should include daily, once, and monday tasks"
        assert tuesday_plan == [daily_task, weekly_tuesday_task, one_time_task], "Tuesday plan should include daily, weekly:tuesday, and once tasks"

    def test_same_time_different_pets_is_conflict(self):
        """Verify same-time tasks for different pets are detected as time-overlap conflicts"""
        # Arrange
        schedule = Schedule()
        owner = Owner("Riley")
        pet1 = Pet("Luna", "Husky", 3, owner)
        pet2 = Pet("Milo", "Beagle", 4, owner)

        task1 = Task("Walk Luna", time(9, 0), "Morning walk", pet1)
        task2 = Task("Feed Milo", time(9, 0), "Breakfast", pet2)

        # Act
        schedule.add_task(task1)
        schedule.add_task(task2)
        conflicts = schedule.check_conflicts()

        # Assert
        assert len(conflicts) == 1, "Different pets at same time should be flagged as a conflict"
        assert "TIME OVERLAP" in conflicts[0], "Conflict message should identify cross-pet overlap"
        assert "09:00" in conflicts[0], "Conflict message should include the overlapping time"

    def test_mark_daily_task_complete_creates_next_instance(self):
        """Verify completing a daily task auto-creates a new pending daily occurrence"""
        # Arrange
        schedule = Schedule()
        owner = Owner("Jamie")
        pet = Pet("Mochi", "Dog", 2, owner)
        daily_task = Task("Morning Feed", time(8, 0), "Feed kibble", pet, frequency="daily")
        schedule.add_task(daily_task)

        # Act
        schedule.mark_task_complete(daily_task)

        # Assert
        assert daily_task.is_completed() is True, "Original task should be completed"
        assert len(schedule.get_tasks_info()) == 2, "A new daily occurrence should be created"
        next_task = schedule.get_tasks_info()[1]
        assert next_task is not daily_task, "New occurrence should be a distinct task object"
        assert next_task.is_completed() is False, "New occurrence should start pending"
        assert next_task.get_description() == daily_task.get_description(), "New occurrence should copy task details"
        assert next_task.get_frequency() == "daily", "New occurrence should retain frequency"

    def test_mark_weekly_task_complete_creates_next_instance(self):
        """Verify completing a weekly task auto-creates a new pending weekly occurrence"""
        # Arrange
        schedule = Schedule()
        owner = Owner("Sam")
        pet = Pet("Nori", "Cat", 3, owner)
        weekly_task = Task("Brush Fur", time(18, 0), "Weekly grooming", pet, frequency="weekly")
        schedule.add_task(weekly_task)

        # Act
        schedule.mark_task_complete(weekly_task)

        # Assert
        assert len(schedule.get_tasks_info()) == 2, "A new weekly occurrence should be created"
        next_task = schedule.get_tasks_info()[1]
        assert next_task.get_frequency() == "weekly", "New occurrence should retain weekly frequency"
        assert next_task.is_completed() is False, "New weekly occurrence should be pending"

    def test_mark_once_task_complete_does_not_create_next_instance(self):
        """Verify non-recurring tasks do not auto-create another instance"""
        # Arrange
        schedule = Schedule()
        owner = Owner("Taylor")
        pet = Pet("Buddy", "Labrador", 4, owner)
        one_time_task = Task("Vet Visit", time(10, 0), "Annual check", pet, frequency="once")
        schedule.add_task(one_time_task)

        # Act
        schedule.mark_task_complete(one_time_task)

        # Assert
        assert one_time_task.is_completed() is True, "Original one-time task should be completed"
        assert len(schedule.get_tasks_info()) == 1, "No new occurrence should be created for one-time tasks"

    def test_marking_same_task_complete_twice_does_not_duplicate_occurrence(self):
        """Verify calling mark_task_complete twice does not create duplicate future tasks"""
        # Arrange
        schedule = Schedule()
        owner = Owner("Avery")
        pet = Pet("Luna", "Husky", 5, owner)
        daily_task = Task("Morning Walk", time(7, 0), "Walk 30 minutes", pet, frequency="daily")
        schedule.add_task(daily_task)

        # Act
        schedule.mark_task_complete(daily_task)
        schedule.mark_task_complete(daily_task)

        # Assert
        assert len(schedule.get_tasks_info()) == 2, "Repeated completion should not spawn extra occurrences"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
