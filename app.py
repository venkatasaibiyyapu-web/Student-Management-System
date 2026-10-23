from flask import Flask, render_template, request
import sqlite3
from database import get_db_connection, create_table

app = Flask(__name__)

create_table()


@app.route("/")
def home():
    conn = get_db_connection()

    total_students = conn.execute(
        "SELECT COUNT(*) FROM students"
    ).fetchone()[0]

    department_stats = conn.execute("""
    SELECT department, COUNT(*) AS total
    FROM students
    GROUP BY department
    ORDER BY department
""").fetchall()

    conn.close()

    return render_template(
        "index.html",
        total_students=total_students,
        department_stats=department_stats
    )


# ADD STUDENT
@app.route("/add_student", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        roll = request.form.get("roll", "").strip()
        email = request.form.get("email", "").strip()
        department = request.form.get("department", "").strip()

        if not all([name, roll, email, department]):
            return "Please fill all fields!"

        if not roll.isdigit():
            return "Roll number must contain only numbers!"

        conn = get_db_connection()

        existing = conn.execute(
            "SELECT id FROM students WHERE roll = ?",
            (roll,)
        ).fetchone()

        if existing:
            conn.close()
            return "Roll Number Already Exists!"

        conn.execute(
            """INSERT INTO students (name, roll, email, department)
               VALUES (?, ?, ?, ?)""",
            (name, roll, email, department)
        )

        conn.commit()
        conn.close()

        return "Student Added Successfully!"

    return render_template("add_student.html")


# VIEW STUDENTS
@app.route("/view_students")
def view_students():
    conn = get_db_connection()

    students = conn.execute(
        "SELECT * FROM students ORDER BY id"
    ).fetchall()

    conn.close()

    return render_template(
        "view_students.html",
        students=students
    )


# SEARCH STUDENT
@app.route("/search_student", methods=["GET", "POST"])
def search_student():
    student = None
    message = ""

    if request.method == "POST":
        roll = request.form.get("roll", "").strip()

        conn = get_db_connection()

        student = conn.execute(
            "SELECT * FROM students WHERE roll = ?",
            (roll,)
        ).fetchone()

        conn.close()

        if student is None:
            message = "Student Not Found!"

    return render_template(
        "search_student.html",
        student=student,
        message=message
    )


# UPDATE STUDENT
@app.route("/update_student", methods=["GET", "POST"])
def update_student():
    if request.method == "POST":
        roll = request.form.get("roll", "").strip()
        new_roll = request.form.get("new_roll", "").strip()
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        department = request.form.get("department", "").strip()

        if not all([roll, name, email, department]):
            return "Please fill all required fields!"

        if new_roll and not new_roll.isdigit():
            return "New roll number must contain only numbers!"

        conn = get_db_connection()

        existing = conn.execute(
            "SELECT id FROM students WHERE roll = ?",
            (roll,)
        ).fetchone()

        if existing is None:
            conn.close()
            return "Student Not Found!"

        final_roll = new_roll if new_roll else roll

        duplicate = conn.execute(
            "SELECT id FROM students WHERE roll = ? AND id != ?",
            (final_roll, existing["id"])
        ).fetchone()

        if duplicate:
            conn.close()
            return "New Roll Number Already Exists!"

        conn.execute(
            """UPDATE students
               SET name = ?, roll = ?, email = ?, department = ?
               WHERE id = ?""",
            (name, final_roll, email, department, existing["id"])
        )

        conn.commit()
        conn.close()

        return "Student Updated Successfully!"

    return render_template("update_student.html")


# DELETE STUDENT
@app.route("/delete_student", methods=["GET", "POST"])
def delete_student():
    if request.method == "POST":
        roll = request.form.get("roll", "").strip()

        conn = get_db_connection()

        cursor = conn.execute(
            "DELETE FROM students WHERE roll = ?",
            (roll,)
        )

        deleted = cursor.rowcount

        conn.commit()
        conn.close()

        if deleted > 0:
            return "Student Deleted Successfully!"

        return "Student Not Found!"

    return render_template("delete_student.html")


if __name__ == "__main__":
    app.run(debug=True)