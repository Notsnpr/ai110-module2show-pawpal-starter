# PawPal+ Class Diagram

## Updated Design (Front Desk Centered)

```mermaid
classDiagram
    class Owner {
        -name: String
        -pets: List~Pet~
        +getName(): String
        +addPet(pet: Pet)
        +getPets(): List~Pet~
    }
    
    class Pet {
        -identifier: String
        -breed: String
        -age: Integer
        -owner: Owner
        -assigned_tasks: List~Task~
        +getIdentifier(): String
        +getBreed(): String
        +getAge(): Integer
        +getOwner(): Owner
        +getAssignedTasks(): List~Task~
        +addTask(task: Task)
    }
    
    class Task {
        -description: String
        -time: Time
        -instructions: String
        -pet: Pet
        +getDescription(): String
        +getTime(): Time
        +getInstructions(): String
        +getPet(): Pet
    }
    
    class Schedule {
        -tasks: List~Task~
        +addTask(task: Task)
        +getTasksInfo(): List~Task~
        +checkConflicts(): List~String~
        +modifyTask(task: Task, newTime: Time)
    }
    
    Owner "1" -- "*" Pet : owns
    Pet "1" -- "*" Task : has_assigned
    Task "*" -- "1" Pet : belongs_to
    Schedule "1" -- "*" Task : manages
```

## Key Relationships

- **Owner → Pet**: One owner can have multiple pets
- **Pet → Task**: Each pet has multiple assigned tasks
- **Task → Pet**: Each task belongs to exactly one pet (enables conflict detection)
- **Schedule → Task**: Centralized schedule manages all tasks across all owners/pets

## System User

The **Front Desk Person** operates this system:
1. Creates new owners
2. Adds pets to owners
3. Schedules tasks for pets
4. Checks the central schedule for conflicts
5. Resolves conflicting times
