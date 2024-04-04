-- Create employees table if it doesn't exist
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    surname TEXT,
    age INTEGER,
    working_since TEXT,
    position TEXT,
    salary REAL,
    special_notes TEXT
);

-- Insert employee data into employees table, avoiding duplicates
-- ? represent the values to be inserted
INSERT INTO employees (name, surname, age, working_since, position, salary, special_notes)
SELECT ?, ?, ?, ?, ?, ?, ?
-- Duplicate check: Replace each ? with the corresponding value to check for duplicates
WHERE NOT EXISTS (
    SELECT 1 FROM employees 
    WHERE name = ? AND surname = ? AND working_since = ?
);

-- Retrieve all rows from employees table

SELECT * FROM employees;

-- Search for employee IDs based on name and surname
-- Replace each ? with the corresponding name and surname
SELECT id FROM employees WHERE name = ? AND surname = ?;

-- Update a specific column of an employee record
-- Replace column with the name of the column to be updated, and ? with the new value
UPDATE employees SET column = ? WHERE id = ?;

-- Delete an employee record based on their ID
-- Replace ? with the employee ID
DELETE FROM employees WHERE id = ?;
