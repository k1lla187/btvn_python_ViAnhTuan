from .employee import Employee

class Developer(Employee):
    """
    Lớp đại diện cho Lập trình viên (Developer).
    Kế thừa từ lớp Employee.
    """
    def __init__(self, emp_id: str, name: str, age: int, base_salary: float, programming_language: str):
        """
        Khởi tạo đối tượng Developer.
        
        Args:
            programming_language (str): Ngôn ngữ lập trình chuyên môn.
        """
        super().__init__(emp_id, name, age, base_salary)
        self._programming_language: str = programming_language

    @property
    def programming_language(self) -> str:
        """Trả về ngôn ngữ lập trình của developer."""
        return self._programming_language

    def calculate_salary(self) -> float:
        """
        Tính lương cho Developer.
        Công thức: Lương CB + 2,000,000 (Phụ cấp ngôn ngữ) + Thưởng hiệu suất (30% lương CB)
        """
        language_bonus = 2000000
        performance_bonus = (self.performance_score / 10) * self.base_salary * 0.3
        return self.base_salary + language_bonus + performance_bonus

    def __str__(self) -> str:
        return f"[Developer] " + super().__str__() + f" | Ngôn ngữ: {self._programming_language}"
