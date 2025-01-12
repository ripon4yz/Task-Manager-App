
---

## **Task Manager App**



---

### **Features:**

- **Task Management:**
  - Add new tasks with a title, description, and deadline.
  - View a list of tasks with deadlines and completion status.
  - Mark tasks as completed or delete them.
  
- **Reminders:**
  - Receive notifications for tasks that are due soon (within 10 minutes of the deadline).

- **User Interface:**
  - Built using **Tkinter** for the graphical interface.
  - Calendar widget (from **tkcalendar**) for selecting dates.
  - Simple text input for task details and time.
  - An easy-to-use interface for managing tasks, deadlines, and reminders.

---

### **Technologies and Libraries Used:**

1. **Python**:
   - Programming language used for the entire development of the app.

2. **Tkinter**:
   - A Python library for creating graphical user interfaces (GUIs). It is used for creating the windows, buttons, labels, and other components in the app.

3. **tkcalendar**:
   - A library that adds calendar functionality to Tkinter. It allows the user to select a date for the task deadline.

4. **SQLite**:
   - A lightweight database used to store tasks, deadlines, and completion status. It stores all the task-related data persistently.

5. **Threading**:
   - Used for running reminder checks in the background without blocking the main UI thread. This allows the app to continuously monitor tasks and send reminders as needed.

6. **PyInstaller**:
   - Used to package the Python application into a standalone executable (`.exe`) that can be run on Windows without needing Python installed.

---

### **Installation Instructions:**

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/Task-Manager-App.git
   ```

2. Install dependencies:
   If you haven't installed the required dependencies, run the following commands:
   ```bash
   pip install tk
   pip install tkcalendar
   ```

3. Run the app:
   After installing the dependencies, you can run the app by executing:
   ```bash
   python TaskManagerApp.py
   ```

4. (Optional) **Creating an Executable**:
   If you want to create a standalone executable for Windows, use **PyInstaller**:
   ```bash
   pyinstaller --onefile --windowed TaskManagerApp.py
   ```
   This will create an executable in the `dist` folder, which you can run without needing Python installed.

---

### **How it was Made:**

1. **User Interface**:
   The app's graphical interface was created using **Tkinter**. It includes text input fields, buttons, and a calendar for selecting the task deadline. The UI is simple and designed for ease of use, with labels and input fields clearly separated.

2. **Database**:
   An **SQLite** database is used to store all tasks. The database schema includes fields for the task title, description, deadline, and completion status. Tasks are added, viewed, updated, and deleted using SQLite queries.

3. **Task Reminder**:
   The app includes a background thread that checks if any tasks are due soon (within 10 minutes). It sends a reminder to the user when a task is nearing its deadline. This background process runs without interrupting the main UI, thanks to Python's threading module.

4. **Packaging**:
   After development, **PyInstaller** was used to package the Python application into a standalone Windows executable. This allows users to run the app on their computers without needing Python or other dependencies installed.

---

### **Usage Instructions:**

- **Adding Tasks**:
  - Enter a title and description for the task.
  - Select a date and time for the deadline.
  - Click "Add Task" to add the task to the list.

- **Viewing Tasks**:
  - All tasks are displayed in a table, showing the task ID, title, description, deadline, and completion status.

- **Marking Tasks as Completed**:
  - Select a task from the list and click "Mark Completed". This will update the task's status.

- **Deleting Tasks**:
  - Select a task from the list and click "Delete Task" to remove it from the list and database.

- **Reminder Notifications**:
  - The app will remind you of tasks that are nearing their deadlines. These reminders will pop up as system notifications.

---

### **License:**
Feel free to use, modify, or distribute the code under the MIT License (or any other license you choose).

---

### **Contributors:**
- **Ripon R. Rahman** (Developer)

---

