import sqlite3

conn = sqlite3.connect("company.db")
cursor = conn.cursor()

question = input("Ask DB Agent: ")

if "all employees" in question.lower():
    cursor.execute("SELECT * FROM employees")
    print(cursor.fetchall())

elif "count" in question.lower():
    cursor.execute("SELECT COUNT(*) FROM employees")
    print(cursor.fetchone())

else:
    print("I don't know that query yet.")

conn.close()
