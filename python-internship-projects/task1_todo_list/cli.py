import sys
from todo_manager import TodoManager

def print_header(title):
    print("\n" + "=" * 60)
    print(f" {title} ".center(60, "-"))
    print("=" * 60)

def display_tasks(tasks):
    if not tasks:
        print("\nNo tasks found.")
        return

    print(f"\n{'ID':<10} | {'Status':<8} | {'Title':<25} | {'Priority':<8} | {'Category':<10} | {'Due Date':<10}")
    print("-" * 80)
    for task in tasks:
        status = "[✓]" if task["completed"] else "[ ]"
        due = task["due_date"] if task["due_date"] else "N/A"
        # Truncate title if it's too long
        title = task["title"]
        if len(title) > 22:
            title = title[:22] + "..."
        print(f"{task['id']:<10} | {status:<8} | {title:<25} | {task['priority']:<8} | {task['category']:<10} | {due:<10}")
    print("-" * 80)

def main():
    manager = TodoManager()
    
    while True:
        print_header("TO-DO LIST MANAGER")
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Toggle Task Completion")
        print("4. Edit Task")
        print("5. Delete Task")
        print("6. View Progress Stats")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == '1':
            print("\nFilter options: 1. All Tasks  2. Pending  3. Completed")
            filter_choice = input("Select filter (default: 1): ").strip()
            
            completed_filter = None
            if filter_choice == '2':
                completed_filter = False
            elif filter_choice == '3':
                completed_filter = True
                
            tasks = manager.get_tasks(completed_filter=completed_filter)
            display_tasks(tasks)
            
        elif choice == '2':
            title = input("Enter task title: ").strip()
            if not title:
                print("Task title cannot be empty.")
                continue
                
            priority = input("Priority (Low/Medium/High, default Medium): ").strip().capitalize()
            if priority not in ["Low", "Medium", "High"]:
                priority = "Medium"
                
            category = input("Category (e.g. Work, Personal, General, default General): ").strip().capitalize()
            if not category:
                category = "General"
                
            due_date = input("Due Date (e.g. YYYY-MM-DD, optional): ").strip()
            
            task = manager.add_task(title, priority, category, due_date)
            if task:
                print(f"\nTask successfully added! [ID: {task['id']}]")
            else:
                print("\nFailed to add task.")
                
        elif choice == '3':
            tasks = manager.get_tasks()
            display_tasks(tasks)
            if not tasks:
                continue
                
            task_id = input("\nEnter Task ID to toggle completion: ").strip()
            if manager.toggle_task(task_id):
                print("\nTask status updated successfully.")
            else:
                print("\nInvalid Task ID.")
                
        elif choice == '4':
            tasks = manager.get_tasks()
            display_tasks(tasks)
            if not tasks:
                continue
                
            task_id = input("\nEnter Task ID to edit: ").strip()
            # Check if task exists
            task_exists = any(t["id"] == task_id for t in tasks)
            if not task_exists:
                print("\nInvalid Task ID.")
                continue
                
            print("\nLeave input empty to keep current value.")
            title = input("New Title: ").strip()
            priority = input("New Priority (Low/Medium/High): ").strip().capitalize()
            category = input("New Category: ").strip().capitalize()
            due_date = input("New Due Date (YYYY-MM-DD): ").strip()
            
            title = title if title else None
            priority = priority if priority in ["Low", "Medium", "High"] else None
            category = category if category else None
            due_date = due_date if due_date else None
            
            if manager.update_task(task_id, title, priority, category, due_date):
                print("\nTask updated successfully.")
            else:
                print("\nFailed to update task.")
                
        elif choice == '5':
            tasks = manager.get_tasks()
            display_tasks(tasks)
            if not tasks:
                continue
                
            task_id = input("\nEnter Task ID to delete: ").strip()
            confirm = input(f"Are you sure you want to delete task {task_id}? (y/n): ").strip().lower()
            if confirm == 'y':
                if manager.delete_task(task_id):
                    print("\nTask deleted successfully.")
                else:
                    print("\nInvalid Task ID.")
            else:
                print("\nDeletion cancelled.")
                
        elif choice == '6':
            percent = manager.get_completion_percentage()
            total = len(manager.tasks)
            completed = sum(1 for t in manager.tasks if t["completed"])
            pending = total - completed
            
            print_header("PROGRESS STATS")
            print(f"Total Tasks:     {total}")
            print(f"Completed:       {completed}")
            print(f"Pending:         {pending}")
            print(f"Completion Rate: {percent}%")
            
            # Simple text progress bar
            bar_length = 20
            filled = int(percent / 100 * bar_length)
            bar = "█" * filled + "-" * (bar_length - filled)
            print(f"Progress Bar:    [{bar}]")
            
        elif choice == '7':
            print("\nThank you for using To-Do List Manager. Goodbye!")
            sys.exit()
            
        else:
            print("\nInvalid choice. Please enter a number between 1 and 7.")

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
