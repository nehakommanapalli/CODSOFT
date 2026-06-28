import json
import os
import uuid
from datetime import datetime

class TodoManager:
    def __init__(self, filepath="todo_data.json"):
        # Resolve path relative to the directory of this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.filepath = os.path.join(current_dir, filepath)
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        """Loads tasks from the JSON file. Creates file if it doesn't exist."""
        if not os.path.exists(self.filepath):
            self.tasks = []
            self.save_tasks()
            return

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                self.tasks = json.load(f)
        except (json.JSONDecodeError, IOError):
            # Fallback for corrupted file
            self.tasks = []
            self.save_tasks()

    def save_tasks(self):
        """Saves tasks to the JSON file."""
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.tasks, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Error saving tasks: {e}")

    def add_task(self, title, priority="Medium", category="General", due_date=""):
        """Adds a new task to the list."""
        if not title.strip():
            return None

        task = {
            "id": str(uuid.uuid4())[:8],  # Use short unique ID
            "title": title.strip(),
            "priority": priority,
            "category": category,
            "due_date": due_date.strip(),
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.tasks.append(task)
        self.save_tasks()
        return task

    def get_tasks(self, category_filter=None, completed_filter=None, search_query=None):
        """Returns tasks filtered by completion status, category, and search query."""
        filtered = self.tasks
        
        if category_filter and category_filter != "All":
            filtered = [t for t in filtered if t["category"].lower() == category_filter.lower()]
            
        if completed_filter is not None:
            filtered = [t for t in filtered if t["completed"] == completed_filter]
            
        if search_query:
            query = search_query.lower()
            filtered = [t for t in filtered if query in t["title"].lower() or query in t["category"].lower()]
            
        return filtered

    def toggle_task(self, task_id):
        """Toggles the completion status of a task by ID."""
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = not task["completed"]
                self.save_tasks()
                return True
        return False

    def update_task(self, task_id, title=None, priority=None, category=None, due_date=None):
        """Updates task details."""
        for task in self.tasks:
            if task["id"] == task_id:
                if title is not None:
                    task["title"] = title.strip()
                if priority is not None:
                    task["priority"] = priority
                if category is not None:
                    task["category"] = category
                if due_date is not None:
                    task["due_date"] = due_date.strip()
                self.save_tasks()
                return True
        return False

    def delete_task(self, task_id):
        """Deletes a task by ID."""
        initial_len = len(self.tasks)
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        if len(self.tasks) < initial_len:
            self.save_tasks()
            return True
        return False

    def clear_all(self):
        """Removes all tasks."""
        self.tasks = []
        self.save_tasks()

    def get_completion_percentage(self):
        """Returns percentage of completed tasks."""
        if not self.tasks:
            return 0.0
        completed = sum(1 for t in self.tasks if t["completed"])
        return round((completed / len(self.tasks)) * 100, 1)
