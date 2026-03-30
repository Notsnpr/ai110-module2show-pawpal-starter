# PawPal+ Class Diagram

## Updated Design (Front Desk Centered)

```mermaid
classDiagram
    class Owner {
        -name: str
        -pets: List~Pet~
        +get_name(): str
        +add_pet(pet: Pet)
        +get_pets(): List~Pet~
        +get_all_tasks(): List~Task~
        +get_pets_count(): int
    }
    
    class Pet {
        -identifier: str
        -breed: str
        -age: int
        -owner: Owner
        -assigned_tasks: List~Task~
        +get_identifier(): str
        +get_breed(): str
        +get_age(): int
        +get_owner(): Owner
        +get_assigned_tasks(): List~Task~
        +add_task(task: Task)
        +get_completed_tasks(): List~Task~
        +get_pending_tasks(): List~Task~
    }
    
    class Task {
        -description: str
        -time: Time
        -instructions: str
        -pet: Pet
        -frequency: str = "daily"
        -completion_status: bool = False
        +get_description(): str
        +get_time(): Time
        +get_instructions(): str
        +get_pet(): Pet
        +get_frequency(): str
        +is_completed(): bool
        +mark_complete()
        +mark_incomplete()
    }
    
    class Schedule {
        -tasks: List~Task~
        +add_task(task: Task)
        +get_tasks_info(): List~Task~
        +get_tasks_sorted_by_time(): List~Task~
        +get_tasks_by_pet(pet: Pet): List~Task~
        +get_tasks_by_owner(owner: Owner): List~Task~
        +get_tasks_by_time(target_time: Time): List~Task~
        +filter_tasks(pet: Pet=None, status: str=None): List~Task~
        +filter_tasks_by_status_or_pet_name(status: str=None, pet_name: str=None): List~Task~
        +get_recurring_tasks(): List~Task~
        +get_tasks_for_day(day_name: str): List~Task~
        +check_conflicts(): List~str~
        +modify_task(task: Task, new_time: Time)
        +get_pending_tasks(): List~Task~
        +get_completed_tasks(): List~Task~
        +get_daily_tasks(): List~Task~
        +mark_task_complete(task: Task)
        +remove_task(task: Task)

        -_filter_tasks_core(status: str=None, pet_name: str=None): List~Task~
        -_normalize_status(status: str=None): str
        -_find_conflicting_task_pairs(): List~Tuple~Task, Task~~
        -_group_tasks_by_time(): Dict~Time, List~Task~~
        -_is_auto_recurring_frequency(frequency: str): bool
        -_create_next_occurrence(task: Task): Task
    }
    
    Owner "1" -- "*" Pet : owns
    Pet "1" -- "*" Task : assigned_tasks
    Task "*" -- "1" Pet : belongs_to
    Schedule "1" -- "*" Task : manages
```

## Key Relationships

- **Owner → Pet**: One owner can have multiple pets
- **Pet → Task**: Each pet has multiple assigned tasks
- **Task → Pet**: Each task belongs to exactly one pet (enables conflict detection)
- **Schedule → Task**: Centralized schedule manages all tasks across all owners/pets
- **Schedule.add_task(...) side effect**: adding to Schedule also adds the same task to Pet.assigned_tasks
- **Schedule.mark_task_complete(...) behavior**: recurring daily/weekly tasks auto-create the next pending occurrence

## System User

The **Front Desk Person** operates this system:
1. Creates new owners
2. Adds pets to owners
3. Schedules tasks for pets
4. Checks the central schedule for conflicts
5. Resolves conflicting times
