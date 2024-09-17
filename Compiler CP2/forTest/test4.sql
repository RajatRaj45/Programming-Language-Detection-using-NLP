CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    name VARCHAR(50),
    age INT,
    department VARCHAR(50),
    salary DECIMAL(10, 2)
);

INSERT INTO employees (employee_id, name, age, department, salary)
VALUES
    (1, 'John Doe', 30, 'Engineering', 60000.00),
    (2, 'Jane Smith', 25, 'Marketing', 45000.00),
    (3, 'Samuel Adams', 40, 'Finance', 75000.00),
    (4, 'Emily Johnson', 35, 'HR', 55000.00);

SELECT * FROM employees;

UPDATE employees
SET salary = 48000.00
WHERE employee_id = 2;

DELETE FROM employees
WHERE employee_id = 3;

SELECT * FROM employees;
