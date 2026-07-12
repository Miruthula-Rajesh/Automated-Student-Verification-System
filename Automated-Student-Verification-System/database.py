# database.py

import sqlite3
from datetime import datetime

DB_NAME = "students.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reg_no TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        department TEXT NOT NULL,
        year TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        status TEXT DEFAULT 'Pending'
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS verification_logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reg_no TEXT,
        email TEXT,
        result TEXT,
        verified_at TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_sample_students():
    conn = get_connection()
    cursor = conn.cursor()

    students = [
        ("221401001", "Arun Kumar", "CSE", "Final Year", "arun@gmail.com", "Verified"),
        ("221401002", "Priya S", "CSE", "Final Year", "priya@gmail.com", "Pending"),
        ("221401003", "Rahul R", "IT", "Final Year", "rahul@gmail.com", "Verified"),
        ("221401004", "Divya M", "ECE", "Third Year", "divya@gmail.com", "Pending"),
        ("221401005", "Kavin P", "CSE", "Second Year", "kavin@gmail.com", "Verified")
    ]

    for student in students:
        try:
            cursor.execute("""
            INSERT INTO students
            (reg_no,name,department,year,email,status)
            VALUES(?,?,?,?,?,?)
            """, student)
        except:
            pass

    conn.commit()
    conn.close()


def get_all_students():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students ORDER BY id DESC")
    students = cursor.fetchall()

    conn.close()

    return students


def get_student(reg_no):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students WHERE reg_no=?", (reg_no,))
    student = cursor.fetchone()

    conn.close()

    return student


def add_student(reg_no, name, department, year, email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO students
    (reg_no,name,department,year,email)
    VALUES(?,?,?,?,?)
    """, (reg_no, name, department, year, email))

    conn.commit()
    conn.close()


def update_status(reg_no, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE students
    SET status=?
    WHERE reg_no=?
    """, (status, reg_no))

    conn.commit()
    conn.close()


def delete_student(reg_no):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students WHERE reg_no=?", (reg_no,))

    conn.commit()
    conn.close()


def search_student(keyword):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM students
    WHERE
    name LIKE ?
    OR
    reg_no LIKE ?
    OR
    department LIKE ?
    """, (
        "%" + keyword + "%",
        "%" + keyword + "%",
        "%" + keyword + "%"
    ))

    result = cursor.fetchall()

    conn.close()

    return result


def log_verification(reg_no, email, result):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO verification_logs
    (reg_no,email,result,verified_at)
    VALUES(?,?,?,?)
    """, (
        reg_no,
        email,
        result,
        datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_logs():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM verification_logs
    ORDER BY id DESC
    """)

    logs = cursor.fetchall()

    conn.close()

    return logs


if __name__ == "__main__":
    create_tables()
    insert_sample_students()
    print("Database Created Successfully.")