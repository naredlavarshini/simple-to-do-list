import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from datetime import datetime

# Database setup
def init_db():
    conn = sqlite3.connect('todo_list.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        priority INTEGER,
        due_date TEXT,
        category TEXT,
        status TEXT DEFAULT 'Incomplete'
    )
    ''')
    conn.commit()
    conn.close()

# Class for the To-Do List Application
class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("To-Do List Application")
        self.geometry("800x600")
        
        self.create_widgets()
        self.populate_tasks()

    def create_widgets(self):
        # Input fields
        tk.Label(self, text="Title:").grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.title_entry = tk.Entry(self)
        self.title_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        tk.Label(self, text="Description:").grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.description_entry = tk.Entry(self)
        self.description_entry.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

        tk.Label(self, text="Priority (1-5):").grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.priority_entry = tk.Entry(self)
        self.priority_entry.grid(row=2, column=1, padx=10, pady=10, sticky='ew')

        tk.Label(self, text="Due Date (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=10, sticky='w')
        self.due_date_entry = tk.Entry(self)
        self.due_date_entry.grid(row=3, column=1, padx=10, pady=10, sticky='ew')

        tk.Label(self, text="Category:").grid(row=4, column=0, padx=10, pady=10, sticky='w')
        self.category_entry = tk.Entry(self)
        self.category_entry.grid(row=4, column=1, padx=10, pady=10, sticky='ew')

        # Buttons
        self.add_button = tk.Button(self, text="Add Task", command=self.add_task)
        self.add_button.grid(row=5, column=0, padx=10, pady=10)

        self.update_button = tk.Button(self, text="Update Task", command=self.update_task)
        self.update_button.grid(row=5, column=1, padx=10, pady=10)

        self.delete_button = tk.Button(self, text="Delete Task", command=self.delete_task)
        self.delete_button.grid(row=5, column=2, padx=10, pady=10)

        self.mark_complete_button = tk.Button(self, text="Mark Complete", command=self.mark_complete)
        self.mark_complete_button.grid(row=5, column=3, padx=10, pady=10)

        # Task List
        self.task_tree = ttk.Treeview(self, columns=('ID', 'Title', 'Description', 'Priority', 'Due Date', 'Category', 'Status'), show='headings')
        self.task_tree.heading('ID', text='ID')
        self.task_tree.heading('Title', text='Title')
        self.task_tree.heading('Description', text='Description')
        self.task_tree.heading('Priority', text='Priority')
        self.task_tree.heading('Due Date', text='Due Date')
        self.task_tree.heading('Category', text='Category')
        self.task_tree.heading('Status', text='Status')
        self.task_tree.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')

        self.task_tree.bind('<<TreeviewSelect>>', self.on_task_select)

    def populate_tasks(self):
        for i in self.task_tree.get_children():
            self.task_tree.delete(i)

        conn = sqlite3.connect('todo_list.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks')
        rows = cursor.fetchall()
        for row in rows:
            self.task_tree.insert('', tk.END, values=row)
        conn.close()

    def add_task(self):
        title = self.title_entry.get()
        description = self.description_entry.get()
        priority = self.priority_entry.get()
        due_date = self.due_date_entry.get()
        category = self.category_entry.get()

        if not title:
            messagebox.showerror("Error", "Title is required")
            return

        try:
            if priority:
                priority = int(priority)
            if due_date:
                datetime.strptime(due_date, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Invalid input for priority or due date")
            return

        conn = sqlite3.connect('todo_list.db')
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO tasks (title, description, priority, due_date, category)
        VALUES (?, ?, ?, ?, ?)
        ''', (title, description, priority, due_date, category))
        conn.commit()
        conn.close()
        self.populate_tasks()

    def update_task(self):
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No task selected")
            return

        item = self.task_tree.item(selected_item)
        task_id = item['values'][0]

        title = self.title_entry.get()
        description = self.description_entry.get()
        priority = self.priority_entry.get()
        due_date = self.due_date_entry.get()
        category = self.category_entry.get()

        if not title:
            messagebox.showerror("Error", "Title is required")
            return

        try:
            if priority:
                priority = int(priority)
            if due_date:
                datetime.strptime(due_date, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Invalid input for priority or due date")
            return

        conn = sqlite3.connect('todo_list.db')
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE tasks
        SET title = ?, description = ?, priority = ?, due_date = ?, category = ?
        WHERE id = ?
        ''', (title, description, priority, due_date, category, task_id))
        conn.commit()
        conn.close()
        self.populate_tasks()

    def delete_task(self):
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No task selected")
            return

        item = self.task_tree.item(selected_item)
        task_id = item['values'][0]

        conn = sqlite3.connect('todo_list.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        conn.close()
        self.populate_tasks()

    def mark_complete(self):
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No task selected")
            return

        item = self.task_tree.item(selected_item)
        task_id = item['values'][0]

        conn = sqlite3.connect('todo_list.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE tasks SET status = ? WHERE id = ?', ('Complete', task_id))
        conn.commit()
        conn.close()
        self.populate_tasks()

    def on_task_select(self, event):
        selected_item = self.task_tree.selection()
        if not selected_item:
            return

        item = self.task_tree.item(selected_item)
        values = item['values']

        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, values[1])

        self.description_entry.delete(0, tk.END)
        self.description_entry.insert(0, values[2])

        self.priority_entry.delete(0, tk.END)
        self.priority_entry.insert(0, values[3])

        self.due_date_entry.delete(0, tk.END)
        self.due_date_entry.insert(0, values[4])

        self.category_entry.delete(0, tk.END)
        self.category_entry.insert(0, values[5])

if __name__ == "__main__":
    init_db()
    app = TodoApp()
    app.mainloop()
