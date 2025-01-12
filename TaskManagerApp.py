import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import simpledialog
from tkcalendar import Calendar
from datetime import datetime, timedelta
import sqlite3
import threading

# Database setup
def setup_database():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            deadline TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# Add a task to the database
def add_task(title, description, deadline):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, description, deadline) VALUES (?, ?, ?)", (title, description, deadline))
    conn.commit()
    conn.close()

# Fetch all tasks from the database
def fetch_tasks():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

# Mark a task as completed
def mark_task_completed(task_id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

# Delete a task from the database
def delete_task(task_id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

# GUI setup
class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")

        # Title
        self.title_label = tk.Label(root, text="Task Title:")
        self.title_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.title_entry = tk.Entry(root, width=30)
        self.title_entry.grid(row=0, column=1, padx=10, pady=5)

        # Description
        self.desc_label = tk.Label(root, text="Description:")
        self.desc_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.desc_entry = tk.Entry(root, width=30)
        self.desc_entry.grid(row=1, column=1, padx=10, pady=5)

        # Deadline
        self.deadline_label = tk.Label(root, text="Deadline:")
        self.deadline_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.deadline_button = tk.Button(root, text="Select Date & Time", command=self.select_deadline)
        self.deadline_button.grid(row=2, column=1, padx=10, pady=5)

        # Add Task Button
        self.add_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Task List
        self.task_tree = ttk.Treeview(root, columns=("ID", "Title", "Description", "Deadline", "Completed"), show="headings")
        self.task_tree.heading("ID", text="ID")
        self.task_tree.heading("Title", text="Title")
        self.task_tree.heading("Description", text="Description")
        self.task_tree.heading("Deadline", text="Deadline")
        self.task_tree.heading("Completed", text="Completed")
        self.task_tree.column("ID", width=30)
        self.task_tree.column("Title", width=150)
        self.task_tree.column("Description", width=200)
        self.task_tree.column("Deadline", width=150)
        self.task_tree.column("Completed", width=80)
        self.task_tree.grid(row=4, column=0, columnspan=2, pady=10)

        # Buttons for Task Actions
        self.complete_button = tk.Button(root, text="Mark Completed", command=self.mark_completed)
        self.complete_button.grid(row=5, column=0, pady=5)
        self.delete_button = tk.Button(root, text="Delete Task", command=self.delete_task)
        self.delete_button.grid(row=5, column=1, pady=5)

        # Developer Credit
        self.credit_label = tk.Label(root, text="Developed by Ripon R. Rahman", font=("Arial", 10, "italic"))
        self.credit_label.grid(row=6, column=0, columnspan=2, pady=10)

        self.selected_deadline = None
        self.load_tasks()
        threading.Thread(target=self.reminder_checker, daemon=True).start()

    def select_deadline(self):
        # Create a popup window for selecting date and time
        self.popup = tk.Toplevel(self.root)
        self.popup.title("Select Deadline")

        # Calendar widget
        self.calendar = Calendar(self.popup, selectmode='day')
        self.calendar.pack(pady=10)

        # Time selection
        self.time_label = tk.Label(self.popup, text="Select Time:")
        self.time_label.pack()
        # Create a Combobox with time slots
        self.time_combobox = ttk.Combobox(self.popup, values=[f"{h:02d}:{m:02d}" for h in range(24) for m in range(0, 60, 15)])
        self.time_combobox.set("12:00")  # Default time
        self.time_combobox.pack(pady=5)

        # Confirm button
        self.confirm_button = tk.Button(self.popup, text="Confirm", command=self.confirm_deadline)
        self.confirm_button.pack(pady=10)

    def confirm_deadline(self):
        # Get selected date and time
        date = self.calendar.get_date()
        time = self.time_combobox.get()

        # Ensure time is in the correct format (HH:MM)
        try:
            # Check if the time matches the expected format (HH:MM)
            datetime.strptime(time, "%H:%M")
            
            # Combine date and time into one string
            self.selected_deadline = f"{date} {time}"
            self.popup.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid time format! Use HH:MM")

    def add_task(self):
        title = self.title_entry.get()
        description = self.desc_entry.get()
        deadline = self.selected_deadline

        if not title or not deadline:
            messagebox.showerror("Error", "Title and Deadline are required!")
            return

        add_task(title, description, deadline)
        self.load_tasks()
        self.title_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.selected_deadline = None

    def load_tasks(self):
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)

        tasks = fetch_tasks()
        for task in tasks:
            self.task_tree.insert("", "end", values=(task[0], task[1], task[2], task[3], "Yes" if task[4] else "No"))

    def mark_completed(self):
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No task selected!")
            return

        task_id = self.task_tree.item(selected_item, "values")[0]
        mark_task_completed(task_id)
        self.load_tasks()

    def delete_task(self):
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No task selected!")
            return

        task_id = self.task_tree.item(selected_item, "values")[0]
        delete_task(task_id)
        self.load_tasks()

    def reminder_checker(self):
        while True:
            tasks = fetch_tasks()
            for task in tasks:
                if not task[4]:  # If not completed
                    deadline = datetime.strptime(task[3], "%Y-%m-%d %H:%M")
                    if datetime.now() >= deadline - timedelta(minutes=10):
                        messagebox.showinfo("Reminder", f"Task '{task[1]}' is due soon!")
                        break
            threading.Event().wait(60)

# Main
if __name__ == "__main__":
    setup_database()
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
