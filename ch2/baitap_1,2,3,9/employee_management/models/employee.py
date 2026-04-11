from abc import ABC, abstractmethod
from typing import List

class Employee(ABC):
    """
    Lớp trừu tượng đại diện cho một nhân viên trong hệ thống.
    Đây là lớp cha (Base Class) cho tất cả các loại nhân viên khác.
    """
    def __init__(self, emp_id: str, name: str, age: int, base_salary: float):
        """
        Khởi tạo một đối tượng Employee.
        
        Args:
            emp_id (str): Mã định danh duy nhất của nhân viên.
            name (str): Tên đầy đủ của nhân viên.
            age (int): Tuổi của nhân viên.
            base_salary (float): Mức lương cơ bản ban đầu.
        """
        self._emp_id: str = emp_id
        self._name: str = name
        self._age: int = age
        self._base_salary: float = base_salary
        self._performance_score: float = 0.0
        self._projects: List[str] = []

    @property
    def emp_id(self) -> str:
        """Trả về mã nhân viên. (Read-only)"""
        return self._emp_id
    
    @property
    def name(self) -> str:
        """Trả về tên nhân viên. (Read-only)"""
        return self._name
    
    @property
    def age(self) -> int:
        """Trả về tuổi của nhân viên. (Read-only)"""
        return self._age
    
    @property
    def base_salary(self) -> float:
        """Trả về lương cơ bản của nhân viên."""
        return self._base_salary
    
    @base_salary.setter
    def base_salary(self, value: float):
        """Cập nhật lương cơ bản."""
        self._base_salary = value

    @property
    def performance_score(self) -> float:
        """Trả về điểm hiệu suất (0-10)."""
        return self._performance_score
    
    @performance_score.setter
    def performance_score(self, value: float):
        """
        Cập nhật điểm hiệu suất.
        
        Raises:
            ValueError: Nếu điểm không nằm trong khoảng [0, 10].
        """
        if 0 <= value <= 10:
            self._performance_score = value
        else:
            raise ValueError("Điểm hiệu suất phải từ 0 đến 10")

    @property
    def projects(self) -> List[str]:
        """Trả về danh sách các dự án tham gia."""
        return self._projects

    @abstractmethod
    def calculate_salary(self) -> float:
        """
        Phương thức trừu tượng để tính tổng lương. 
        Mỗi lớp con phải ghi đè (override) phương thức này.
        """
        pass

    def add_project(self, project_name: str) -> None:
        """
        Thêm một dự án mới cho nhân viên.
        
        Args:
            project_name (str): Tên dự án.
            
        Raises:
            ProjectAllocationError: Nếu đã tham gia quá 5 dự án.
        """
        if len(self._projects) >= 5:
            from exceptions.employee_exceptions import ProjectAllocationError
            raise ProjectAllocationError()
        if project_name and project_name not in self._projects:
            self._projects.append(project_name)

    def remove_project(self, project_name: str) -> None:
        """Xóa một dự án khỏi danh sách tham gia."""
        if project_name in self._projects:
            self._projects.remove(project_name)

    def __str__(self) -> str:
        """Trả về chuỗi đại diện của nhân viên."""
        return f"ID: {self._emp_id} | Tên: {self._name} | Tuổi: {self._age} | Lương CB: {self._base_salary:,.0f} | Điểm HS: {self._performance_score}"
