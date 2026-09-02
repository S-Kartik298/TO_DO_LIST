import tkinter
import json

window = tkinter.Tk()

window.title("My To-Do List")
window.geometry("500x600")


def save_tasks():

    tasks = []

    for i in range(task_list.size()):
        task = task_list.get(i)
        tasks.append(task)

    file = open("tasks.json", "w")

    json.dump(tasks, file, indent=4)

    file.close()


def load_tasks():

    try:

        file = open("tasks.json", "r")

        tasks = json.load(file)

        file.close()

        for task in tasks:
            task_list.insert(tkinter.END, task)

    except FileNotFoundError:

        pass

    update_counter()


def add_task():

    task = task_entry.get()

    if task != "":

        task_list.insert(tkinter.END, task)

        task_entry.delete(0, tkinter.END)

        update_counter()

        save_tasks()


def delete_task():

    selected_task = task_list.curselection()

    if selected_task:

        task_list.delete(selected_task)

        update_counter()

        save_tasks()


def complete_task():

    selected_task = task_list.curselection()

    if selected_task:

        task = task_list.get(selected_task)

        if not task.startswith("✓ "):

            task_list.delete(selected_task)

            task_list.insert(selected_task, "✓ " + task)

        update_counter()

        save_tasks()


def edit_task():

    selected_task = task_list.curselection()

    if selected_task:

        task = task_list.get(selected_task)

        if task.startswith("✓ "):
            task = task[2:]

        task_entry.delete(0, tkinter.END)

        task_entry.insert(0, task)

        task_list.delete(selected_task)

        update_counter()

        save_tasks()


def clear_all():

    task_list.delete(0, tkinter.END)

    update_counter()

    save_tasks()


def update_counter():

    total_tasks = task_list.size()

    completed_tasks = 0

    for i in range(total_tasks):

        task = task_list.get(i)

        if task.startswith("✓ "):
            completed_tasks = completed_tasks + 1

    remaining_tasks = total_tasks - completed_tasks

    counter_label.config(
        text="Tasks remaining: " + str(remaining_tasks)
    )


heading = tkinter.Label(
    window,
    text="MY TO-DO LIST",
    font=("Arial", 20, "bold")
)

heading.pack(pady=20)


instruction = tkinter.Label(
    window,
    text="Enter your task:"
)

instruction.pack()


task_entry = tkinter.Entry(
    window,
    width=40
)

task_entry.pack(pady=10)


add_button = tkinter.Button(
    window,
    text="ADD TASK",
    width=20,
    command=add_task
)

add_button.pack(pady=5)


task_list = tkinter.Listbox(
    window,
    width=45,
    height=15
)

task_list.pack(pady=15)


complete_button = tkinter.Button(
    window,
    text="COMPLETE TASK",
    width=20,
    command=complete_task
)

complete_button.pack(pady=3)


edit_button = tkinter.Button(
    window,
    text="EDIT TASK",
    width=20,
    command=edit_task
)

edit_button.pack(pady=3)


delete_button = tkinter.Button(
    window,
    text="DELETE TASK",
    width=20,
    command=delete_task
)

delete_button.pack(pady=3)


clear_button = tkinter.Button(
    window,
    text="CLEAR ALL",
    width=20,
    command=clear_all
)

clear_button.pack(pady=3)


counter_label = tkinter.Label(
    window,
    text="Tasks remaining: 0"
)

counter_label.pack(pady=10)


load_tasks()

window.mainloop()
