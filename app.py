import streamlit as st
from pawpal_system import Owner, Pet, Task, Schedule
from datetime import time

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")


def task_rows(tasks):
    """Convert Task objects into table-ready dictionaries."""
    return [
        {
            "time": task.get_time().strftime("%H:%M"),
            "task": task.get_description(),
            "pet": task.get_pet().get_identifier(),
            "owner": task.get_pet().get_owner().get_name(),
            "frequency": task.get_frequency(),
            "status": "completed" if task.is_completed() else "pending",
        }
        for task in tasks
    ]

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")

# Persist the Owner object in session state so it survives reruns.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name)

# Persist the centralized schedule in session state.
if "schedule" not in st.session_state:
    st.session_state.schedule = Schedule()

# Keep the stored owner name in sync if the user edits the text input.
if st.session_state.owner.get_name() != owner_name:
    st.session_state.owner = Owner(owner_name)
    st.session_state.schedule = Schedule()

st.markdown("### Add a Pet")
st.caption("Submit this form to call Owner.add_pet(...) and persist pets for this owner.")

with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    pet_age = st.number_input("Pet age", min_value=0, max_value=40, value=2)
    add_pet_submitted = st.form_submit_button("Add pet")

if add_pet_submitted:
    existing_names = {pet.get_identifier().lower() for pet in st.session_state.owner.get_pets()}
    if pet_name.strip().lower() in existing_names:
        st.warning("A pet with that name already exists for this owner.")
    else:
        new_pet = Pet(
            identifier=pet_name.strip(),
            breed=species,
            age=int(pet_age),
            owner=st.session_state.owner,
        )
        st.session_state.owner.add_pet(new_pet)
        st.success(f"Added {new_pet.get_identifier()} to {st.session_state.owner.get_name()}.")

current_pets = st.session_state.owner.get_pets()
if current_pets:
    st.write("Current pets:")
    st.table(
        [
            {
                "name": pet.get_identifier(),
                "species": pet.get_breed(),
                "age": pet.get_age(),
                "tasks": len(pet.get_assigned_tasks()),
            }
            for pet in current_pets
        ]
    )
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.markdown("### Schedule a Task")
st.caption("Submit this form to create a Task and call Schedule.add_task(...).")

pet_options = [pet.get_identifier() for pet in st.session_state.owner.get_pets()]

if pet_options:
    with st.form("add_task_form"):
        selected_pet_name = st.selectbox("Assign to pet", pet_options)
        task_title = st.text_input("Task title", value="Morning walk")
        task_time = st.time_input("Task time", value=time(9, 0))
        task_instructions = st.text_input("Instructions", value="Walk for 20 minutes")
        task_frequency = st.selectbox("Frequency", ["daily", "weekly", "once"], index=0)
        add_task_submitted = st.form_submit_button("Schedule task")

    if add_task_submitted:
        selected_pet = next(
            pet for pet in st.session_state.owner.get_pets() if pet.get_identifier() == selected_pet_name
        )
        new_task = Task(
            description=task_title.strip(),
            time=task_time,
            instructions=task_instructions.strip(),
            pet=selected_pet,
            frequency=task_frequency,
        )
        st.session_state.schedule.add_task(new_task)
        st.success(f"Scheduled '{new_task.get_description()}' for {selected_pet.get_identifier()} at {task_time.strftime('%H:%M')}.")
else:
    st.info("Add at least one pet before scheduling tasks.")

st.divider()

st.subheader("Build Schedule")
st.caption("This now renders data directly from your Schedule object.")

if "show_schedule" not in st.session_state:
    st.session_state.show_schedule = False

if st.button("Generate schedule"):
    st.session_state.show_schedule = True

if st.session_state.show_schedule:
    schedule = st.session_state.schedule
    scheduled_tasks = schedule.get_tasks_sorted_by_time()

    if not scheduled_tasks:
        st.info("No scheduled tasks yet.")
    else:
        totals_col, completed_col, pending_col = st.columns(3)
        totals_col.metric("Total Tasks", len(schedule.get_tasks_info()))
        completed_col.metric("Completed", len(schedule.get_completed_tasks()))
        pending_col.metric("Pending", len(schedule.get_pending_tasks()))

        st.success("Showing tasks in chronological order.")
        st.write("Today's Schedule")
        st.table(task_rows(scheduled_tasks))

        filter_col1, filter_col2 = st.columns(2)
        pet_filter = filter_col1.selectbox("Filter by pet", ["All pets"] + pet_options)
        status_filter = filter_col2.selectbox("Filter by status", ["all", "pending", "completed"])

        filtered_tasks = schedule.filter_tasks_by_status_or_pet_name(
            status=None if status_filter == "all" else status_filter,
            pet_name=None if pet_filter == "All pets" else pet_filter,
        )
        filtered_tasks = sorted(filtered_tasks, key=lambda task: task.get_time())

        if filtered_tasks:
            st.table(task_rows(filtered_tasks))
            st.success(f"{len(filtered_tasks)} task(s) match your current filters.")
        else:
            st.warning("No tasks match the selected filters.")

        conflicts = schedule.check_conflicts()
        if conflicts:
            st.warning(f"Scheduling warning: {len(conflicts)} conflict(s) detected.")
            with st.expander("Review conflicts and quick fix tips", expanded=True):
                for idx, conflict in enumerate(conflicts, start=1):
                    st.write(f"{idx}. {conflict}")
                st.caption("Try moving one of the overlapping tasks by 15-30 minutes to avoid missed care steps.")
        else:
            st.success("No scheduling conflicts detected.")
