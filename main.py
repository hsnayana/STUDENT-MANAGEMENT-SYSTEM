import sqlite3

# Connect to database
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Create student table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id TEXT PRIMARY KEY,
    name TEXT,
    course TEXT,
    marks REAL
)
""")

conn.commit()

while True:
    print("\n=== STUDENT MANAGEMENT SYSTEM ===")
    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        student_id = input("Enter Student ID: ")
        name = input("Enter Student Name: ")
        course = input("Enter Course: ")
        marks = float(input("Enter Marks: "))

        cursor.execute(
            "INSERT INTO students VALUES (?, ?, ?, ?)",
            (student_id, name, course, marks)
        )
        conn.commit()
        print("Student Added Successfully!")

    elif choice == "2":
        cursor.execute("SELECT * FROM students")
        records = cursor.fetchall()

        if len(records) == 0:
            print("No student records found.")
        else:
            for student in records:
                print(student)

    elif choice == "3":
        search_id = input("Enter Student ID: ")

        cursor.execute(
            "SELECT * FROM students WHERE id = ?",
            (search_id,)
        )
        student = cursor.fetchone()

        if student:
            print("Student Found:", student)
        else:
            print("Student Not Found!")

    elif choice == "4":
        update_id = input("Enter Student ID: ")
        name = input("Enter New Name: ")
        course = input("Enter New Course: ")
        marks = float(input("Enter New Marks: "))

        cursor.execute("""
        UPDATE students
        SET name = ?, course = ?, marks = ?
        WHERE id = ?
        """, (name, course, marks, update_id))

        conn.commit()

        if cursor.rowcount > 0:
            print("Student Updated Successfully!")
        else:
            print("Student Not Found!")

    elif choice == "5":
        delete_id = input("Enter Student ID: ")

        cursor.execute(
            "DELETE FROM students WHERE id = ?",
            (delete_id,)
        )
        conn.commit()

        if cursor.rowcount > 0:
            print("Student Deleted Successfully!")
        else:
            print("Student Not Found!")

    elif choice == "6":
        print("Thank you for using the system!")
        break

    else:
        print("Invalid choice!")

conn.close()
