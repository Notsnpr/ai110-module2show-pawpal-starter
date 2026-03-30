from pawpal_system import Owner, Pet, Task, Schedule
from datetime import time


def print_schedule_header():
    """Print a formatted header for the schedule"""
    print("\n" + "=" * 70)
    print(" " * 20 + "TODAY'S SCHEDULE")
    print("=" * 70 + "\n")


def print_task_details(task, index):
    """Print details of a single task"""
    pet = task.get_pet()
    owner = pet.get_owner()
    status = "✓ COMPLETED" if task.is_completed() else "⏳ PENDING"
    
    print(f"{index}. [{status}] {task.get_time().strftime('%H:%M')} - {task.get_description()}")
    print(f"   Pet: {pet.get_identifier()} ({pet.get_breed()})")
    print(f"   Owner: {owner.get_name()}")
    print(f"   Instructions: {task.get_instructions()}")
    print(f"   Frequency: {task.get_frequency()}")
    print()


def main():
    # Create a centralized schedule
    schedule = Schedule()
    
    # Create owners
    owner1 = Owner("John Smith")
    owner2 = Owner("Sarah Johnson")
    
    # Create pets
    fluffy = Pet("Fluffy", "Golden Retriever", 3, owner1)
    max_the_cat = Pet("Max", "Tabby Cat", 5, owner1)
    buddy = Pet("Buddy", "Labrador", 2, owner2)
    
    # Add pets to owners
    owner1.add_pet(fluffy)
    owner1.add_pet(max_the_cat)
    owner2.add_pet(buddy)
    
    # Create tasks with different times
    # Fluffy's tasks
    task1 = Task(
        description="Morning Feeding",
        time=time(8, 0),
        instructions="Give 2 cups of dry food",
        pet=fluffy,
        frequency="daily"
    )
    
    task2 = Task(
        description="Afternoon Walk",
        time=time(14, 30),
        instructions="Walk for 30 minutes in the park",
        pet=fluffy,
        frequency="daily"
    )
    
    # Max's task
    task3 = Task(
        description="Feeding Time",
        time=time(9, 0),
        instructions="Give 1 can of wet food",
        pet=max_the_cat,
        frequency="daily"
    )
    
    # Buddy's tasks
    task4 = Task(
        description="Playtime",
        time=time(10, 0),
        instructions="Interactive play session for 20 minutes",
        pet=buddy,
        frequency="daily"
    )
    
    task5 = Task(
        description="Evening Feeding",
        time=time(18, 0),
        instructions="Give 3 cups of dry food",
        pet=buddy,
        frequency="daily"
    )
    
    # Add tasks to schedule
    schedule.add_task(task1)
    schedule.add_task(task2)
    schedule.add_task(task3)
    schedule.add_task(task4)
    schedule.add_task(task5)
    
    # Mark one task as completed
    task1.mark_complete()
    
    # Print today's schedule
    print_schedule_header()
    
    # Display all tasks sorted by time
    tasks_sorted = sorted(schedule.get_tasks_info(), key=lambda t: t.get_time())
    
    for i, task in enumerate(tasks_sorted, 1):
        print_task_details(task, i)
    
    # Print summary statistics
    print("=" * 70)
    print("SCHEDULE SUMMARY")
    print("=" * 70)
    print(f"Total Tasks Today: {len(schedule.get_tasks_info())}")
    print(f"Completed Tasks: {len(schedule.get_completed_tasks())}")
    print(f"Pending Tasks: {len(schedule.get_pending_tasks())}")
    print()
    
    # Check for conflicts
    conflicts = schedule.check_conflicts()
    if conflicts:
        print("⚠️  CONFLICTS DETECTED:")
        for conflict in conflicts:
            print(f"   {conflict}")
    else:
        print("✓ No scheduling conflicts detected!")
    print()
    
    # Print owner summaries
    print("=" * 70)
    print("OWNER SUMMARIES")
    print("=" * 70)
    for owner in [owner1, owner2]:
        print(f"\n{owner.get_name()}")
        print(f"  Pets: {owner.get_pets_count()}")
        for pet in owner.get_pets():
            tasks = schedule.get_tasks_by_pet(pet)
            print(f"    - {pet.get_identifier()} ({pet.get_breed()}): {len(tasks)} tasks")
        print(f"  Total tasks: {len(owner.get_all_tasks())}")
    
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    main()
