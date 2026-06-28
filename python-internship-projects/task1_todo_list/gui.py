import tkinter as tk
from tkinter import messagebox, simpledialog
import customtkinter as ctk
from todo_manager import TodoManager

# Configure CustomTkinter
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class TodoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.manager = TodoManager()

        # Window configuration
        self.title("To-Do Flow - Task Manager")
        self.geometry("900x600")
        self.minimum_size = (850, 550)
        self.minsize(850, 550)

        # State variables
        self.current_category_filter = "All"
        self.current_completion_filter = "All"  # "All", "Pending", "Completed"
        self.search_text = ""

        # Layout grids
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.create_sidebar()
        self.create_main_content()
        self.load_and_render_tasks()

    def create_sidebar(self):
        # Sidebar Frame
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # App Title
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="To-Do Flow", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Progress tracking panel
        self.progress_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.progress_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.progress_label = ctk.CTkLabel(self.progress_frame, text="Completion Progress: 0%")
        self.progress_label.pack(anchor="w", pady=2)
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.pack(fill="x", pady=5)
        self.progress_bar.set(0.0)

        # Filters Label
        self.filter_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="Filter Status", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.filter_label.grid(row=2, column=0, padx=20, pady=(20, 5), sticky="w")

        # Completion Status filter options
        self.status_option = ctk.CTkSegmentedButton(
            self.sidebar_frame, 
            values=["All", "Pending", "Completed"],
            command=self.change_status_filter
        )
        self.status_option.grid(row=3, column=0, padx=20, pady=5, sticky="ew")
        self.status_option.set("All")

        # Category Filter Label
        self.cat_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="Category Filter", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.cat_label.grid(row=4, column=0, padx=20, pady=(20, 5), sticky="w")

        # Category Option
        self.cat_option = ctk.CTkOptionMenu(
            self.sidebar_frame,
            values=["All", "General", "Work", "Personal", "Shopping", "Health"],
            command=self.change_category_filter
        )
        self.cat_option.grid(row=5, column=0, padx=20, pady=5, sticky="ew")
        self.cat_option.set("All")

        # Utility Buttons Frame at bottom
        self.settings_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.settings_frame.grid(row=6, column=0, padx=20, pady=20, sticky="ew")

        # Theme toggle
        self.appearance_label = ctk.CTkLabel(self.settings_frame, text="Appearance Mode:")
        self.appearance_label.pack(anchor="w", pady=2)
        self.appearance_menu = ctk.CTkOptionMenu(
            self.settings_frame,
            values=["Dark", "Light", "System"],
            command=self.change_appearance_mode
        )
        self.appearance_menu.pack(fill="x", pady=5)
        self.appearance_menu.set("Dark")
        ctk.set_appearance_mode("Dark")

        # Clear All Button
        self.clear_btn = ctk.CTkButton(
            self.settings_frame, 
            text="Clear All Tasks", 
            fg_color="#C0392B", 
            hover_color="#962D22", 
            command=self.clear_all_tasks
        )
        self.clear_btn.pack(fill="x", pady=(10, 0))

    def create_main_content(self):
        # Main Area Frame
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_rowconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Header Search Bar
        self.header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(
            self.header_frame, 
            placeholder_text="Search tasks..."
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self.on_search_change)

        # Add Task input Panel
        self.input_frame = ctk.CTkFrame(self.main_frame)
        self.input_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15), padx=2)
        
        # Grid inside Input Panel
        self.input_frame.grid_columnconfigure(0, weight=1) # Title gets most space
        
        # Title Entry
        self.task_entry = ctk.CTkEntry(self.input_frame, placeholder_text="What needs to be done?")
        self.task_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.task_entry.bind("<Return>", lambda e: self.add_task())

        # Dropdowns & Add Button Row
        self.controls_subframe = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        self.controls_subframe.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        self.priority_menu = ctk.CTkOptionMenu(
            self.controls_subframe,
            values=["Low", "Medium", "High"],
            width=95
        )
        self.priority_menu.pack(side="left", padx=5)
        self.priority_menu.set("Medium")

        self.category_menu = ctk.CTkOptionMenu(
            self.controls_subframe,
            values=["General", "Work", "Personal", "Shopping", "Health"],
            width=95
        )
        self.category_menu.pack(side="left", padx=5)
        self.category_menu.set("General")

        self.due_entry = ctk.CTkEntry(self.controls_subframe, placeholder_text="Due (e.g. Tomorrow)", width=120)
        self.due_entry.pack(side="left", padx=5)

        self.add_btn = ctk.CTkButton(
            self.controls_subframe, 
            text="Add Task", 
            width=80, 
            command=self.add_task
        )
        self.add_btn.pack(side="left", padx=5)

        # Scrollable Frame for Task List
        self.task_list_frame = ctk.CTkScrollableFrame(self.main_frame, label_text="Tasks")
        self.task_list_frame.grid(row=2, column=0, sticky="nsew")

    def load_and_render_tasks(self):
        # Clear current task entries in GUI
        for widget in self.task_list_frame.winfo_children():
            widget.destroy()

        # Fetch filtered tasks
        completed_filter = None
        if self.current_completion_filter == "Pending":
            completed_filter = False
        elif self.current_completion_filter == "Completed":
            completed_filter = True

        tasks = self.manager.get_tasks(
            category_filter=self.current_category_filter,
            completed_filter=completed_filter,
            search_query=self.search_text
        )

        # Render tasks
        for idx, task in enumerate(tasks):
            self.render_task_item(task, idx)

        # Update sidebar statistics
        completion_percent = self.manager.get_completion_percentage()
        self.progress_label.configure(text=f"Completion Progress: {completion_percent}%")
        self.progress_bar.set(completion_percent / 100.0)

    def render_task_item(self, task, idx):
        # Create row frame
        row_frame = ctk.CTkFrame(self.task_list_frame)
        row_frame.pack(fill="x", pady=4, padx=5)
        
        # Completion checkbox
        cb_var = tk.BooleanVar(value=task["completed"])
        cb = ctk.CTkCheckBox(
            row_frame, 
            text="", 
            variable=cb_var, 
            width=24,
            command=lambda tid=task["id"]: self.toggle_task(tid)
        )
        cb.pack(side="left", padx=(10, 5))

        # Priority Color Indicator
        priority_colors = {
            "High": "#E74C3C",    # Red
            "Medium": "#E67E22",  # Orange
            "Low": "#7F8C8D"      # Gray
        }
        p_color = priority_colors.get(task["priority"], "#7F8C8D")

        # Text label (title)
        # Apply strikethrough if completed
        display_text = task["title"]
        label_font = ctk.CTkFont(size=13, weight="normal")
        if task["completed"]:
            # Customtkinter doesn't support easy strikethrough styling in label font directly via configuration 
            # as cleanly, so we can change the text color or add visual completion prefix if needed.
            # Let's italicize and dim the text color.
            label_font = ctk.CTkFont(size=13, slant="italic")
            txt_color = "gray"
        else:
            txt_color = ("black", "white")

        title_label = ctk.CTkLabel(
            row_frame, 
            text=display_text, 
            font=label_font, 
            text_color=txt_color,
            anchor="w"
        )
        title_label.pack(side="left", fill="x", expand=True, padx=5)

        # Badges & Buttons Frame
        badge_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        badge_frame.pack(side="right", padx=5)

        # Due Date badge
        if task["due_date"]:
            due_label = ctk.CTkLabel(
                badge_frame, 
                text=f" 📅 {task['due_date']} ", 
                font=ctk.CTkFont(size=10),
                fg_color=("#EAEDED", "#2C3E50"),
                corner_radius=4
            )
            due_label.pack(side="left", padx=3)

        # Category badge
        cat_color = {
            "General": "#34495E",
            "Work": "#2980B9",
            "Personal": "#8E44AD",
            "Shopping": "#27AE60",
            "Health": "#D35400"
        }.get(task["category"], "#34495E")

        cat_label = ctk.CTkLabel(
            badge_frame, 
            text=f" {task['category']} ", 
            font=ctk.CTkFont(size=10, weight="bold"),
            fg_color=cat_color,
            text_color="white",
            corner_radius=4
        )
        cat_label.pack(side="left", padx=3)

        # Priority Badge
        p_label = ctk.CTkLabel(
            badge_frame, 
            text=f" {task['priority']} ", 
            font=ctk.CTkFont(size=10, weight="bold"),
            fg_color=p_color,
            text_color="white",
            corner_radius=4
        )
        p_label.pack(side="left", padx=3)

        # Edit button
        edit_btn = ctk.CTkButton(
            badge_frame, 
            text="✏️", 
            width=28, 
            height=24,
            fg_color="transparent",
            hover_color=("#D5D8DC", "#34495E"),
            command=lambda tid=task["id"]: self.edit_task(tid)
        )
        edit_btn.pack(side="left", padx=2)

        # Delete button
        del_btn = ctk.CTkButton(
            badge_frame, 
            text="🗑️", 
            width=28, 
            height=24,
            fg_color="transparent",
            hover_color=("#FADBD8", "#78281F"),
            command=lambda tid=task["id"]: self.delete_task(tid)
        )
        del_btn.pack(side="left", padx=2)

    def add_task(self):
        title = self.task_entry.get().strip()
        if not title:
            messagebox.showwarning("Empty Task", "Please enter a task description.")
            return

        priority = self.priority_menu.get()
        category = self.category_menu.get()
        due_date = self.due_entry.get().strip()

        self.manager.add_task(title, priority, category, due_date)
        
        # Clear inputs
        self.task_entry.delete(0, tk.END)
        self.due_entry.delete(0, tk.END)
        self.priority_menu.set("Medium")
        self.category_menu.set("General")

        self.load_and_render_tasks()

    def toggle_task(self, task_id):
        self.manager.toggle_task(task_id)
        # Rerender to apply visual updates (e.g. strikethrough/dimming)
        # Use delay so checking checkbox feels smooth before complete reload
        self.after(100, self.load_and_render_tasks)

    def edit_task(self, task_id):
        # Find current task
        task = next((t for t in self.manager.tasks if t["id"] == task_id), None)
        if not task:
            return

        new_title = simpledialog.askstring("Edit Task", "Update task description:", initialvalue=task["title"])
        if new_title is not None and new_title.strip() != "":
            self.manager.update_task(task_id, title=new_title)
            self.load_and_render_tasks()

    def delete_task(self, task_id):
        if messagebox.askyesno("Delete Task", "Are you sure you want to delete this task?"):
            self.manager.delete_task(task_id)
            self.load_and_render_tasks()

    def clear_all_tasks(self):
        if messagebox.askyesno("Clear All", "Delete ALL tasks? This cannot be undone."):
            self.manager.clear_all()
            self.load_and_render_tasks()

    def change_category_filter(self, category):
        self.current_category_filter = category
        self.load_and_render_tasks()

    def change_status_filter(self, status):
        self.current_completion_filter = status
        self.load_and_render_tasks()

    def on_search_change(self, event):
        self.search_text = self.search_entry.get().strip()
        self.load_and_render_tasks()

    def change_appearance_mode(self, new_mode):
        ctk.set_appearance_mode(new_mode)

if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
