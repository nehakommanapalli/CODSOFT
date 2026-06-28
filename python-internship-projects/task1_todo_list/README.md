# Task 1: To-Do List Application

A professional-grade To-Do List application supporting task categorization, prioritization, completion percentages, due dates, and persistent local storage.

## Features

- **Double-Mode Interface**: Enjoy either a clean interactive Command Line Interface (CLI) or a modern, sleek Graphical User Interface (GUI).
- **Persistent Data**: Tasks are automatically saved to and loaded from `todo_data.json`.
- **Filtering & Search**: Search tasks by title or category, filter by completion status, and filter by categories (General, Work, Personal, Shopping, Health).
- **Priority Badges**: Tasks are priority-coded (Low, Medium, High) with corresponding indicator colors.
- **Progress Tracking**: See your completion progress dynamically update.

---

## How to Run

Navigate to the project root directory first.

### Run CLI version
```bash
python task1_todo_list/cli.py
```

### Run GUI version
```bash
python task1_todo_list/main.py
```

*Note: The GUI version requires `customtkinter`. Ensure dependencies are installed via `pip install -r requirements.txt`.*
