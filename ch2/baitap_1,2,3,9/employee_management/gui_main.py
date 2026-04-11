import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
import sys
from typing import Optional, List

# Thêm thư mục gốc vào path để import các module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.manager import Manager
from models.developer import Developer
from models.intern import Intern
from services.company import Company
from services.payroll import Payroll
from utils.formatters import Formatters
from utils.validators import Validators
from exceptions.employee_exceptions import EmployeeError, EmployeeNotFoundError

class EmployeeWinForm(tk.Tk):
    """
    Giao diện Quản lý Nhân viên phong cách Windows Forms.
    Sử dụng kiến trúc Menu-driven và Master-Detail view.
    """
    def __init__(self):
        super().__init__()

        self.title("Hệ thống Quản lý Nhân viên (WinForm Edition)")
        self.geometry("1100x700")
        self.setup_styles()

        # Khởi tạo Service
        self.company = Company()
        self.data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "employees.json")
        self.load_data()

        # Xây dựng giao diện
        self.create_menu()
        self.create_toolbar()
        self.create_main_content()
        self.create_status_bar()

        # Phím tắt
        self.bind("<Control-s>", lambda e: self.save_data())
        self.bind("<Control-f>", lambda e: self.focus_search())
        self.bind("<F5>", lambda e: self.refresh_table())

        self.refresh_table()
        self.update_status("Sẵn sàng")

    def setup_styles(self):
        """Thiết lập phong cách đồ họa chuẩn Windows."""
        self.style = ttk.Style()
        # Cố gắng sử dụng theme hệ thống nếu có
        themes = self.style.theme_names()
        if 'vista' in themes: self.style.theme_use('vista')
        elif 'winnative' in themes: self.style.theme_use('winnative')
        
        # Tùy chỉnh Font chữ hiện đại hơn
        default_font = ("Segoe UI", 9)
        header_font = ("Segoe UI", 10, "bold")
        self.option_add("*Font", default_font)
        
        self.style.configure("Treeview.Heading", font=header_font)
        self.style.configure("WinForm.TButton", padding=5)
        self.style.configure("Status.TLabel", padding=(5, 2))

    def create_menu(self):
        """Tạo thanh MenuStrip phía trên cùng."""
        self.menubar = tk.Menu(self)

        # Menu Hệ thống
        file_menu = tk.Menu(self.menubar, tearoff=0)
        file_menu.add_command(label="Tải dữ liệu (F5)", command=self.refresh_table)
        file_menu.add_command(label="Lưu dữ liệu (Ctrl+S)", command=self.save_data)
        file_menu.add_separator()
        file_menu.add_command(label="Thoát", command=self.quit)
        self.menubar.add_cascade(label="Hệ thống", menu=file_menu)

        # Menu Quản lý
        manage_menu = tk.Menu(self.menubar, tearoff=0)
        manage_menu.add_command(label="Thêm Manager...", command=lambda: self.add_employee_dialog('Manager'))
        manage_menu.add_command(label="Thêm Developer...", command=lambda: self.add_employee_dialog('Developer'))
        manage_menu.add_command(label="Thêm Intern...", command=lambda: self.add_employee_dialog('Intern'))
        manage_menu.add_separator()
        manage_menu.add_command(label="Tăng lương...", command=self.increase_salary)
        manage_menu.add_command(label="Giảm lương...", command=self.decrease_salary)
        manage_menu.add_separator()
        manage_menu.add_command(label="Xóa nhân viên", command=self.delete_employee)
        manage_menu.add_command(label="Thăng chức...", command=self.promote_employee)
        manage_menu.add_command(label="Cho nghỉ việc (Đền bù)...", command=self.terminate_employee)
        self.menubar.add_cascade(label="Quản lý Nhân sự", menu=manage_menu)

        # Menu Báo cáo
        report_menu = tk.Menu(self.menubar, tearoff=0)
        report_menu.add_command(label="Tổng hợp quỹ lương", command=self.show_payroll_stats)
        report_menu.add_command(label="Thống kê hiệu suất", command=self.show_performance_stats)
        report_menu.add_separator()
        report_menu.add_command(label="Phân bổ Dự án (Sắp xếp)", command=self.show_project_stats)
        report_menu.add_command(label="Tìm nhân viên theo Dự án", command=self.find_by_project)
        self.menubar.add_cascade(label="Báo cáo", menu=report_menu)

        # Menu Trợ giúp
        help_menu = tk.Menu(self.menubar, tearoff=0)
        help_menu.add_command(label="Về phần mềm", command=lambda: messagebox.showinfo("About", "Hệ thống Quản lý Nhân viên\nPhiên bản: 2.0 WinForm\nTác giả: Vi Anh Tuấn"))
        self.menubar.add_cascade(label="Trợ giúp", menu=help_menu)

        self.config(menu=self.menubar)

    def create_toolbar(self):
        """Tạo thanh công cụ (ToolStrip) dưới menu."""
        toolbar = ttk.Frame(self, relief="raised", padding=2)
        toolbar.pack(side="top", fill="x")

        # Nút chức năng nhanh
        self.btn_add = ttk.Button(toolbar, text="⊕ Thêm nhân viên", command=self.add_employee_menu)
        self.btn_add.pack(side="left", padx=2)

        self.btn_edit = ttk.Button(toolbar, text="✎ Cập nhật điểm", command=self.update_score)
        self.btn_edit.pack(side="left", padx=2)

        self.btn_del = ttk.Button(toolbar, text="☒ Xóa", command=self.delete_employee)
        self.btn_del.pack(side="left", padx=2)

        ttk.Separator(toolbar, orient="vertical").pack(side="left", fill="y", padx=5)

        # Thanh tìm kiếm
        ttk.Label(toolbar, text="Tìm kiếm: ").pack(side="left", padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.filter_table())
        self.search_entry = ttk.Entry(toolbar, textvariable=self.search_var, width=30)
        self.search_entry.pack(side="left", padx=2)

    def create_main_content(self):
        """Tạo khu vực nội dung chính (Master-Detail)."""
        paned = ttk.PanedWindow(self, orient="horizontal")
        paned.pack(fill="both", expand=True)

        # Left Panel: Treeview (Master)
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=3)

        columns = ("id", "name", "type", "salary", "performance", "projects")
        self.tree = ttk.Treeview(left_frame, columns=columns, show="headings", selectmode="browse")
        
        self.tree.heading("id", text="Mã NV", command=lambda: self.sort_tree("id"))
        self.tree.heading("name", text="Họ và Tên", command=lambda: self.sort_tree("name"))
        self.tree.heading("type", text="Chức vụ", command=lambda: self.sort_tree("type"))
        self.tree.heading("salary", text="Lương (VNĐ)", command=lambda: self.sort_tree("salary"))
        self.tree.heading("performance", text="Điểm HS", command=lambda: self.sort_tree("performance"))
        self.tree.heading("projects", text="Số Dự án", command=lambda: self.sort_tree("projects"))

        self.tree.column("id", width=80, anchor="center")
        self.tree.column("name", width=200)
        self.tree.column("type", width=120, anchor="center")
        self.tree.column("salary", width=150, anchor="e")
        self.tree.column("performance", width=80, anchor="center")
        self.tree.column("projects", width=80, anchor="center")

        scroll = ttk.Scrollbar(left_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        self.tree.bind("<<TreeviewSelect>>", self.on_employee_select)

        # Right Panel: Details (Detail)
        self.right_panel = ttk.LabelFrame(paned, text="Chi tiết Nhân viên", padding=10)
        paned.add(self.right_panel, weight=1)

        # Các nhãn hiển thị thông tin
        self.lbl_id = ttk.Label(self.right_panel, text="Mã NV: -", font=("Segoe UI", 10, "bold"))
        self.lbl_id.pack(anchor="w", pady=5)
        self.lbl_name = ttk.Label(self.right_panel, text="Họ tên: -")
        self.lbl_name.pack(anchor="w", pady=2)
        self.lbl_type = ttk.Label(self.right_panel, text="Chức vụ: -")
        self.lbl_type.pack(anchor="w", pady=2)
        self.lbl_salary = ttk.Label(self.right_panel, text="Lương hiện tại: -")
        self.lbl_salary.pack(anchor="w", pady=2)
        
        self.separator = ttk.Separator(self.right_panel, orient="horizontal")
        self.separator.pack(fill="x", pady=10)

        # Area cho các thông tin riêng của từng loại
        self.info_frame = ttk.Frame(self.right_panel)
        self.info_frame.pack(fill="x", pady=5)
        self.lbl_extra = ttk.Label(self.info_frame, text="")
        self.lbl_extra.pack(anchor="w")

        # Panel Dự án
        ttk.Label(self.right_panel, text="Danh sách Dự án:", font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(10, 0))
        self.list_projects = tk.Listbox(self.right_panel, height=6, bg="#f8f9fa")
        self.list_projects.pack(fill="x", pady=5)

        # Nút thao tác nhanh trên Detail panel
        btn_frame = ttk.Frame(self.right_panel)
        btn_frame.pack(fill="x", pady=10)
        
        ttk.Button(btn_frame, text="Assign Project", command=self.add_project).pack(side="left", expand=True, padx=2)
        ttk.Button(btn_frame, text="Promote", command=self.promote_employee).pack(side="left", expand=True, padx=2)

    def create_status_bar(self):
        """Tạo thanh trạng thái ở đáy cửa sổ."""
        self.status_var = tk.StringVar(value="Đang sẵn sàng...")
        self.status_bar = ttk.Label(self, textvariable=self.status_var, relief="sunken", anchor="w", style="Status.TLabel")
        self.status_bar.pack(side="bottom", fill="x")

    # --- Các hàm xử lý nghiệp vụ ---

    def load_data(self):
        self.company.load_from_json(self.data_file)

    def save_data(self):
        self.company.save_to_json(self.data_file)
        self.update_status("✓ Dữ liệu đã được lưu!")
        messagebox.showinfo("Thông báo", "Dữ liệu đã được lưu thành công vào employees.json")

    def update_status(self, message: str):
        self.status_var.set(message)

    def refresh_table(self, query: Optional[str] = None):
        """
        Tải lại dữ liệu lên bảng.
        Nếu có query, chỉ hiển thị những nhân viên khớp với từ khóa.
        """
        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Thêm dữ liệu mới
        employees = self.company.get_all_employees()
        count = 0
        
        for emp in employees:
            # Kiểm tra bộ lọc nếu có
            if query:
                match_fields = [
                    emp.emp_id,
                    emp.name,
                    emp.__class__.__name__
                ]
                if not any(query.lower() in str(f).lower() for f in match_fields):
                    continue

            self.tree.insert("", "end", iid=emp.emp_id, values=(
                emp.emp_id,
                emp.name,
                emp.__class__.__name__,
                Formatters.format_currency(emp.calculate_salary()),
                f"{emp.performance_score}/10",
                len(emp.projects)
            ))
            count += 1
            
        if query:
            self.update_status(f"Tìm thấy {count} kết quả cho '{query}'.")
        else:
            self.update_status(f"Đã tải {len(employees)} nhân viên.")

    def filter_table(self):
        """Handler khi người dùng nhập vào ô tìm kiếm."""
        query = self.search_var.get().strip()
        self.refresh_table(query if query else None)

    def on_employee_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        
        emp_id = selected[0]
        emp = self.company.find_employee_by_id(emp_id)
        
        # Cập nhật GUI
        self.lbl_id.config(text=f"Mã NV: {emp.emp_id}")
        self.lbl_name.config(text=f"Họ tên: {emp.name} ({emp.age} tuổi)")
        self.lbl_type.config(text=f"Chức vụ: {emp.__class__.__name__}")
        self.lbl_salary.config(text=f"Lương: {Formatters.format_currency(emp.calculate_salary())}")
        
        # Thông tin riêng
        if isinstance(emp, Manager):
            self.lbl_extra.config(text=f"Quy mô Team: {emp.team_size} nhân viên")
        elif isinstance(emp, Developer):
            self.lbl_extra.config(text=f"Ngôn ngữ: {emp.programming_language}")
        elif isinstance(emp, Intern):
            self.lbl_extra.config(text=f"Chuyên ngành: {emp.major}")

        # Dự án
        self.list_projects.delete(0, tk.END)
        for proj in emp.projects:
            self.list_projects.insert(tk.END, f"• {proj}")
            
        self.update_status(f"Đang xem: {emp.name}")

    def add_employee_menu(self):
        # Menu popup chọn loại nhân viên
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Manager", command=lambda: self.add_employee_dialog('Manager'))
        menu.add_command(label="Developer", command=lambda: self.add_employee_dialog('Developer'))
        menu.add_command(label="Intern", command=lambda: self.add_employee_dialog('Intern'))
        
        # Mở ở vị trí nút
        x = self.btn_add.winfo_rootx()
        y = self.btn_add.winfo_rooty() + self.btn_add.winfo_height()
        menu.post(x, y)

    def add_employee_dialog(self, etype: str):
        dialog = AddEmployeeDialog(self, etype)
        self.wait_window(dialog)
        if dialog.result:
            try:
                self.company.add_employee(dialog.result)
                self.save_data()
                self.refresh_table()
                messagebox.showinfo("Thành công", f"Đã thêm {etype} thành công!")
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))

    def update_score(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một nhân viên!")
            return
        
        emp_id = selected[0]
        emp = self.company.find_employee_by_id(emp_id)
        
        score = simpledialog.askfloat("Cập nhật điểm", f"Nhập điểm hiệu suất mới cho {emp.name} (0-10):", minvalue=0, maxvalue=10)
        if score is not None:
            emp.performance_score = score
            self.save_data()
            self.refresh_table()
            self.on_employee_select(None)

    def increase_salary(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một nhân viên!")
            return
        
        emp_id = selected[0]
        emp = self.company.find_employee_by_id(emp_id)
        
        amount = simpledialog.askfloat("Tăng lương", f"Nhập số tiền tăng cho {emp.name} (VNĐ):", minvalue=0)
        if amount:
            emp.base_salary += amount
            self.save_data()
            self.refresh_table()
            messagebox.showinfo("Thành công", f"Đã tăng lương thành công cho {emp.name}")

    def decrease_salary(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một nhân viên!")
            return
        
        emp_id = selected[0]
        emp = self.company.find_employee_by_id(emp_id)
        
        amount = simpledialog.askfloat("Giảm lương", f"Nhập số tiền giảm cho {emp.name} (VNĐ):", minvalue=0)
        if amount:
            try:
                self.company.decrease_salary(emp_id, amount)
                self.save_data()
                self.refresh_table()
                messagebox.showinfo("Thành công", f"Đã giảm lương thành công cho {emp.name}")
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))

    def delete_employee(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn nhân viên cần xóa!")
            return
        
        emp_id = selected[0]
        emp = self.company.find_employee_by_id(emp_id)
        
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa nhân viên {emp.name}?"):
            self.company.remove_employee(emp_id)
            self.save_data()
            self.refresh_table()
            self.update_status(f"Đã xóa {emp.name}")

    def add_project(self):
        selected = self.tree.selection()
        if not selected: return
        
        emp_id = selected[0]
        emp = self.company.find_employee_by_id(emp_id)
        
        p_name = simpledialog.askstring("Phân công", "Nhập tên dự án mới:")
        if p_name:
            try:
                emp.add_project(p_name)
                self.save_data()
                self.on_employee_select(None)
            except EmployeeError as e:
                messagebox.showerror("Lỗi", str(e))

    def promote_employee(self):
        selected = self.tree.selection()
        if not selected: return
        
        emp_id = selected[0]
        emp = self.company.find_employee_by_id(emp_id)
        
        if isinstance(emp, Manager):
            messagebox.showinfo("Thông tin", "Nhân viên này đã ở cấp Quản lý cao nhất.")
            return

        if isinstance(emp, Intern):
            new_type = 'Developer'
            extra_lbl = "Ngôn ngữ lập trình:"
        else: # Developer
            new_type = 'Manager'
            extra_lbl = "Quy mô Team (số người):"

        extra_info = simpledialog.askstring("Thăng chức", f"Thăng chức lên {new_type}.\n{extra_lbl}")
        if extra_info:
            try:
                self.company.promote_employee(emp_id, new_type, extra_info)
                self.save_data()
                self.refresh_table()
                messagebox.showinfo("Chúc mừng", f"Đã thăng chức thành công lên {new_type}!")
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))

    def terminate_employee(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn nhân viên!")
            return
        
        emp_id = selected[0]
        emp = self.company.find_employee_by_id(emp_id)
        
        if messagebox.askyesno("Xác nhận Cho nghỉ việc", f"Bạn có chắc muốn cho nhân viên {emp.name} nghỉ việc?\nHành động này sẽ tính toán khoản đền bù hợp đồng."):
            try:
                compensation = self.company.terminate_employee(emp_id)
                self.save_data()
                self.refresh_table()
                messagebox.showinfo("Kết quả Đền bù", f"Nhân viên {emp.name} đã nghỉ việc.\nSố tiền đền bù hợp đồng là: {Formatters.format_currency(compensation)}")
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))

    def show_payroll_stats(self):
        total = self.company.calculate_total_payroll()
        count = len(self.company.get_all_employees())
        avg = total / count if count > 0 else 0
        
        msg = f"Tổng nhân sự: {count}\n"
        msg += f"Tổng quỹ lương: {Formatters.format_currency(total)}\n"
        msg += f"Lương trung bình: {Formatters.format_currency(avg)}"
        messagebox.showinfo("Báo cáo Tài chính", msg)

    def show_performance_stats(self):
        top = self.company.get_top_performers()[:3]
        if not top: return
        
        msg = "TOP 3 NHÂN VIÊN XUẤT SẮC:\n\n"
        for i, emp in enumerate(top, 1):
            msg += f"{i}. {emp.name} - Điểm: {emp.performance_score}\n"
        messagebox.showinfo("Báo cáo Hiệu suất", msg)

    def show_project_stats(self):
        employees = self.company.get_employees_sorted_by_projects()
        if not employees: return
        
        msg = "THỐNG KÊ PHÂN BỔ DỰ ÁN (Nhiều -> Ít):\n\n"
        for i, emp in enumerate(employees, 1):
            msg += f"{i}. {emp.name}: {len(emp.projects)} dự án\n"
        messagebox.showinfo("Báo cáo Dự án", msg)

    def find_by_project(self):
        p_name = simpledialog.askstring("Tìm theo Dự án", "Nhập tên dự án cần tra cứu:")
        if not p_name: return
        
        employees = self.company.get_employees_by_project(p_name)
        if not employees:
            messagebox.showinfo("Kết quả", f"Không tìm thấy nhân viên nào tham gia dự án '{p_name}'")
            return
        
        msg = f"DANH SÁCH NHÂN VIÊN THAM GIA DỰ ÁN '{p_name}':\n\n"
        for i, emp in enumerate(employees, 1):
            msg += f"{i}. {emp.name} ({emp.emp_id})\n"
        messagebox.showinfo("Kết quả Tra cứu", msg)

    def sort_tree(self, col):
        """Sắp xếp lại bảng khi nhấn vào tiêu đề cột."""
        items = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        
        # Thử chuyển sang số để sắp xếp chuẩn hơn
        try:
            items.sort(key=lambda t: float(t[0].replace(' VNĐ', '').replace(',', '')), reverse=False)
        except ValueError:
            items.sort(reverse=False)

        for index, (val, k) in enumerate(items):
            self.tree.move(k, '', index)

    def focus_search(self):
        self.search_entry.focus_set()

# --- Modal Dialog cho việc thêm nhân viên ---

class AddEmployeeDialog(tk.Toplevel):
    def __init__(self, parent, etype: str):
        super().__init__(parent)
        self.title(f"Thêm {etype}")
        self.geometry("400x450")
        self.etype = etype
        self.result = None
        self.transient(parent)
        self.grab_set()

        frame = ttk.Frame(self, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text=f"THÔNG TIN {etype.upper()}", font=("Segoe UI", 12, "bold")).pack(pady=(0, 20))

        # Form fields
        self.entries = {}
        fields = [("id", "Mã nhân viên:"), ("name", "Họ tên:"), ("age", "Tuổi:"), ("salary", "Lương cơ bản:")]
        
        if etype == 'Manager': fields.append(("team", "Quy mô team:"))
        elif etype == 'Developer': fields.append(("extra", "Ngôn ngữ lập trình:"))
        elif etype == 'Intern': fields.append(("extra", "Chuyên ngành:"))

        for key, lbl in fields:
            ttk.Label(frame, text=lbl).pack(anchor="w", pady=(5, 0))
            ent = ttk.Entry(frame)
            ent.pack(fill="x", pady=(0, 5))
            self.entries[key] = ent

        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", pady=(20, 0))
        
        ttk.Button(btn_frame, text="Lưu", command=self.save).pack(side="right", padx=5)
        ttk.Button(btn_frame, text="Hủy", command=self.destroy).pack(side="right")

    def save(self):
        try:
            eid = self.entries['id'].get().strip()
            name = self.entries['name'].get().strip()
            age = int(self.entries['age'].get())
            salary = float(self.entries['salary'].get())
            
            Validators.validate_age(age)
            Validators.validate_salary(salary)

            if self.etype == 'Manager':
                self.result = Manager(eid, name, age, salary, int(self.entries['team'].get()))
            elif self.etype == 'Developer':
                self.result = Developer(eid, name, age, salary, self.entries['extra'].get())
            elif self.etype == 'Intern':
                self.result = Intern(eid, name, age, salary, self.entries['extra'].get())
            
            self.destroy()
        except Exception as e:
            messagebox.showerror("Lỗi dữ liệu", str(e))

if __name__ == "__main__":
    app = EmployeeWinForm()
    app.mainloop()
