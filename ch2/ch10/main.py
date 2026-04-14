import sys
import re
import sqlite3
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QWidget, QMainWindow, QVBoxLayout, 
                             QMessageBox, QTableWidget, QTableWidgetItem, QPushButton)
from PyQt6.QtCore import Qt
from PyQt6 import uic

class RegistrationForm(QMainWindow):
    def __init__(self):
        super().__init__()
        # Load UI into a widget and set as central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.ui = uic.loadUi('untitled.ui', self.central_widget)
        self.setWindowTitle('Đăng ký thành viên')
        
        # Initialize database
        self.init_database()
        
        # Populate date dropdowns
        self.populate_date_dropdowns()
        
        # Connect button
        self.central_widget.btnRegister.clicked.connect(self.register)
        
    def init_database(self):
        """Initialize SQLite database"""
        try:
            self.conn = sqlite3.connect('members.db')
            self.cursor = self.conn.cursor()
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS members (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ho TEXT NOT NULL,
                    ten TEXT NOT NULL,
                    contact TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    day INTEGER,
                    month INTEGER,
                    year INTEGER,
                    gender TEXT,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            self.conn.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(self, 'Lỗi Database', f'Lỗi kết nối database: {e}')
    
    def populate_date_dropdowns(self):
        """Populate day, month, year dropdowns"""
        # Days: 1-31
        days = [str(i) for i in range(1, 32)]
        self.central_widget.cbDay.addItems(['Ngày'] + days)
        
        # Months: 1-12
        months = [str(i) for i in range(1, 13)]
        self.central_widget.cbMonth.addItems(['Tháng'] + months)
        
        # Years: from 1950 to current year
        current_year = datetime.now().year
        years = [str(i) for i in range(current_year, 1949, -1)]
        self.central_widget.cbYear.addItems(['Năm'] + years)
    
    def validate_required_fields(self):
        """Validate all required fields"""
        errors = []
        
        # Check Họ (Last name)
        if not self.central_widget.txtHo.text().strip():
            errors.append('• Họ không được để trống')
        
        # Check Tên (First name)
        if not self.central_widget.txtTen.text().strip():
            errors.append('• Tên không được để trống')
        
        # Check Contact (Phone/Email)
        if not self.central_widget.txtContact.text().strip():
            errors.append('• Số di động hoặc email không được để trống')
        
        # Check Password
        if not self.central_widget.txtPassword.text().strip():
            errors.append('• Mật khẩu mới không được để trống')
        
        # Check Gender
        if not (self.central_widget.radNam.isChecked() or self.central_widget.radNu.isChecked()):
            errors.append('• Giới tính phải được chọn')
        
        # Check Agreement
        if not self.central_widget.chkAgree.isChecked():
            errors.append('• Phải đồng ý với các điều khoản')
        
        if errors:
            error_msg = 'Vui lòng kiểm tra:\n\n' + '\n'.join(errors)
            QMessageBox.warning(self, 'Cảnh báo', error_msg)
            return False
        return True
    
    def validate_password_strength(self):
        """Validate password strength"""
        password = self.central_widget.txtPassword.text()
        errors = []
        
        # Check minimum length (8 characters)
        if len(password) < 8:
            errors.append('• Ít nhất 8 ký tự')
        
        # Check for lowercase letters
        if not re.search(r'[a-z]', password):
            errors.append('• Ít nhất 1 ký tự a-z')
        
        # Check for uppercase letters
        if not re.search(r'[A-Z]', password):
            errors.append('• Ít nhất 1 ký tự A-Z')
        
        # Check for digits
        if not re.search(r'[0-9]', password):
            errors.append('• Ít nhất 1 ký tự số (0-9)')
        
        # Check for special characters
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:,.<>?]', password):
            errors.append('• Ít nhất 1 ký tự đặc biệt')
        
        if errors:
            error_msg = 'Mật khẩu không đủ mạnh:\n\n' + '\n'.join(errors)
            QMessageBox.warning(self, 'Mật khẩu yếu', error_msg)
            return False
        return True
    
    def validate_contact(self):
        """Validate phone number or email"""
        contact = self.central_widget.txtContact.text().strip()
        
        # Simple email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        # Simple phone validation (10-11 digits)
        phone_pattern = r'^\d{10,11}$'
        
        if not (re.match(email_pattern, contact) or re.match(phone_pattern, contact)):
            QMessageBox.warning(self, 'Lỗi', 
                              'Số di động hoặc email không hợp lệ')
            return False
        return True
    
    def save_to_database(self):
        """Save registration data to database"""
        try:
            ho = self.central_widget.txtHo.text().strip()
            ten = self.central_widget.txtTen.text().strip()
            contact = self.central_widget.txtContact.text().strip()
            password = self.central_widget.txtPassword.text().strip()
            day = int(self.central_widget.cbDay.currentText()) if self.central_widget.cbDay.currentText() != 'Ngày' else None
            month = int(self.central_widget.cbMonth.currentText()) if self.central_widget.cbMonth.currentText() != 'Tháng' else None
            year = int(self.central_widget.cbYear.currentText()) if self.central_widget.cbYear.currentText() != 'Năm' else None
            gender = 'Nam' if self.central_widget.radNam.isChecked() else 'Nữ'
            
            self.cursor.execute('''
                INSERT INTO members (ho, ten, contact, password, day, month, year, gender)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (ho, ten, contact, password, day, month, year, gender))
            
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, 'Lỗi', 
                              'Số di động hoặc email đã được đăng ký')
            return False
        except sqlite3.Error as e:
            QMessageBox.critical(self, 'Lỗi Database', f'Lỗi lưu dữ liệu: {e}')
            return False
    
    def register(self):
        """Handle registration button click"""
        # Validate required fields
        if not self.validate_required_fields():
            return
        
        # Validate contact format
        if not self.validate_contact():
            return
        
        # Validate password strength
        if not self.validate_password_strength():
            return
        
        # Save to database
        if self.save_to_database():
            QMessageBox.information(self, 'Thành công', 
                                  'Đăng ký thành công!')
            self.open_member_list()
    
    def open_member_list(self):
        """Open member list window after successful registration"""
        self.member_window = MemberListWindow(self.cursor, self.conn)
        self.member_window.show()
        self.close()


class MemberListWindow(QMainWindow):
    def __init__(self, cursor, conn):
        super().__init__()
        self.cursor = cursor
        self.conn = conn
        self.setWindowTitle('Danh sách thành viên')
        self.setGeometry(100, 100, 900, 600)
        
        # Create main widget
        main_widget = QWidget()
        layout = QVBoxLayout()
        
        # Create table
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            'ID', 'Họ', 'Tên', 'Liên hệ', 'Giới tính', 
            'Ngày sinh', 'Tháng sinh', 'Năm sinh', 'Ngày tạo'
        ])
        
        layout.addWidget(self.table)
        
        # Add button to go back
        back_button = QPushButton('Quay lại Đăng ký')
        back_button.clicked.connect(self.go_back)
        layout.addWidget(back_button)
        
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
        
        # Load data
        self.load_members()
    
    def load_members(self):
        """Load members from database"""
        try:
            self.cursor.execute('SELECT * FROM members ORDER BY id DESC')
            rows = self.cursor.fetchall()
            
            self.table.setRowCount(len(rows))
            
            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate(row_data):
                    item = QTableWidgetItem(str(value))
                    self.table.setItem(row_idx, col_idx, item)
            
            # Resize columns to content
            self.table.resizeColumnsToContents()
        except sqlite3.Error as e:
            QMessageBox.critical(self, 'Lỗi Database', f'Lỗi tải dữ liệu: {e}')
    
    def go_back(self):
        """Go back to registration form"""
        self.close()
        self.registration_window = RegistrationForm()
        self.registration_window.show()


def main():
    app = QApplication(sys.argv)
    window = RegistrationForm()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
