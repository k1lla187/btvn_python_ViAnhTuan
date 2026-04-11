import json
import os
from typing import List, Dict, Union, Optional
from models.employee import Employee
from models.manager import Manager
from models.developer import Developer
from models.intern import Intern
from exceptions.employee_exceptions import EmployeeNotFoundError, DuplicateEmployeeError

class Company:
    """
    Lớp quản lý tập hợp các nhân viên và các nghiệp vụ liên quan đến công ty.
    """
    def __init__(self, name: str = "Công ty ABC"):
        """
        Khởi tạo đối tượng Company.
        
        Args:
            name (str): Tên công ty.
        """
        self.name: str = name
        self.employees: Dict[str, Employee] = {} # emp_id -> Employee object

    def add_employee(self, employee: Employee) -> None:
        """
        Thêm nhân viên mới vào hệ thống.
        
        Args:
            employee (Employee): Đối tượng nhân viên cần thêm.
            
        Raises:
            DuplicateEmployeeError: Nếu mã nhân viên đã tồn tại.
        """
        if employee.emp_id in self.employees:
            raise DuplicateEmployeeError(employee.emp_id)
        self.employees[employee.emp_id] = employee

    def remove_employee(self, emp_id: str) -> None:
        """
        Xóa nhân viên khỏi hệ thống.
        
        Args:
            emp_id (str): Mã nhân viên cần xóa.
            
        Raises:
            EmployeeNotFoundError: Nếu không tìm thấy mã nhân viên.
        """
        if emp_id not in self.employees:
            raise EmployeeNotFoundError(emp_id)
        del self.employees[emp_id]

    def find_employee_by_id(self, emp_id: str) -> Employee:
        """
        Tìm kiếm nhân viên theo ID.
        
        Args:
            emp_id (str): Mã nhân viên.
            
        Returns:
            Employee: Đối tượng nhân viên tìm thấy.
            
        Raises:
            EmployeeNotFoundError: Nếu không tìm thấy.
        """
        if emp_id not in self.employees:
            raise EmployeeNotFoundError(emp_id)
        return self.employees[emp_id]

    def find_employees_by_name(self, name: str) -> List[Employee]:
        """
        Tìm kiếm nhân viên theo tên (gần đúng).
        
        Args:
            name (str): Tên hoặc một phần tên cần tìm.
            
        Returns:
            List[Employee]: Danh sách nhân viên thỏa mãn.
            
        Raises:
            EmployeeNotFoundError: Nếu không tìm thấy kết quả nào.
        """
        results = [e for e in self.employees.values() if name.lower() in e.name.lower()]
        if not results:
            raise EmployeeNotFoundError(name)
        return results

    def get_all_employees(self) -> List[Employee]:
        """Trả về danh sách tất cả nhân viên."""
        return list(self.employees.values())

    def get_employees_by_type(self, emp_type: str) -> List[Employee]:
        """
        Lọc nhân viên theo loại (Manager, Developer, Intern).
        
        Args:
            emp_type (str): Tên lớp đối tượng cần lọc.
        """
        return [e for e in self.employees.values() if e.__class__.__name__.lower() == emp_type.lower()]

    def get_top_performers(self) -> List[Employee]:
        """Trả về danh sách nhân viên sắp xếp theo điểm hiệu suất giảm dần."""
        return sorted(self.employees.values(), key=lambda x: x.performance_score, reverse=True)

    def calculate_total_payroll(self) -> float:
        """Tính tổng quỹ lương của toàn công ty."""
        return sum(e.calculate_salary() for e in self.employees.values())

    def get_top_3_salaries(self) -> List[Employee]:
        """Trả về Top 3 nhân viên có mức lương cao nhất."""
        return sorted(self.employees.values(), key=lambda x: x.calculate_salary(), reverse=True)[:3]

    def promote_employee(self, emp_id: str, new_type: str, extra_info: Union[str, int]) -> Employee:
        """
        Thăng chức hoặc chuyển đổi loại nhân viên.
        
        Args:
            emp_id (str): Mã nhân viên.
            new_type (str): Loại mới ('Developer' hoặc 'Manager').
            extra_info: Thông tin bổ sung (ngôn ngữ lập trình hoặc quy mô team).
            
        Returns:
            Employee: Đối tượng nhân viên mới sau khi thăng chức.
        """
        old_emp = self.find_employee_by_id(emp_id)
        
        if new_type == 'Developer':
            new_emp = Developer(old_emp.emp_id, old_emp.name, old_emp.age, old_emp.base_salary, str(extra_info))
        elif new_type == 'Manager':
            new_emp = Manager(old_emp.emp_id, old_emp.name, old_emp.age, old_emp.base_salary, int(extra_info))
        else:
            raise ValueError("Loại nhân viên mới không hợp lệ")

        # Sao chép dữ liệu hiện có
        new_emp.performance_score = old_emp.performance_score
        for proj in old_emp.projects:
            new_emp.add_project(proj)
            
        self.employees[emp_id] = new_emp
        return new_emp

    def save_to_json(self, filepath: str) -> None:
        """Lưu toàn bộ danh sách nhân viên vào tệp JSON."""
        data = []
        for emp in self.employees.values():
            emp_data = {
                'type': emp.__class__.__name__,
                'id': emp.emp_id,
                'name': emp.name,
                'age': emp.age,
                'salary': emp.base_salary,
                'performance': emp.performance_score,
                'projects': emp.projects
            }
            if isinstance(emp, Manager):
                emp_data['team_size'] = emp.team_size
            elif isinstance(emp, Developer):
                emp_data['language'] = emp.programming_language
            elif isinstance(emp, Intern):
                emp_data['major'] = emp.major
            data.append(emp_data)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_from_json(self, filepath: str) -> None:
        """Tải danh sách nhân viên từ tệp JSON."""
        if not os.path.exists(filepath):
            return
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            self.employees = {}
            for item in data:
                etype = item['type']
                if etype == 'Manager':
                    emp = Manager(item['id'], item['name'], item['age'], item['salary'], item['team_size'])
                elif etype == 'Developer':
                    emp = Developer(item['id'], item['name'], item['age'], item['salary'], item['language'])
                elif etype == 'Intern':
                    emp = Intern(item['id'], item['name'], item['age'], item['salary'], item['major'])
                else:
                    continue
                
                emp.performance_score = item['performance']
                for proj in item['projects']:
                    emp.add_project(proj)
                
                self.employees[emp.emp_id] = emp
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Lỗi khi đọc file dữ liệu: {e}")
