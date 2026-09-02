
import tkinter
import json


# -----------------------------
# CREATE MAIN WINDOW
# -----------------------------

window = tkinter.Tk()

window.title("My To-Do List")
window.geometry("550x650")


# -----------------------------
# FUNCTION TO SAVE TASKS
# -----------------------------

def save_tasks():

    tasks = []

    for i in range(task_list.size()):

        task = task_list.get(i)

        # Remove numbering before saving
        if ". " in task:
            task = task.split(". ", 1)[1]

        # Check whether task is completed
        completed = False

        if task.startswith("✓ "):
            completed = True
            task = task[2:]

        tasks.append({
            "task": task,
            "completed": completed
        })

    file = open("tasks.json", "w")

    json.dump(tasks, file, indent=4)

    file.close()


# -----------------------------
# FUNCTION TO LOAD TASKS
# -----------------------------

def load_tasks():

    try:

        file = open("tasks.json", "r")

        tasks = json.load(file)

        file.close()

        for item in tasks:

            # New JSON format
            if isinstance(item, dict):

                task = item["task"]
                completed = item["completed"]

                if completed:
                    task = "✓ " + task

            # Old format support
            else:

                task = item

            task_list.insert(tkinter.END, task)

    except FileNotFoundError:

        pass

    update_task_numbers()
    update_counter()


# -----------------------------
# FUNCTION TO ADD TASK
# -----------------------------

def add_task():

    task = task_entry.get()

    if task != "":

        task_list.insert(tkinter.END, task)

        task_entry.delete(0, tkinter.END)

        update_task_numbers()
        update_counter()

        save_tasks()


# -----------------------------
# FUNCTION TO DELETE TASK
# -----------------------------

def delete_task():

    selected_task = task_list.curselection()

    if selected_task:

        task_list.delete(selected_task)

        update_task_numbers()
        update_counter()

        save_tasks()


# -----------------------------
# FUNCTION TO COMPLETE TASK
# -----------------------------

def complete_task():

    selected_task = task_list.curselection()

    if selected_task:

        task = task_list.get(selected_task)

        # Remove number
        if ". " in task:
            task = task.split(". ", 1)[1]

        # Add check mark
        if not task.startswith("✓ "):

            task = "✓ " + task

            task_list.delete(selected_task)

            task_list.insert(selected_task, task)

        update_task_numbers()
        update_counter()

        save_tasks()


# -----------------------------
# FUNCTION TO EDIT TASK
# -----------------------------

def edit_task():

    selected_task = task_list.curselection()

    if selected_task:

        task = task_list.get(selected_task)

        # Remove number
        if ". " in task:
            task = task.split(". ", 1)[1]

        # Remove check mark
        if task.startswith("✓ "):
            task = task[2:]

        task_entry.delete(0, tkinter.END)

        task_entry.insert(0, task)

        task_list.delete(selected_task)

        update_task_numbers()
        update_counter()

        save_tasks()


# -----------------------------
# FUNCTION TO CLEAR ALL TASKS
# -----------------------------

def clear_all():

    task_list.delete(0, tkinter.END)

    update_task_numbers()
    update_counter()

    save_tasks()


# -----------------------------
# FUNCTION TO NUMBER TASKS
# -----------------------------

def update_task_numbers():

    tasks = []

    for i in range(task_list.size()):

        task = task_list.get(i)

        # Remove old number
        if ". " in task:
            task = task.split(". ", 1)[1]

        tasks.append(task)

    # Clear the list
    task_list.delete(0, tkinter.END)

    # Add tasks again with new numbers
    for i in range(len(tasks)):

        number = i + 1

        task_list.insert(
            tkinter.END,
            str(number) + ". " + tasks[i]
        )


# -----------------------------
# FUNCTION TO UPDATE PROGRESS
# -----------------------------

def update_counter():

    total_tasks = task_list.size()

    completed_tasks = 0

    for i in range(total_tasks):

        task = task_list.get(i)

        if "✓ " in task:

            completed_tasks = completed_tasks + 1

    counter_label.config(
        text="Progress: "
        + str(completed_tasks)
        + "/"
        + str(total_tasks)
        + " tasks completed"
    )


# -----------------------------
# HEADING
# -----------------------------

heading = tkinter.Label(
    window,
    text="MY TO-DO LIST",
    font=("Arial", 22, "bold")
)

heading.pack(pady=20)


# -----------------------------
# INSTRUCTION
# -----------------------------

instruction = tkinter.Label(
    window,
    text="Enter your task:"
)

instruction.pack()


# -----------------------------
# TEXT ENTRY BOX
# -----------------------------

task_entry = tkinter.Entry(
    window,
    width=45
)

task_entry.pack(pady=10)


# -----------------------------
# ADD BUTTON
# -----------------------------

add_button = tkinter.Button(
    window,
    text="ADD TASK",
    width=20,
    command=add_task
)

add_button.pack(pady=5)


# -----------------------------
# TASK LIST
# -----------------------------

task_list = tkinter.Listbox(
    window,
    width=50,
    height=15
)

task_list.pack(pady=15)


# -----------------------------
# COMPLETE BUTTON
# -----------------------------

complete_button = tkinter.Button(
    window,
    text="COMPLETE TASK",
    width=20,
    command=complete_task
)

complete_button.pack(pady=3)


# -----------------------------
# EDIT BUTTON
# -----------------------------

edit_button = tkinter.Button(
    window,
    text="EDIT TASK",
    width=20,
    command=edit_task
)

edit_button.pack(pady=3)


# -----------------------------
# DELETE BUTTON
# -----------------------------

delete_button = tkinter.Button(
    window,
    text="DELETE TASK",
    width=20,
    command=delete_task
)

delete_button.pack(pady=3)


# -----------------------------
# CLEAR ALL BUTTON
# -----------------------------

clear_button = tkinter.Button(
    window,
    text="CLEAR ALL",
    width=20,
    command=clear_all
)

clear_button.pack(pady=3)


# -----------------------------
# PROGRESS STATUS
# -----------------------------

counter_label = tkinter.Label(
    window,
    text="Progress: 0/0 tasks completed",
    font=("Arial", 12, "bold")
)

counter_label.pack(pady=15)


# -----------------------------
# LOAD SAVED TASKS
# -----------------------------

load_tasks()


# -----------------------------
# START APPLICATION
# -----------------------------

window.mainloop()
```
