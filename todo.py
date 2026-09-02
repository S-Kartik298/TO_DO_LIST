import tkinter
from tkinter import messagebox
import json


# ==================================================
# FILE NAME
# ==================================================

FILE_NAME = "tasks.json"


# ==================================================
# MAIN WINDOW
# ==================================================

window = tkinter.Tk()

window.title("My To-Do List")
window.geometry("650x750")


# ==================================================
# TASK DATA
# ==================================================

tasks = []


# ==================================================
# SAVE TASKS TO JSON
# ==================================================

def save_tasks():

    file = open(FILE_NAME, "w")

    json.dump(tasks, file, indent=4)

    file.close()


# ==================================================
# LOAD TASKS FROM JSON
# ==================================================

def load_tasks():

    global tasks

    try:

        file = open(FILE_NAME, "r")

        tasks = json.load(file)

        file.close()

    except FileNotFoundError:

        tasks = []

    refresh_list()


# ==================================================
# DISPLAY TASKS
# ==================================================

def refresh_list():

    task_list.delete(0, tkinter.END)

    search_text = search_entry.get().lower()

    number = 1

    for task in tasks:

        # Search task
        if search_text in task["task"].lower():

            status = ""

            if task["completed"]:
                status = "✓ "

            text = (
                str(number)
                + ". "
                + status
                + task["task"]
                + " | Priority: "
                + task["priority"]
                + " | Due: "
                + task["due_date"]
                + " | "
                + task["category"]
            )

            task_list.insert(tkinter.END, text)

            number = number + 1

    update_counter()


# ==================================================
# ADD TASK
# ==================================================

def add_task():

    task_name = task_entry.get().strip()

    priority = priority_var.get()

    due_date = date_entry.get().strip()

    category = category_var.get()


    if task_name == "":

        messagebox.showwarning(
            "Warning",
            "Please enter a task."
        )

        return


    new_task = {

        "task": task_name,

        "completed": False,

        "priority": priority,

        "due_date": due_date,

        "category": category

    }


    tasks.append(new_task)

    save_tasks()

    task_entry.delete(0, tkinter.END)

    date_entry.delete(0, tkinter.END)

    refresh_list()


# ==================================================
# GET SELECTED TASK
# ==================================================

def get_selected_task():

    selected = task_list.curselection()

    if not selected:

        messagebox.showwarning(
            "Warning",
            "Please select a task first."
        )

        return None


    search_text = search_entry.get().lower()

    visible_tasks = []


    for task in tasks:

        if search_text in task["task"].lower():

            visible_tasks.append(task)


    return visible_tasks[selected[0]]


# ==================================================
# COMPLETE TASK
# ==================================================

def complete_task():

    task = get_selected_task()

    if task is not None:

        task["completed"] = True

        save_tasks()

        refresh_list()


# ==================================================
# DELETE TASK
# ==================================================

def delete_task():

    task = get_selected_task()

    if task is not None:

        tasks.remove(task)

        save_tasks()

        refresh_list()


# ==================================================
# EDIT TASK
# ==================================================

def edit_task():

    task = get_selected_task()

    if task is not None:

        task_entry.delete(0, tkinter.END)

        task_entry.insert(
            0,
            task["task"]
        )


        date_entry.delete(0, tkinter.END)

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

        refresh_list()


# ==================================================
# CLEAR ALL
# ==================================================

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

        refresh_list()


# ==================================================
# UPDATE PROGRESS
# ==================================================

def update_counter():

    total = len(tasks)

    completed = 0


    for task in tasks:

        if task["completed"]:

            completed = completed + 1


    counter_label.config(

        text="Progress: "
        + str(completed)
        + "/"
        + str(total)
        + " tasks completed"

    )


# ==================================================
# SEARCH TASKS
# ==================================================

def search_tasks():

    refresh_list()


# ==================================================
# CLEAR SEARCH
# ==================================================

def clear_search():

    search_entry.delete(0, tkinter.END)

    refresh_list()


# ==================================================
# HEADING
# ==================================================

heading = tkinter.Label(

    window,

    text="MY TO-DO LIST",

    font=("Arial", 24, "bold")

)

heading.pack(pady=15)


# ==================================================
# TASK ENTRY
# ==================================================

instruction = tkinter.Label(

    window,

    text="Enter your task:"

)

instruction.pack()


task_entry = tkinter.Entry(

    window,

    width=50

)

task_entry.pack(pady=5)


# ==================================================
# PRIORITY
# ==================================================

priority_label = tkinter.Label(

    window,

    text="Priority:"

)

priority_label.pack()


priority_var = tkinter.StringVar()

priority_var.set("Medium")


priority_menu = tkinter.OptionMenu(

    window,

    priority_var,

    "High",
    "Medium",
    "Low"

)

priority_menu.pack(pady=5)


# ==================================================
# DUE DATE
# ==================================================

date_label = tkinter.Label(

    window,

    text="Due Date (DD-MM-YYYY):"

)

date_label.pack()


date_entry = tkinter.Entry(

    window,

    width=30

)

date_entry.pack(pady=5)


# ==================================================
# CATEGORY
# ==================================================

category_label = tkinter.Label(

    window,

    text="Category:"

)

category_label.pack()


category_var = tkinter.StringVar()

category_var.set("College")


category_menu = tkinter.OptionMenu(

    window,

    category_var,

    "College",
    "Personal",
    "Work",
    "Other"

)

category_menu.pack(pady=5)


# ==================================================
# ADD BUTTON
# ==================================================

add_button = tkinter.Button(

    window,

    text="ADD TASK",

    width=20,

    command=add_task

)

add_button.pack(pady=8)


# ==================================================
# SEARCH
# ==================================================

search_label = tkinter.Label(

    window,

    text="Search Task:"

)

search_label.pack(pady=5)


search_entry = tkinter.Entry(

    window,

    width=40

)

search_entry.pack()


search_button = tkinter.Button(

    window,

    text="SEARCH",

    width=15,

    command=search_tasks

)

search_button.pack(pady=5)


clear_search_button = tkinter.Button(

    window,

    text="CLEAR SEARCH",

    width=15,

    command=clear_search

)

clear_search_button.pack(pady=3)


# ==================================================
# TASK LIST
# ==================================================

task_list = tkinter.Listbox(

    window,

    width=85,

    height=12

)

task_list.pack(pady=15)


# ==================================================
# BUTTON FRAME
# ==================================================

button_frame = tkinter.Frame(window)

button_frame.pack()


# COMPLETE

complete_button = tkinter.Button(

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


# EDIT

edit_button = tkinter.Button(

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


# DELETE

delete_button = tkinter.Button(

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


# CLEAR ALL

clear_button = tkinter.Button(

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


# ==================================================
# PROGRESS
# ==================================================

counter_label = tkinter.Label(

    window,

    text="Progress: 0/0 tasks completed",

    font=("Arial", 13, "bold")

)

counter_label.pack(pady=15)


# ==================================================
# LOAD EXISTING TASKS
# ==================================================

load_tasks()


# ==================================================
# START APPLICATION
# ==================================================

window.mainloop()