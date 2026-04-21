import sqlite3

# Kết nối đến cơ sở dữ liệu
conn = sqlite3.connect('company.db')
cursor = conn.cursor()

# Tạo các bảng nếu chưa tồn tại
cursor.execute('''CREATE TABLE IF NOT EXISTS department (
    department_id INTEGER PRIMARY KEY,
    department_name TEXT,
    location TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS employee (
    employee_id INTEGER PRIMARY KEY,
    name TEXT,
    job TEXT,
    department_id INTEGER,
    FOREIGN KEY(department_id) REFERENCES department(department_id)
)''')

# A) Lấy ra danh sách các nhân viên có chức vụ là MANAGER
cursor.execute("SELECT * FROM employee WHERE job = 'MANAGER'")
managers = cursor.fetchall()
print("Danh sách Manager:", managers)

# Thêm dữ liệu mẫu vào database
# Xóa dữ liệu cũ để chạy lại script nhiều lần
cursor.execute("DELETE FROM employee")
cursor.execute("DELETE FROM department")

# Thêm phòng ban mẫu
departments = [
    (10, 'Accounting', 'New York'),
    (20, 'Research', 'Dallas'),
    (30, 'Sales', 'Chicago'),
    (40, 'Operations', 'Boston'),
    (50, 'IT Department', 'Hanoi')
]
for dept in departments:
    cursor.execute("INSERT INTO department VALUES (?, ?, ?)", dept)

# Thêm nhân viên mẫu (bao gồm MANAGER)
employees = [
    (7839, 'KING', 'PRESIDENT', 10),
    (7566, 'JONES', 'MANAGER', 20),
    (7788, 'SCOTT', 'ANALYST', 20),
    (7876, 'ADAMS', 'CLERK', 20),
    (7902, 'FORD', 'ANALYST', 20),
    (7369, 'SMITH', 'CLERK', 20),
    (7844, 'TURNER', 'SALESMAN', 30),
    (7654, 'MARTIN', 'SALESMAN', 30),
    (7521, 'WARD', 'SALESMAN', 30),
    (7698, 'BLAKE', 'MANAGER', 30),
    (7499, 'ALLEN', 'SALESMAN', 30),
    (7782, 'CLARK', 'MANAGER', 10),
    (7934, 'MILLER', 'CLERK', 10)
]
for emp in employees:
    cursor.execute("INSERT INTO employee VALUES (?, ?, ?, ?)", emp)

print("\n=== Dữ liệu mẫu đã được thêm vào ===\n")

# A) Lấy ra danh sách các nhân viên có chức vụ là MANAGER
cursor.execute("SELECT * FROM employee WHERE job = 'MANAGER'")
managers = cursor.fetchall()
print("A) Danh sách Manager:")
for manager in managers:
    print(f"   ID: {manager[0]}, Tên: {manager[1]}, Chức vụ: {manager[2]}, Phòng ban: {manager[3]}")

# B) Insert thông tin phòng làm việc thực tế vào bảng department
# Giả sử bảng có các cột: department_id, department_name, location
cursor.execute("INSERT OR REPLACE INTO department (department_id, department_name, location) VALUES (?, ?, ?)", 
               (50, 'IT Department', 'Hanoi'))
print("\nB) Đã thêm phòng ban IT Department (ID: 50, Hanoi)")

# C) Insert thông tin thực tế của bản thân vào bảng employee
# Giả sử bảng có các cột: employee_id, name, job, department_id
cursor.execute("INSERT OR REPLACE INTO employee (employee_id, name, job, department_id) VALUES (?, ?, ?, ?)", 
               (999, 'Nguyen Van A', 'Developer', 50))
print("C) Đã thêm nhân viên: ID=999, Tên=Nguyen Van A, Chức vụ=Developer, Phòng ban=50")

# D) Cập nhật thông tin của nhân viên tên là CLARK thành thông tin cá nhân của bạn
cursor.execute("UPDATE employee SET name = ?, job = ? WHERE name = 'CLARK'", 
               ('Nguyen Van A', 'Developer'))
print("D) Đã cập nhật nhân viên CLARK thành: Tên=Nguyen Van A, Chức vụ=Developer")

# E) Xóa thông tin của nhân viên có tên là MILLER trong bảng employee
cursor.execute("DELETE FROM employee WHERE name = 'MILLER'")
print("E) Đã xóa nhân viên MILLER khỏi cơ sở dữ liệu")

# Hiển thị dữ liệu cuối cùng
print("\n=== Danh sách nhân viên cuối cùng ===")
cursor.execute("SELECT e.employee_id, e.name, e.job, d.department_name FROM employee e LEFT JOIN department d ON e.department_id = d.department_id ORDER BY e.employee_id")
employees_final = cursor.fetchall()
for emp in employees_final:
    print(f"ID: {emp[0]}, Tên: {emp[1]}, Chức vụ: {emp[2]}, Phòng ban: {emp[3]}")

# Lưu thay đổi và đóng kết nối
conn.commit()
conn.close()