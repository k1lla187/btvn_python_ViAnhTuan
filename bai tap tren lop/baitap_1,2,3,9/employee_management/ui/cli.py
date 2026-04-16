import os
import sys
from typing import Tuple, Optional

# Thêm thư mục gốc vào path để import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Manager, Developer, Intern
from services.company import Company
from services.payroll import Payroll
from utils.validators import Validators
from utils.formatters import Formatters
from exceptions.employee_exceptions import EmployeeError, EmployeeNotFoundError, DuplicateEmployeeError

class EmployeeManagementApp:
    """
    Ứng dụng Quản lý Nhân viên giao diện dòng lệnh (CLI).
    Điều hướng người dùng qua các menu và kết nối với dịch vụ Company.
    """
    def __init__(self):
        self.company = Company()
        # Đường dẫn tệp dữ liệu tương đối so với vị trí của file này
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_file = os.path.join(base_dir, "data", "employees.json")
        self.ensure_data_dir()
        self.company.load_from_json(self.data_file)

    def ensure_data_dir(self) -> None:
        """Đảm bảo thư mục dữ liệu tồn tại."""
        data_dir = os.path.dirname(self.data_file)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

    def save_data(self) -> None:
        """Lưu trạng thái hiện tại vào tệp JSON."""
        self.company.save_to_json(self.data_file)

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def input_employee_data(self) -> Tuple[str, str, int, float]:
        """Nhập thông tin nhân viên cơ bản từ bàn phím."""
        while True:
            try:
                emp_id = input("Nhập ID: ").strip()
                if not emp_id:
                    print("ID không được để trống!")
                    continue
                
                name = input("Nhập tên: ").strip()
                if not name:
                    print("Tên không được để trống!")
                    continue
                
                age = int(input("Nhập tuổi: "))
                Validators.validate_age(age)
                base_salary = float(input("Nhập lương cơ bản: "))
                Validators.validate_salary(base_salary)
                return emp_id, name, age, base_salary
            except ValueError:
                print(f"Lỗi: Dữ liệu không hợp lệ. Vui lòng nhập lại.")
            except EmployeeError as e:
                print(f"Lỗi: {e}. Vui lòng nhập lại.")

    def add_manager(self):
        try:
            emp_id, name, age, salary = self.input_employee_data()
            while True:
                try:
                    tsize = int(input("Nhập quy mô team: "))
                    if tsize < 0:
                        print("Quy mô team phải >= 0!")
                        continue
                    break
                except ValueError:
                    print("Vui lòng nhập số nguyên!")
            
            self.company.add_employee(Manager(emp_id, name, age, salary, tsize))
            self.save_data()
            print("✓ Đã thêm Manager thành công!\n")
        except DuplicateEmployeeError as e:
            print(f"✗ Lỗi: {e}\n")
        except Exception as e:
            print(f"✗ Lỗi: {e}\n")

    def add_developer(self):
        try:
            emp_id, name, age, salary = self.input_employee_data()
            lang = input("Nhập ngôn ngữ lập trình: ").strip()
            if not lang:
                print("Ngôn ngữ lập trình không được để trống!")
                return
            
            self.company.add_employee(Developer(emp_id, name, age, salary, lang))
            self.save_data()
            print("✓ Đã thêm Developer thành công!\n")
        except DuplicateEmployeeError as e:
            print(f"✗ Lỗi: {e}\n")
        except Exception as e:
            print(f"✗ Lỗi: {e}\n")

    def add_intern(self):
        try:
            emp_id, name, age, salary = self.input_employee_data()
            major = input("Nhập chuyên ngành: ").strip()
            if not major:
                print("Chuyên ngành không được để trống!")
                return
            
            self.company.add_employee(Intern(emp_id, name, age, salary, major))
            self.save_data()
            print("✓ Đã thêm Intern thành công!\n")
        except DuplicateEmployeeError as e:
            print(f"✗ Lỗi: {e}\n")
        except Exception as e:
            print(f"✗ Lỗi: {e}\n")

    def display_all_employees(self):
        employees = self.company.get_all_employees()
        if not employees:
            print("✗ Danh sách nhân viên trống!\n")
            return
        
        print("\n" + "="*80)
        print("DANH SÁCH TẤT CẢ NHÂN VIÊN")
        print("="*80)
        for emp in employees:
            print(emp)
        print("="*80 + "\n")

    def display_employees_by_type(self):
        print("\nLoại nhân viên:")
        print("1. Manager | 2. Developer | 3. Intern")
        emp_type = input("Chọn loại (1-3): ").strip()
        
        type_map = {'1': 'Manager', '2': 'Developer', '3': 'Intern'}
        if emp_type not in type_map:
            print("✗ Lựa chọn không hợp lệ!\n")
            return
        
        employees = self.company.get_employees_by_type(type_map[emp_type])
        if not employees:
            print(f"✗ Không có {type_map[emp_type]} nào trong hệ thống!\n")
            return
        
        print(f"\n{'='*80}")
        print(f"DANH SÁCH {type_map[emp_type].upper()}")
        print("="*80)
        for emp in employees:
            print(emp)
        print("="*80 + "\n")

    def display_employees_by_performance(self):
        employees = self.company.get_top_performers()
        if not employees:
            print("✗ Danh sách nhân viên trống!\n")
            return
        
        print("\n" + "="*80)
        print("DANH SÁCH NHÂN VIÊN SẮP XẾP THEO HIỆU SUẤT (Cao → Thấp)")
        print("="*80)
        for i, emp in enumerate(employees, 1):
            print(f"{i}. {emp}")
        print("="*80 + "\n")

    def find_employee_by_id(self):
        try:
            eid = input("Nhập ID cần tìm: ").strip()
            emp = self.company.find_employee_by_id(eid)
            print(f"\n{'='*80}")
            print("THÔNG TIN NHÂN VIÊN")
            print("="*80)
            print(emp)
            print(f"Lương: {Formatters.format_currency(emp.calculate_salary())}")
            print(f"Dự án: {', '.join(emp.projects) if emp.projects else 'Chưa có'}")
            print("="*80 + "\n")
        except EmployeeNotFoundError as e:
            print(f"✗ Lỗi: {e}\n")

    def find_employees_by_name(self):
        try:
            name = input("Nhập tên cần tìm: ").strip()
            employees = self.company.find_employees_by_name(name)
            
            print(f"\n{'='*80}")
            print(f"KẾT QUẢ TÌM KIẾM ('{name}')")
            print("="*80)
            for emp in employees:
                print(emp)
            print("="*80 + "\n")
        except EmployeeNotFoundError as e:
            print(f"✗ Lỗi: {e}\n")

    def calculate_individual_salary(self):
        try:
            eid = input("Nhập ID nhân viên: ").strip()
            emp = self.company.find_employee_by_id(eid)
            salary = emp.calculate_salary()
            
            print(f"\n{'='*80}")
            print("TÍNH LƯƠNG CÁ NHÂN")
            print("="*80)
            print(f"Nhân viên: {emp.name} ({eid})")
            print(f"Lương cơ bản: {Formatters.format_currency(emp.base_salary)}")
            print(f"Điểm hiệu suất: {emp.performance_score}/10")
            print(f"Lương tổng cộng: {Formatters.format_currency(salary)}")
            print("="*80 + "\n")
        except EmployeeNotFoundError as e:
            print(f"✗ Lỗi: {e}\n")

    def display_total_payroll(self):
        if not self.company.get_all_employees():
            print("✗ Danh sách nhân viên trống!\n")
            return
        
        total = self.company.calculate_total_payroll()
        print(f"\n{'='*80}")
        print("TỔNG LƯƠNG CÔNG TY")
        print("="*80)
        print(f"Tổng lương tất cả nhân viên: {Formatters.format_currency(total)}")
        print("="*80 + "\n")

    def display_top_3_salaries(self):
        if not self.company.get_all_employees():
            print("✗ Danh sách nhân viên trống!\n")
            return
        
        top_3 = self.company.get_top_3_salaries()
        print(f"\n{'='*80}")
        print("TOP 3 NHÂN VIÊN LƯƠNG CAO NHẤT")
        print("="*80)
        for i, emp in enumerate(top_3, 1):
            print(f"{i}. {emp.name} ({emp.__class__.__name__}): {Formatters.format_currency(emp.calculate_salary())}")
        print("="*80 + "\n")

    def assign_project(self):
        try:
            eid = input("Nhập ID nhân viên: ").strip()
            emp = self.company.find_employee_by_id(eid)
            project = input("Nhập tên dự án: ").strip()
            
            if not project:
                print("✗ Tên dự án không được để trống!\n")
                return
            
            emp.add_project(project)
            self.save_data()
            print(f"✓ Đã phân công dự án '{project}' cho {emp.name}!\n")
        except EmployeeNotFoundError as e:
            print(f"✗ Lỗi: {e}\n")
        except EmployeeError as e:
            print(f"✗ Lỗi: {e}\n")

    def remove_project(self):
        try:
            eid = input("Nhập ID nhân viên: ").strip()
            emp = self.company.find_employee_by_id(eid)
            
            if not emp.projects:
                print("✗ Nhân viên này chưa tham gia dự án nào!\n")
                return
            
            print(f"Dự án hiện tại: {', '.join(emp.projects)}")
            project = input("Nhập tên dự án cần xóa: ").strip()
            
            emp.remove_project(project)
            self.save_data()
            print(f"✓ Đã xóa dự án '{project}' khỏi {emp.name}!\n")
        except EmployeeNotFoundError as e:
            print(f"✗ Lỗi: {e}\n")

    def display_projects(self):
        try:
            eid = input("Nhập ID nhân viên: ").strip()
            emp = self.company.find_employee_by_id(eid)
            
            print(f"\n{'='*80}")
            print(f"DANH SÁCH DỰ ÁN CỦA {emp.name.upper()}")
            print("="*80)
            if emp.projects:
                for i, project in enumerate(emp.projects, 1):
                    print(f"{i}. {project}")
            else:
                print("Chưa tham gia dự án nào")
            print("="*80 + "\n")
        except EmployeeNotFoundError as e:
            print(f"✗ Lỗi: {e}\n")

    def update_performance_score(self):
        try:
            eid = input("Nhập ID nhân viên: ").strip()
            emp = self.company.find_employee_by_id(eid)
            
            while True:
                try:
                    score = float(input("Nhập điểm hiệu suất (0-10): "))
                    emp.performance_score = score
                    self.save_data()
                    print(f"✓ Đã cập nhật điểm hiệu suất cho {emp.name}!\n")
                    break
                except ValueError as e:
                    print(f"✗ Lỗi: {e}\n")
        except EmployeeNotFoundError as e:
            print(f"✗ Lỗi: {e}\n")

    def remove_employee(self):
        try:
            eid = input("Nhập ID nhân viên cần xóa: ").strip()
            emp = self.company.find_employee_by_id(eid)
            confirm = input(f"Bạn có chắc chắn muốn xóa {emp.name}? (y/n): ").lower()
            
            if confirm == 'y':
                self.company.remove_employee(eid)
                self.save_data()
                print(f"✓ Đã xóa nhân viên {emp.name}!\n")
            else:
                print("✗ Đã hủy bỏ.\n")
        except EmployeeNotFoundError as e:
            print(f"✗ Lỗi: {e}\n")

    def increase_salary(self):
        try:
            eid = input("Nhập ID nhân viên: ").strip()
            emp = self.company.find_employee_by_id(eid)
            
            while True:
                try:
                    increase = float(input(f"Nhập mức tăng lương (VNĐ): "))
                    if increase < 0:
                        print("✗ Mức tăng phải >= 0!\n")
                        continue
                    
                    old_salary = emp.base_salary
                    emp.base_salary += increase
                    self.save_data()
                    print(f"✓ Đã tăng lương cho {emp.name}!")
                    print(f"  Lương cũ: {Formatters.format_currency(old_salary)}")
                    print(f"  Lương mới: {Formatters.format_currency(emp.base_salary)}\n")
                    break
                except ValueError:
                    print("✗ Vui lòng nhập số hợp lệ!\n")
        except EmployeeNotFoundError as e:
            print(f"✗ Lỗi: {e}\n")

    def promote_employee(self):
        try:
            eid = input("Nhập ID nhân viên: ").strip()
            emp = self.company.find_employee_by_id(eid)
            
            print(f"\nNhân viên hiện tại: {emp.name} - {emp.__class__.__name__}")
            print("Thăng chức:")
            print("1. Intern → Developer")
            print("2. Developer → Manager")
            
            choice = input("Chọn (1-2): ").strip()
            
            if choice == '1':
                if isinstance(emp, Intern):
                    lang = input("Nhập ngôn ngữ lập trình cho Developer mới: ").strip()
                    if lang:
                        self.company.promote_employee(eid, 'Developer', lang)
                        self.save_data()
                        print(f"✓ Đã thăng chức {emp.name} lên Developer!\n")
                    else:
                        print("✗ Ngôn ngữ không được để trống!\n")
                else:
                    print("✗ Chỉ có thể thăng chức từ Intern!\n")
            elif choice == '2':
                if isinstance(emp, Developer):
                    try:
                        tsize = int(input("Nhập quy mô team cho Manager mới: "))
                        self.company.promote_employee(eid, 'Manager', tsize)
                        self.save_data()
                        print(f"✓ Đã thăng chức {emp.name} lên Manager!\n")
                    except ValueError:
                        print("✗ Vui lòng nhập số nguyên!\n")
                else:
                    print("✗ Chỉ có thể thăng chức từ Developer!\n")
            else:
                print("✗ Lựa chọn không hợp lệ!\n")
        except EmployeeNotFoundError as e:
            print(f"✗ Lỗi: {e}\n")

    def display_statistics(self):
        employees = self.company.get_all_employees()
        
        if not employees:
            print("✗ Danh sách nhân viên trống!\n")
            return
        
        managers = self.company.get_employees_by_type('Manager')
        developers = self.company.get_employees_by_type('Developer')
        interns = self.company.get_employees_by_type('Intern')
        
        avg_projects = Payroll.calculate_average_projects(employees)
        total_payroll = self.company.calculate_total_payroll()
        
        excellent = [e for e in employees if e.performance_score > 8]
        need_improvement = [e for e in employees if e.performance_score < 5]
        
        print(f"\n{'='*80}")
        print("THỐNG KÊ BÁO CÁO")
        print("="*80)
        print(f"Tổng số nhân viên: {len(employees)}")
        print(f"  - Manager: {len(managers)}")
        print(f"  - Developer: {len(developers)}")
        print(f"  - Intern: {len(interns)}")
        print(f"\nTổng quỹ lương công ty: {Formatters.format_currency(total_payroll)}")
        print(f"Lương bình quân: {Formatters.format_currency(total_payroll / len(employees)) if employees else 0}")
        print(f"\nSố dự án trung bình/nhân viên: {avg_projects:.2f}")
        print(f"\nNhân viên xuất sắc (Điểm > 8): {len(excellent)}")
        for e in excellent:
            print(f"  - {e.name} ({e.performance_score}/10)")
        print(f"\nNhân viên cần cải thiện (Điểm < 5): {len(need_improvement)}")
        for e in need_improvement:
            print(f"  - {e.name} ({e.performance_score}/10)")
        print("="*80 + "\n")

    def run(self):
        while True:
            print(Formatters.format_header("HỆ THỐNG QUẢN LÝ NHÂN VIÊN CÔNG TY ABC"))
            print("1. Thêm nhân viên mới")
            print("   a. Thêm Manager | b. Thêm Developer | c. Thêm Intern")
            print("2. Hiển thị danh sách nhân viên")
            print("   a. Tất cả | b. Theo loại | c. Theo hiệu suất")
            print("3. Tìm kiếm nhân viên")
            print("   a. Theo ID | b. Theo tên")
            print("4. Quản lý lương")
            print("   a. Tính lương cá nhân | b. Tổng lương công ty | c. Top 3")
            print("5. Quản lý dự án")
            print("   a. Phân công | b. Xóa khỏi dự án | c. Hiển thị dự án")
            print("6. Đánh giá hiệu suất")
            print("7. Quản lý nhân sự (Xóa/Tăng lương/Thăng chức)")
            print("8. Thống kê báo cáo")
            print("9. Thoát")
            
            choice = input("\nChọn chức năng (1-9): ").lower().strip()

            try:
                if choice == '1a':
                    self.add_manager()
                elif choice == '1b':
                    self.add_developer()
                elif choice == '1c':
                    self.add_intern()
                elif choice == '2a':
                    self.display_all_employees()
                elif choice == '2b':
                    self.display_employees_by_type()
                elif choice == '2c':
                    self.display_employees_by_performance()
                elif choice == '3a':
                    self.find_employee_by_id()
                elif choice == '3b':
                    self.find_employees_by_name()
                elif choice == '4a':
                    self.calculate_individual_salary()
                elif choice == '4b':
                    self.display_total_payroll()
                elif choice == '4c':
                    self.display_top_3_salaries()
                elif choice == '5a':
                    self.assign_project()
                elif choice == '5b':
                    self.remove_project()
                elif choice == '5c':
                    self.display_projects()
                elif choice == '6':
                    self.update_performance_score()
                elif choice == '7':
                    self.display_hr_menu()
                elif choice == '8':
                    self.display_statistics()
                elif choice == '9':
                    print("\nCảm ơn bạn đã sử dụng hệ thống!")
                    break
                else:
                    print("✗ Lựa chọn không hợp lệ. Vui lòng thử lại.\n")
            except Exception as e:
                print(f"✗ Đã xảy ra lỗi: {e}\n")

    def display_hr_menu(self):
        while True:
            print("\n" + "="*80)
            print("QUẢN LÝ NHÂN SỰ")
            print("="*80)
            print("1. Xóa nhân viên")
            print("2. Tăng lương cơ bản")
            print("3. Thăng chức")
            print("4. Quay lại menu chính")
            
            choice = input("Chọn (1-4): ").strip()
            
            if choice == '1':
                self.remove_employee()
            elif choice == '2':
                self.increase_salary()
            elif choice == '3':
                self.promote_employee()
            elif choice == '4':
                break
            else:
                print("✗ Lựa chọn không hợp lệ!\n")
