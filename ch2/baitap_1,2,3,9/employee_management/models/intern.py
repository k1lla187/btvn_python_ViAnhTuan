from .employee import Employee

class Intern(Employee):
    """
    Lớp đại diện cho Thực tập sinh (Intern).
    Kế thừa từ lớp Employee.
    """
    def __init__(self, emp_id: str, name: str, age: int, base_salary: float, major: str):
        """
        Khởi tạo đối tượng Intern.
        
        Args:
            major (str): Chuyên ngành đào tạo.
        """
        super().__init__(emp_id, name, age, base_salary)
        self._major: str = major

    @property
    def major(self) -> str:
        """Trả về chuyên ngành của thực tập sinh."""
        return self._major

    def calculate_salary(self) -> float:
        """
        Tính lương cho Intern.
        Công thức: 80% Lương CB + Thưởng hiệu suất (tối đa 1,000,000)
        """
        return (self.base_salary * 0.8) + (self.performance_score / 10) * 1000000

    def __str__(self) -> str:
        return f"[Intern] " + super().__str__() + f" | Chuyên ngành: {self._major}"
