import tkinter as tk
from tkinter import messagebox
import json


# ==========================================
# FILE WHERE TASKS ARE STORED
# ==========================================

FILE_NAME = "tasks.json"


# ==========================================
# MAIN WINDOW
# ==========================================

window = tk.Tk()

window.title("My To-Do List")
window.geometry("700x750")

window.resizable(False, False)


# ==========================================
# TASK LIST
# ==========================================

tasks = []


# ==========================================
# SAVE TASKS
# ==========================================

def save_tasks():

    try:

        with open(FILE_NAME, "w") as file:

            json.dump(tasks, file, indent=4)

    except Exception as error:

        messagebox.showerror(
            "Error",
            "Could not save tasks.\n" + str(error)
        )


# ==========================================
# LOAD TASKS
# ==========================================

def load_tasks():

    global tasks

    try:

        with open(FILE_NAME, "r") as file:

            data = json.load(file)


        # Make sure the JSON contains a list
        if not isinstance(data, list):

            tasks = []

            return


        tasks = []


        # Read every item
        for item in data:

            # --------------------------------
            # NEW FORMAT
            # --------------------------------

            if isinstance(item, dict):

                task = {

                    "task": str(
                        item.get("task", "")
                    ),

                    "completed": bool(
                        item.get("completed", False)
                    ),

                    "priority": str(
                        item.get("priority", "Medium")
                    ),

                    "due_date": str(
                        item.get("due_date", "")
                    ),

                    "category": str(
                        item.get("category", "College")
                    )

                }


                # Make sure priority is valid

                if task["priority"] not in [
                    "High",
                    "Medium",
                    "Low"
                ]:

                    task["priority"] = "Medium"


                # Make sure category is valid

                if task["category"] not in [
                    "College",
                    "Personal",
                    "Work",
                    "Other"
                ]:

                    task["category"] = "Other"


                tasks.append(task)


            # --------------------------------
            # OLD FORMAT
            # --------------------------------

            elif isinstance(item, str):

                task_text = item

                completed = False


                # Old completed task

                if task_text.startswith("✓ "):

                    completed = True

                    task_text = task_text[2:]


                # Remove old numbering

                if ". " in task_text:

                    first_part = task_text.split(
                        ". ",
                        1
                    )

                    if first_part[0].isdigit():

                        task_text = first_part[1]


                task = {

                    "task": task_text,

                    "completed": completed,

                    "priority": "Medium",

                    "due_date": "",

                    "category": "College"

                }


                tasks.append(task)


    except FileNotFoundError:

        # First time running the program
        tasks = []


    except json.JSONDecodeError:

        # If JSON file is damaged
        tasks = []


    except Exception as error:

        messagebox.showerror(
            "Error",
            "Could not load tasks.\n" + str(error)
        )

        tasks = []


# ==========================================
# DISPLAY TASKS
# ==========================================

def refresh_tasks():

    task_list.delete(
        0,
        tk.END
    )


    search_text = search_entry.get().lower()


    visible_tasks.clear()


    number = 1


    for task in tasks:

        # Search
        if search_text in task["task"].lower():

            visible_tasks.append(task)


            # Completion symbol

            if task["completed"]:

                status = "✓ "

            else:

                status = ""


            # Display text

            display_text = (

                str(number)
                + ". "
                + status
                + task["task"]
                + " | "
                + task["priority"]
                + " | Due: "
                + (
                    task["due_date"]
                    if task["due_date"]
                    else "No date"
                )
                + " | "
                + task["category"]

            )


            task_list.insert(
                tk.END,
                display_text
            )


            number += 1


    update_progress()


# ==========================================
# ADD TASK
# ==========================================

def add_task():

    task_name = task_entry.get().strip()

    priority = priority_var.get()

    due_date = date_entry.get().strip()

    category = category_var.get()


    # Check empty task

    if task_name == "":

        messagebox.showwarning(
            "Warning",
            "Please enter a task."
        )

        return


    # Create task

    new_task = {

        "task": task_name,

        "completed": False,

        "priority": priority,

        "due_date": due_date,

        "category": category

    }


    # Add to list

    tasks.append(new_task)


    # Save

    save_tasks()


    # Clear input boxes

    task_entry.delete(
        0,
        tk.END
    )

    date_entry.delete(
        0,
        tk.END
    )


    # Refresh display

    refresh_tasks()


# ==========================================
# GET SELECTED TASK
# ==========================================

def get_selected_task():

    selected = task_list.curselection()


    if not selected:

        messagebox.showwarning(
            "Warning",
            "Please select a task first."
        )

        return None


    position = selected[0]


    if position >= len(visible_tasks):

        return None


    return visible_tasks[position]


# ==========================================
# COMPLETE TASK
# ==========================================

def complete_task():

    task = get_selected_task()


    if task is not None:

        task["completed"] = not task["completed"]


        save_tasks()

        refresh_tasks()


# ==========================================
# DELETE TASK
# ==========================================

def delete_task():

    task = get_selected_task()


    if task is not None:

        answer = messagebox.askyesno(

            "Delete Task",

            "Are you sure you want to delete this task?"

        )


        if answer:

            tasks.remove(task)

            save_tasks()

            refresh_tasks()


# ==========================================
# EDIT TASK
# ==========================================

def edit_task():

    task = get_selected_task()


    if task is None:

        return


    # Put existing information into input boxes

    task_entry.delete(
        0,
        tk.END
    )

    task_entry.insert(
        0,
        task["task"]
    )


    date_entry.delete(
        0,
        tk.END
    )

    date_entry.insert(
        0,
        task["due_date"]
    )


    priority_var.set(
        task["priority"]
    )


    category_var.set(
        task["category"]
    )


    # Remove old task

    tasks.remove(task)


    save_tasks()

    refresh_tasks()


# ==========================================
# CLEAR ALL TASKS
# ==========================================

def clear_all():

    if len(tasks) == 0:

        return


    answer = messagebox.askyesno(

        "Clear All",

        "Are you sure you want to delete all tasks?"

    )


    if answer:

        tasks.clear()

        save_tasks()

        refresh_tasks()


# ==========================================
# UPDATE PROGRESS
# ==========================================

def update_progress():

    total = len(tasks)

    completed = 0


    for task in tasks:

        if task["completed"]:

            completed += 1


    progress_label.config(

        text="Progress: "
        + str(completed)
        + "/"
        + str(total)
        + " tasks completed"

    )


# ==========================================
# SEARCH TASKS
# ==========================================

def search_tasks():

    refresh_tasks()


# ==========================================
# CLEAR SEARCH
# ==========================================

def clear_search():

    search_entry.delete(
        0,
        tk.END
    )

    refresh_tasks()


# ==========================================
# SAVE BEFORE CLOSING
# ==========================================

def close_application():

    save_tasks()

    window.destroy()


# ==========================================
# HEADING
# ==========================================

heading = tk.Label(

    window,

    text="MY TO-DO LIST",

    font=(
        "Arial",
        24,
        "bold"
    )

)

heading.pack(
    pady=15
)


# ==========================================
# TASK INPUT
# ==========================================

task_label = tk.Label(

    window,

    text="Enter your task:"

)

task_label.pack()


task_entry = tk.Entry(

    window,

    width=55

)

task_entry.pack(
    pady=5
)


# ==========================================
# PRIORITY
# ==========================================

priority_label = tk.Label(

    window,

    text="Priority:"

)

priority_label.pack()


priority_var = tk.StringVar()

priority_var.set(
    "Medium"
)


priority_menu = tk.OptionMenu(

    window,

    priority_var,

    "High",
    "Medium",
    "Low"

)

priority_menu.pack(
    pady=3
)


# ==========================================
# DUE DATE
# ==========================================

date_label = tk.Label(

    window,

    text="Due Date (DD-MM-YYYY):"

)

date_label.pack()


date_entry = tk.Entry(

    window,

    width=30

)

date_entry.pack(
    pady=3
)


# ==========================================
# CATEGORY
# ==========================================

category_label = tk.Label(

    window,

    text="Category:"

)

category_label.pack()


category_var = tk.StringVar()

category_var.set(
    "College"
)


category_menu = tk.OptionMenu(

    window,

    category_var,

    "College",
    "Personal",
    "Work",
    "Other"

)

category_menu.pack(
    pady=3
)


# ==========================================
# ADD BUTTON
# ==========================================

add_button = tk.Button(

    window,

    text="ADD TASK",

    width=25,

    command=add_task

)

add_button.pack(
    pady=8
)


# ==========================================
# SEARCH
# ==========================================

search_label = tk.Label(

    window,

    text="Search Task:"

)

search_label.pack()


search_entry = tk.Entry(

    window,

    width=45

)

search_entry.pack(
    pady=3
)


search_button = tk.Button(

    window,

    text="SEARCH",

    width=15,

    command=search_tasks

)

search_button.pack(
    pady=3
)


clear_search_button = tk.Button(

    window,

    text="CLEAR SEARCH",

    width=15,

    command=clear_search

)

clear_search_button.pack(
    pady=3
)


# ==========================================
# TASK LIST
# ==========================================

task_list = tk.Listbox(

    window,

    width=90,

    height=12,

    font=(
        "Arial",
        10
    )

)

task_list.pack(
    pady=12
)


# This stores the tasks currently visible
# after searching

visible_tasks = []


# ==========================================
# BUTTON FRAME
# ==========================================

button_frame = tk.Frame(
    window
)

button_frame.pack()


# ==========================================
# COMPLETE BUTTON
# ==========================================

complete_button = tk.Button(

    button_frame,

    text="COMPLETE",

    width=15,

    command=complete_task

)

complete_button.grid(

    row=0,

    column=0,

    padx=5,

    pady=5

)


# ==========================================
# EDIT BUTTON
# ==========================================

edit_button = tk.Button(

    button_frame,

    text="EDIT",

    width=15,

    command=edit_task

)

edit_button.grid(

    row=0,

    column=1,

    padx=5,

    pady=5

)


# ==========================================
# DELETE BUTTON
# ==========================================

delete_button = tk.Button(

    button_frame,

    text="DELETE",

    width=15,

    command=delete_task

)

delete_button.grid(

    row=1,

    column=0,

    padx=5,

    pady=5

)


# ==========================================
# CLEAR ALL BUTTON
# ==========================================

clear_button = tk.Button(

    button_frame,

    text="CLEAR ALL",

    width=15,

    command=clear_all

)

clear_button.grid(

    row=1,

    column=1,

    padx=5,

    pady=5

)


# ==========================================
# PROGRESS
# ==========================================

progress_label = tk.Label(

    window,

    text="Progress: 0/0 tasks completed",

    font=(
        "Arial",
        13,
        "bold"
    )

)

progress_label.pack(
    pady=12
)


# ==========================================
# LOAD SAVED DATA
# ==========================================

load_tasks()


# ==========================================
# SHOW TASKS
# ==========================================

refresh_tasks()


# ==========================================
# SAVE WHEN WINDOW IS CLOSED
# ==========================================

window.protocol(
    "WM_DELETE_WINDOW",
    close_application
)


# ==========================================
# START PROGRAM
# ==========================================

window.mainloop()