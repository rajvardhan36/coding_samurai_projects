"""
TO-DO LIST GUI APPLICATION
For Coding Samurai Python Development Internship - Project 2
Opens in a new window with graphical interface
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
import json
import os
from datetime import datetime

class TodoListApp:
    def __init__(self):
        # Create main window
        self.root = tk.Tk()
        self.root.title("Coding Samurai - To-Do List")
        self.root.geometry("800x600")
        self.root.configure(bg="#F5F7FA")
        
        # File for saving tasks
        self.filename = "todo_gui.json"
        self.tasks = self.load_tasks()
        
        # Custom fonts
        self.title_font = font.Font(family="Arial", size=24, weight="bold")
        self.task_font = font.Font(family="Arial", size=12)
        self.button_font = font.Font(family="Arial", size=11, weight="bold")
        
        # Setup the UI
        self.setup_ui()
        
    def load_tasks(self):
        """Load tasks from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    return json.load(file)
            except:
                return []
        return []
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        with open(self.filename, 'w') as file:
            json.dump(self.tasks, file, indent=2)
    
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg="#F5F7FA")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_frame, bg="#F5F7FA")
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            header_frame,
            text="📝 To-Do List Application",
            font=self.title_font,
            bg="#F5F7FA",
            fg="#2C3E50"
        ).pack(side=tk.LEFT)
        
        # Stats label
        self.stats_label = tk.Label(
            header_frame,
            text="Tasks: 0 | Completed: 0",
            font=("Arial", 11),
            bg="#F5F7FA",
            fg="#7F8C8D"
        )
        self.stats_label.pack(side=tk.RIGHT)
        
        # Input section
        input_frame = tk.Frame(main_frame, bg="#F5F7FA")
        input_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            input_frame,
            text="Add New Task:",
            font=self.button_font,
            bg="#F5F7FA",
            fg="#2C3E50"
        ).pack(anchor=tk.W)
        
        # Task entry
        self.task_entry = tk.Entry(
            input_frame,
            font=self.task_font,
            bg="white",
            fg="#2C3E50",
            relief=tk.FLAT,
            width=50
        )
        self.task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.task_entry.bind("<Return>", lambda e: self.add_task())
        
        # Add button
        add_btn = tk.Button(
            input_frame,
            text="➕ Add Task",
            font=self.button_font,
            bg="#27AE60",
            fg="white",
            activebackground="#219653",
            activeforeground="white",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=self.add_task
        )
        add_btn.pack(side=tk.RIGHT)
        
        # Task list section
        list_frame = tk.Frame(main_frame, bg="#F5F7FA")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # List header
        list_header = tk.Frame(list_frame, bg="#34495E")
        list_header.pack(fill=tk.X)
        
        headers = ["Status", "ID", "Task", "Created", "Actions"]
        for i, header in enumerate(headers):
            tk.Label(
                list_header,
                text=header,
                font=self.button_font,
                bg="#34495E",
                fg="white",
                padx=10,
                pady=10
            ).grid(row=0, column=i, sticky="w")
        
        # Configure grid weights
        for i in range(5):
            list_header.grid_columnconfigure(i, weight=1)
        
        # Treeview for tasks
        self.tree_frame = tk.Frame(list_frame, bg="#F5F7FA")
        self.tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas and scrollbar
        self.canvas = tk.Canvas(self.tree_frame, bg="#F5F7FA", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#F5F7FA")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind mouse wheel for scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Control buttons
        control_frame = tk.Frame(main_frame, bg="#F5F7FA")
        control_frame.pack(fill=tk.X, pady=(20, 0))
        
        buttons = [
            ("✅ Mark Complete", "#2ECC71", self.mark_complete),
            ("🗑️ Delete", "#E74C3C", self.delete_task),
            ("🔍 Search", "#3498DB", self.search_tasks),
            ("🧹 Clear Completed", "#95A5A6", self.clear_completed),
            ("🔄 Refresh", "#9B59B6", self.refresh_list),
            ("💾 Save & Exit", "#2C3E50", self.exit_app)
        ]
        
        for text, color, command in buttons:
            btn = tk.Button(
                control_frame,
                text=text,
                font=self.button_font,
                bg=color,
                fg="white",
                activebackground=color,
                activeforeground="white",
                relief=tk.FLAT,
                padx=15,
                pady=8,
                command=command
            )
            btn.pack(side=tk.LEFT, padx=5)
        
        # Load and display initial tasks
        self.refresh_list()
    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def add_task(self):
        """Add a new task"""
        task_text = self.task_entry.get().strip()
        if not task_text:
            messagebox.showwarning("Empty Task", "Please enter a task description!")
            return
        
        new_task = {
            "id": len(self.tasks) + 1,
            "task": task_text,
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "completed_at": None
        }
        
        self.tasks.append(new_task)
        self.save_tasks()
        self.task_entry.delete(0, tk.END)
        self.refresh_list()
        messagebox.showinfo("Success", f"Task added successfully! (ID: {new_task['id']})")
    
    def refresh_list(self):
        """Refresh the task list display"""
        # Clear current display
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Display tasks
        for task in self.tasks:
            task_frame = tk.Frame(self.scrollable_frame, bg="white", relief=tk.RAISED, bd=1)
            task_frame.pack(fill=tk.X, pady=2)
            
            # Status
            status = "✅" if task["completed"] else "⏳"
            status_color = "#27AE60" if task["completed"] else "#F39C12"
            tk.Label(
                task_frame,
                text=status,
                font=self.task_font,
                bg=status_color,
                fg="white",
                width=4
            ).grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
            
            # ID
            tk.Label(
                task_frame,
                text=str(task["id"]),
                font=self.task_font,
                bg="white",
                fg="#2C3E50",
                width=5
            ).grid(row=0, column=1, sticky="w", padx=5)
            
            # Task
            task_text = task["task"]
            if task["completed"]:
                task_text = f"~~{task_text}~~"
            
            tk.Label(
                task_frame,
                text=task_text,
                font=self.task_font,
                bg="white",
                fg="#2C3E50" if not task["completed"] else "#95A5A6",
                anchor="w",
                wraplength=300
            ).grid(row=0, column=2, sticky="w", padx=5)
            
            # Created date
            tk.Label(
                task_frame,
                text=task["created_at"],
                font=self.task_font,
                bg="white",
                fg="#7F8C8D"
            ).grid(row=0, column=3, sticky="w", padx=5)
            
            # Action buttons
            action_frame = tk.Frame(task_frame, bg="white")
            action_frame.grid(row=0, column=4, sticky="e", padx=5)
            
            if not task["completed"]:
                complete_btn = tk.Button(
                    action_frame,
                    text="✓",
                    font=self.task_font,
                    bg="#27AE60",
                    fg="white",
                    width=3,
                    command=lambda tid=task["id"]: self.mark_complete_single(tid)
                )
                complete_btn.pack(side=tk.LEFT, padx=2)
            
            delete_btn = tk.Button(
                action_frame,
                text="✗",
                font=self.task_font,
                bg="#E74C3C",
                fg="white",
                width=3,
                command=lambda tid=task["id"]: self.delete_single_task(tid)
            )
            delete_btn.pack(side=tk.LEFT, padx=2)
            
            # Configure grid weights
            for i in range(5):
                task_frame.grid_columnconfigure(i, weight=1 if i == 2 else 0)
        
        # Update statistics
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t["completed"])
        self.stats_label.config(text=f"Tasks: {total} | Completed: {completed}")
    
    def mark_complete_single(self, task_id):
        """Mark a single task as complete"""
        for task in self.tasks:
            if task["id"] == task_id and not task["completed"]:
                task["completed"] = True
                task["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                self.save_tasks()
                self.refresh_list()
                messagebox.showinfo("Success", f"Task {task_id} marked as complete!")
                return
        messagebox.showwarning("Warning", f"Task {task_id} not found or already completed!")
    
    def delete_single_task(self, task_id):
        """Delete a single task"""
        if messagebox.askyesno("Confirm Delete", f"Delete task {task_id}?"):
            for i, task in enumerate(self.tasks):
                if task["id"] == task_id:
                    self.tasks.pop(i)
                    # Reassign IDs
                    for idx, t in enumerate(self.tasks, 1):
                        t["id"] = idx
                    self.save_tasks()
                    self.refresh_list()
                    messagebox.showinfo("Deleted", "Task deleted successfully!")
                    return
    
    def mark_complete(self):
        """Mark selected task as complete"""
        if not self.tasks:
            messagebox.showwarning("No Tasks", "No tasks to mark as complete!")
            return
        self.refresh_list()
    
    def delete_task(self):
        """Delete a task dialog"""
        if not self.tasks:
            messagebox.showwarning("No Tasks", "No tasks to delete!")
            return
        self.refresh_list()
    
    def search_tasks(self):
        """Search for tasks"""
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Tasks")
        search_window.geometry("400x300")
        search_window.configure(bg="#F5F7FA")
        
        tk.Label(
            search_window,
            text="🔍 Search Tasks",
            font=self.title_font,
            bg="#F5F7FA",
            fg="#2C3E50"
        ).pack(pady=20)
        
        search_entry = tk.Entry(
            search_window,
            font=self.task_font,
            width=30
        )
        search_entry.pack(pady=10)
        
        result_text = tk.Text(
            search_window,
            height=10,
            width=40,
            font=self.task_font
        )
        result_text.pack(pady=10)
        
        def perform_search():
            keyword = search_entry.get().strip().lower()
            result_text.delete(1.0, tk.END)
            
            if not keyword:
                result_text.insert(tk.END, "Please enter a search keyword!")
                return
            
            results = [t for t in self.tasks if keyword in t["task"].lower()]
            
            if results:
                result_text.insert(tk.END, f"Found {len(results)} task(s):\n\n")
                for task in results:
                    status = "Completed" if task["completed"] else "Pending"
                    result_text.insert(tk.END, f"ID {task['id']}: {task['task']} ({status})\n")
            else:
                result_text.insert(tk.END, f"No tasks found for '{keyword}'")
        
        tk.Button(
            search_window,
            text="Search",
            command=perform_search,
            bg="#3498DB",
            fg="white",
            font=self.button_font,
            padx=20
        ).pack(pady=10)
    
    def clear_completed(self):
        """Clear all completed tasks"""
        completed_count = sum(1 for t in self.tasks if t["completed"])
        
        if completed_count == 0:
            messagebox.showinfo("No Completed Tasks", "No completed tasks to clear!")
            return
        
        if messagebox.askyesno("Confirm Clear", f"Clear {completed_count} completed task(s)?"):
            self.tasks = [t for t in self.tasks if not t["completed"]]
            # Reassign IDs
            for idx, task in enumerate(self.tasks, 1):
                task["id"] = idx
            self.save_tasks()
            self.refresh_list()
            messagebox.showinfo("Cleared", f"Cleared {completed_count} completed task(s)!")
    
    def exit_app(self):
        """Save and exit the application"""
        self.save_tasks()
        self.root.quit()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

# Launch the application immediately
if __name__ == "__main__":
    app = TodoListApp()
    app.run()