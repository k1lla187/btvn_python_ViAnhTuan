import re
from exceptions.employee_exceptions import InvalidAgeError, InvalidSalaryError

class Validators:
    """
    Cung cấp các phương thức tĩnh để kiểm tra tính hợp lệ của dữ liệu đầu vào.
    """
    @staticmethod
    def validate_age(age: int) -> bool:
        """
        Kiểm tra tuổi nhân viên có nằm trong khoảng 18-65 hay không.
        
        Args:
            age (int): Tuổi cần kiểm tra.
            
        Returns:
            bool: True nếu hợp lệ.
            
        Raises:
            InvalidAgeError: Nếu tuổi nằm ngoài khoảng quy định.
        """
        if not (18 <= age <= 65):
            raise InvalidAgeError(age)
        return True

    @staticmethod
    def validate_salary(salary: float) -> bool:
        """
        Kiểm tra lương có phải số dương hay không.
        
        Raises:
            InvalidSalaryError: Nếu lương <= 0.
        """
        if salary <= 0:
            raise InvalidSalaryError(salary)
        return True

    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Kiểm tra định dạng email bằng Regex.
        
        Args:
            email (str): Chuỗi email cần kiểm tra.
        """
        # Biểu thức chính quy cho email đơn giản
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            raise ValueError("Email sai định dạng (thiếu @ hoặc tên miền)")
        return True
