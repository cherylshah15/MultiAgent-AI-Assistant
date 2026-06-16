import sqlite3

conn = sqlite3.connect("company.db")
cursor = conn.cursor()

question = input("Ask DB Agent: ").lower()

if "all employees" in question:
    cursor.execute("SELECT * FROM employees")
    print(cursor.fetchall())

elif "count" in question or "how many" in question:
    cursor.execute("SELECT COUNT(*) FROM employees")
    print(f"Total Employees: {cursor.fetchone()[0]}")

elif "ai" in question:
    cursor.execute(
        "SELECT name FROM employees WHERE department='AI'"
    )
    print(cursor.fetchall())

elif "departments" in question:
    cursor.execute(
        "SELECT DISTINCT department FROM employees"
    )
    print(cursor.fetchall())

else:
    print("Sorry, I don't understand that query yet.")

conn.close()