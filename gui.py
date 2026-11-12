import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os

# Database connection
DB_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "students.db"
)
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Main window
root = tk.Tk()
root.title("Student Management System")
root.geometry("800x600")
root.configure(bg="#eaf2f8")

# Heading
heading = tk.Label(
    root,
    text="STUDENT MANAGEMENT SYSTEM",
    font=("Arial", 20, "bold"),
    bg="#1f4e79",
    fg="white",
    pady=15
)
heading.pack(fill="x")

# Input fields
frame = tk.Frame(root, bg="#eaf2f8")
frame.pack(pady=15)

tk.Label(frame, text="Student ID:", bg="#eaf2f8").grid(row=0, column=0, padx=10, pady=8)
id_entry = tk.Entry(frame, width=25)
id_entry.grid(row=0, column=1)

tk.Label(frame, text="Name:", bg="#eaf2f8").grid(row=1, column=0, padx=10, pady=8)
name_entry = tk.Entry(frame, width=25)
name_entry.grid(row=1, column=1)

tk.Label(frame, text="Course:", bg="#eaf2f8").grid(row=2, column=0, padx=10, pady=8)
course_entry = tk.Entry(frame, width=25)
course_entry.grid(row=2, column=1)

tk.Label(frame, text="Marks:", bg="#eaf2f8").grid(row=3, column=0, padx=10, pady=8)
marks_entry = tk.Entry(frame, width=25)
marks_entry.grid(row=3, column=1)

# Clear input fields
def clear_fields():
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)
    marks_entry.delete(0, tk.END)


# View all students
def view_students():
    for item in table.get_children():
        table.delete(item)

    cursor.execute("SELECT * FROM students")
    records = cursor.fetchall()

    for record in records:
        table.insert("", tk.END, values=record)


# Add student
def add_student():
    student_id = id_entry.get().strip()
    name = name_entry.get().strip()
    course = course_entry.get().strip()
    marks = marks_entry.get().strip()

    if not student_id or not name or not course or not marks:
        messagebox.showwarning("Warning", "Please fill all fields")
        return

    try:
        marks = float(marks)

        if not 0 <= marks <= 100:
            messagebox.showwarning("Warning", "Marks must be between 0 and 100")
            return

        cursor.execute(
            "INSERT INTO students VALUES (?, ?, ?, ?)",
            (student_id, name, course, marks)
        )
        conn.commit()

        messagebox.showinfo("Success", "Student added successfully!")
        clear_fields()
        view_students()

    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Student ID already exists")

    except ValueError:
        messagebox.showerror("Error", "Enter valid marks")
# Select student from table
def select_student(event):
    selected = table.focus()

    if selected:
        values = table.item(selected, "values")
        clear_fields()

        id_entry.insert(0, values[0])
        name_entry.insert(0, values[1])
        course_entry.insert(0, values[2])
        marks_entry.insert(0, values[3])


# Search student
def search_student():
    student_id = id_entry.get().strip()

    if not student_id:
        messagebox.showwarning("Warning", "Enter Student ID")
        return

    cursor.execute(
        "SELECT * FROM students WHERE id=?",
        (student_id,)
    )
    record = cursor.fetchone()

    for item in table.get_children():
        table.delete(item)

    if record:
        table.insert("", tk.END, values=record)
    else:
        messagebox.showinfo("Result", "Student not found")


# Update student
def update_student():
    student_id = id_entry.get().strip()
    name = name_entry.get().strip()
    course = course_entry.get().strip()
    marks = marks_entry.get().strip()

    if not student_id or not name or not course or not marks:
        messagebox.showwarning("Warning", "Please fill all fields")
        return

    try:
        marks = float(marks)

        if not 0 <= marks <= 100:
            messagebox.showwarning("Warning", "Marks must be between 0 and 100")
            return

        cursor.execute(
            "UPDATE students SET name=?, course=?, marks=? WHERE id=?",
            (name, course, marks, student_id)
        )
        conn.commit()

        if cursor.rowcount == 0:
            messagebox.showinfo("Result", "Student not found")
        else:
            messagebox.showinfo("Success", "Student updated!")
            clear_fields()
            view_students()

    except ValueError:
        messagebox.showerror("Error", "Enter valid marks")
# Delete student
def delete_student():
    student_id = id_entry.get().strip()

    if not student_id:
        messagebox.showwarning("Warning", "Enter Student ID")
        return

    answer = messagebox.askyesno(
        "Confirm",
        "Do you want to delete this student?"
    )

    if answer:
        cursor.execute(
            "DELETE FROM students WHERE id=?",
            (student_id,)
        )
        conn.commit()

        if cursor.rowcount == 0:
            messagebox.showinfo("Result", "Student not found")
        else:
            messagebox.showinfo("Success", "Student deleted!")
            clear_fields()
            view_students()


# Buttons
button_frame = tk.Frame(root, bg="#eaf2f8")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add", width=12, command=add_student).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="View", width=12, command=view_students).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Search", width=12, command=search_student).grid(row=0, column=2, padx=5)

tk.Button(button_frame, text="Update", width=12, command=update_student).grid(row=1, column=0, padx=5, pady=8)
tk.Button(button_frame, text="Delete", width=12, command=delete_student).grid(row=1, column=1, padx=5, pady=8)
tk.Button(button_frame, text="Clear", width=12, command=clear_fields).grid(row=1, column=2, padx=5, pady=8)

# Student records table
table_frame = tk.Frame(root)
table_frame.pack(pady=15, fill="both", expand=True, padx=15)

columns = ("ID", "Name", "Course", "Marks")

table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

for column in columns:
    table.heading(column, text=column)
    table.column(column, width=150)

table.pack(fill="both", expand=True)

# Select a record
table.bind("<<TreeviewSelect>>", select_student)

# Display existing records
view_students()

# Close application safely
def close_app():
    conn.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", close_app)

# Run application
root.mainloop()
