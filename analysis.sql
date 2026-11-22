-- Run these statements in a SQLite query tool after running main.py.

-- 1. Display all student records.
SELECT * FROM students ORDER BY student_id;

-- 2. Find students scoring above 80.
SELECT student_id, student_name, department, marks
FROM students
WHERE marks > 80
ORDER BY marks DESC;

-- 3. Calculate average marks department-wise.
SELECT department, ROUND(AVG(marks), 2) AS average_marks
FROM students
GROUP BY department
ORDER BY average_marks DESC;

-- 4. Find the highest and lowest marks.
SELECT MAX(marks) AS highest_marks, MIN(marks) AS lowest_marks
FROM students;

-- 5. Count students in each department.
SELECT department, COUNT(*) AS student_count
FROM students
GROUP BY department
ORDER BY student_count DESC;

-- 6. Find students with attendance below 75 percent.
SELECT student_id, student_name, department, attendance
FROM students
WHERE attendance < 75
ORDER BY attendance;
