from .employee import Employee

class Manager(Employee):
    """
    Lớp đại diện cho cấp bậc Quản lý (Manager).
    Kế thừa từ lớp Employee.
    """
    def __init__(self, emp_id: str, name: str, age: int, base_salary: float, team_size: int):
        """
        Khởi tạo đối tượng Manager.
        
        Args:
            team_size (int): Số lượng nhân viên mà manager quản lý.
        """
        super().__init__(emp_id, name, age, base_salary)
        self._team_size: int = team_size

    @property
    def team_size(self) -> int:
        """Trả về quy mô team quản lý."""
        return self._team_size

    def calculate_salary(self) -> float:
        """
        Tính lương cho Manager.
        Công thức: Lương CB + (Team * 5,000,000) + Thưởng hiệu suất (50% lương CB)
        """
        allowance = self._team_size * 5000000
        performance_bonus = (self.performance_score / 10) * self.base_salary * 0.5
        return self.base_salary + allowance + performance_bonus

    def __str__(self) -> str:
        return f"[Manager] " + super().__str__() + f" | Team: {self._team_size}"
