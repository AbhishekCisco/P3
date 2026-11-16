from connection import getSqliteConnection


def main():
    departments = [
        (1, "Computer Science"),
        (2, "Electrical Engineering"),
        (3, "Mechanical Engineering"),
        (4, "Mathematics"),
        (5, "Physics"),
    ]
    students = [
        (101, "Alice Johnson", 1),
        (102, "Bob Smith", 2),
        (103, "Carol Lee", 3),
        (104, "David Brown", 4),
        (105, "Emily White", 5),
    ]

    connection = getSqliteConnection()
    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute("DROP TABLE IF EXISTS students")
            cursor.execute("DROP TABLE IF EXISTS departments")
            cursor.execute("""
                CREATE TABLE departments (
                    DepartmentId INTEGER PRIMARY KEY,
                    DepartmentName TEXT NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE students (
                    StudentId INTEGER PRIMARY KEY,
                    StudentName TEXT NOT NULL,
                    DepartmentId INTEGER,
                    FOREIGN KEY (DepartmentId)
                        REFERENCES departments (DepartmentId)
                )
            """)
            cursor.executemany(
                "INSERT INTO departments (DepartmentId, DepartmentName) VALUES (?, ?)",
                departments,
            )
            department_count = cursor.rowcount
            cursor.executemany(
                "INSERT INTO students (StudentId, StudentName, DepartmentId) "
                "VALUES (?, ?, ?)",
                students,
            )
            student_count = cursor.rowcount
    finally:
        connection.close()

    print(f"Inserted {department_count} rows into departments.")
    print(f"Inserted {student_count} rows into students.")


if __name__ == "__main__":
    main()
