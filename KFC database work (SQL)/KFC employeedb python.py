import sqlite3


def create_employee_db():
    with sqlite3.connect('kfc_employee.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS employees
                     (id INTEGER PRIMARY KEY, name TEXT, surname TEXT, age INTEGER, working_since TEXT, position TEXT, salary REAL, special_notes TEXT)''')


def insert_employee_into_db(employee_data):
    conn = sqlite3.connect('kfc_employee.db')
    c = conn.cursor()

    # Check if employee with the same name, surname, and working since date already exists
    c.execute("SELECT * FROM employees WHERE name = ? AND surname = ? AND working_since = ?",
              (employee_data[0], employee_data[1], employee_data[3]))
    existing_employee = c.fetchone()

    if existing_employee is None:
        c.execute(
            "INSERT INTO employees (name, surname, age, working_since, position, salary, special_notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
            employee_data)
        conn.commit()
        print("Employee added successfully.")
    else:
        print("Employee already exists in the database.")

    conn.close()


def read_employee_data():
    with sqlite3.connect('kfc_employee.db') as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM employees")
        rows = c.fetchall()
        for row in rows:
            print(row)


def search_employee_id(name, surname):
    with sqlite3.connect('kfc_employee.db') as conn:
        c = conn.cursor()
        c.execute("SELECT id FROM employees WHERE name = ? AND surname = ?", (name, surname))
        employee_ids = c.fetchall()
        if employee_ids:
            print(f"Employee IDs for {name} {surname} are: {', '.join(str(id[0]) for id in employee_ids)}")
        else:
            print(f"No employee found with name {name} {surname}")



def edit_employee_info(employee_id, column, new_value):
    with sqlite3.connect('kfc_employee.db') as conn:
        c = conn.cursor()
        c.execute("UPDATE employees SET {} = ? WHERE id = ?".format(column), (new_value, employee_id))
        print("Employee information updated successfully.")


def remove_employee(employee_id):
    with sqlite3.connect('kfc_employee.db') as conn:
        c = conn.cursor()
        c.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
        print("Employee removed successfully.")


def remove_duplicates_and_adjust_ids():
    with sqlite3.connect('kfc_employee.db') as conn:
        c = conn.cursor()
        c.execute(
            "DELETE FROM employees WHERE id NOT IN (SELECT MIN(id) FROM employees GROUP BY name, surname, working_since)")
        c.execute(
            "UPDATE employees SET id = (SELECT MIN(id) FROM employees AS temp WHERE temp.name = employees.name AND temp.surname = employees.surname AND temp.working_since = employees.working_since)")


if __name__ == "__main__":
    create_employee_db()

    employees = [
        ('Yana', 'Pavlovna', 19, '2022-05-21', 'Entry-level', 28000, 'Knows Ukrainian'),
        # Employee data to add here...
    ]

    for employee in employees:
        insert_employee_into_db(employee)



    # Uncomment to perform actions like editing or removing employees
    #search_employee_id('Olena', 'Vladimirovna')
    #search_employee_id('Anna', 'Kowalska')
    #search_employee_id('Dariusz',  'Komosinski')
    #edit_employee_info(53, 'salary', '52000') # example                   EXAMPLES
    #remove_employee(id here)
    remove_duplicates_and_adjust_ids()
    read_employee_data()
