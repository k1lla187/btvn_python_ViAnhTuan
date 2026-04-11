from typing import List, Dict, Any

class Payroll:
    """
    Tiện ích xử lý các vấn đề liên quan đến bảng lương và thống kê dự án.
    """
    @staticmethod
    def generate_salary_report(employees: List[Any]) -> List[Dict[str, Any]]:
        """
        Tạo báo cáo lương cho danh sách nhân viên.
        
        Args:
            employees (List[Employee]): Danh sách nhân viên cần thống kê.
            
        Returns:
            List[Dict]: Danh sách từ điển chứa thông tin lương.
        """
        report = []
        for emp in employees:
            salary = emp.calculate_salary()
            report.append({
                "id": emp.emp_id,
                "name": emp.name,
                "type": emp.__class__.__name__,
                "salary": salary
            })
        return report

    @staticmethod
    def calculate_average_projects(employees: List[Any]) -> float:
        """
        Tính số lượng dự án trung bình mỗi nhân viên tham gia.
        
        Args:
            employees (List[Employee]): Danh sách nhân viên.
            
        Returns:
            float: Số lượng dự án trung bình.
        """
        if not employees: return 0.0
        total_projects = sum(len(e.projects) for e in employees)
        return total_projects / len(employees)
