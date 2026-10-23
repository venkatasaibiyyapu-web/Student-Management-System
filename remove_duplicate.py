import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Check the exact record before deleting
cursor.execute(
    "SELECT id, name, roll, email, department FROM students WHERE id = ?",
    (5,)
)

student = cursor.fetchone()

if student is None:
    print("Student ID 5 not found.")

elif student[1:] != (
    "GOPI", "105", "GOPI@GMAIL.COM", "ECE"
):
    print("Record does not match. Deletion cancelled.")

else:
    print("Record found:", student)

    confirm = input("Type YES to delete Student ID 5: ")

    if confirm == "YES":
        cursor.execute(
            "DELETE FROM students WHERE id = ?",
            (5,)
        )
        conn.commit()
        print("Duplicate student deleted successfully!")
    else:
        print("Deletion cancelled.")

conn.close()